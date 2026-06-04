# Databricks notebook source
 %run ./mhsds_functions

# COMMAND ----------

 %run ./measure_metadata

# COMMAND ----------

 %run ./parameters

# COMMAND ----------

# dbutils.widgets.text("db_output", "personal_db")
# dbutils.widgets.text("db_source", "mhsds_database")
# dbutils.widgets.text("rp_enddate", "2026-03-31")
# dbutils.widgets.text("status", "Adhoc")

# COMMAND ----------

db_output = dbutils.widgets.get("db_output")
db_source = dbutils.widgets.get("db_source")
rp_startdate_1m = dbutils.widgets.get("rp_startdate_1m")
rp_enddate = dbutils.widgets.get("rp_enddate")
status = dbutils.widgets.get("status")
product = dbutils.widgets.get("product")
# db_output = "personal_db"
# db_source = "mhsds_database"
# rp_startdate_1m = "2026-03-01"
# rp_enddate = "2026-03-31"
# status = "Adhoc"
# product = "ALL"

# COMMAND ----------

 %sql 
 DELETE FROM $db_output.bbrb_final_raw
 WHERE REPORTING_PERIOD_END = '$rp_enddate'
 AND STATUS = '$status'
 AND SOURCE_DB = '$db_source'
 ;
 VACUUM $db_output.bbrb_final_raw RETAIN 8 HOURS;

# COMMAND ----------

 %sql 
 DELETE FROM $db_output.bbrb_final_suppressed
 WHERE REPORTING_PERIOD_END = '$rp_enddate'
 AND STATUS = '$status'
 AND SOURCE_DB = '$db_source'
 ;
 VACUUM $db_output.bbrb_final_suppressed RETAIN 8 HOURS;

# COMMAND ----------

# DBTITLE 1,Population Agg
pop_dfs = []
for pop_id in pop_metadata:
  pop_name = pop_metadata[pop_id]["measure_name"]
  age_group_filter = pop_metadata[pop_id]["age_group"]
  breakdowns = pop_metadata[pop_id]["breakdowns"]
  for breakdown in breakdowns:
    source_table = breakdown["source_table"]
    aggregate_field = breakdown["aggregate_field"]
    breakdown_name = breakdown["breakdown_name"]
    primary_level = breakdown["primary_level"]
    primary_level_desc = breakdown["primary_level_desc"]
    secondary_level = breakdown["secondary_level"]
    secondary_level_desc = breakdown["secondary_level_desc"]
    print(pop_id, breakdown_name)
    #create agg df
    agg_df = produce_filter_agg_df(
      db_output, db_source, source_table, age_group_filter,
      rp_startdate_1m, rp_enddate, primary_level, primary_level_desc, secondary_level, secondary_level_desc, 
      aggregate_field, breakdown_name, status, 
      pop_id, pop_id, pop_id, pop_name, output_columns
    )
    pop_dfs.append(agg_df)

final_pop_df = unionAll(*pop_dfs)

# COMMAND ----------

# DBTITLE 1,Get measure metadata depending on product selected
product_measure_metadata = measure_metadata[product] #metadata used in aggregation depends on product
count_measure_ids = [measure_id for measure_id in product_measure_metadata if product_measure_metadata[measure_id]["crude_rate"] != 1]
crude_rate_measure_ids = [measure_id for measure_id in product_measure_metadata if product_measure_metadata[measure_id]["crude_rate"] == 1]

# COMMAND ----------

num_partitions = spark.sparkContext.defaultParallelism
target_tasks_per_job = num_partitions * 2
batch_size = max(5, int(target_tasks_per_job / 10))
print(f"Batch Size: {batch_size}")

raw_count_dfs = []
raw_crude_dfs = []

supp_details = []
supp_dfs = []

pop_raw = (
    final_pop_df
    .withColumn("MEASURE_VALUE", F.coalesce(F.col("MEASURE_VALUE"), F.lit(0)))
    .select(*output_columns)
)
raw_count_dfs.append(pop_raw)

# COMMAND ----------

# DBTITLE 1,Product Agg for Count Measures
for measure_id in count_measure_ids:  
  measure_dict = product_measure_metadata[measure_id]
  measure_name = measure_dict["name"]
  measure_freq = measure_dict["freq"]
  measure_rp_startdate = mh_freq_to_rp_startdate(measure_freq, rp_startdate_1m)
  source_table = measure_dict["source_table"]
  filter_clause = measure_dict["filter_clause"]
  aggregate_field = measure_dict["aggregate_field"]
  aggregate_function = measure_dict["aggregate_function"]
  numerator_id = measure_dict["numerator_id"]
  denominator_id = measure_dict["denominator"]
  suppression_type = measure_dict["suppression"]
  measure_breakdowns = measure_dict["breakdowns"]
  
  for breakdown in measure_breakdowns:
    breakdown_name = breakdown["breakdown_name"]
    print(f"{measure_id}: {breakdown_name}")
    primary_level = breakdown["primary_level"]
    primary_level_desc = breakdown["primary_level_desc"]
    secondary_level = breakdown["secondary_level"]
    secondary_level_desc = breakdown["secondary_level_desc"]
    #create agg df
    agg_df = aggregate_function(
      db_output, db_source, source_table, filter_clause,
      measure_rp_startdate, rp_enddate, primary_level, primary_level_desc, secondary_level, secondary_level_desc, 
      aggregate_field, breakdown_name, status, measure_id, numerator_id, denominator_id, 
      measure_name, output_columns)
    
    raw_count_df = (
      agg_df
      .withColumn("MEASURE_VALUE", F.coalesce(F.col("MEASURE_VALUE"), F.lit(0)))
      .select(*output_columns)      
    )
    
    raw_count_dfs.append(raw_count_df)
    supp_details.append((suppression_type, breakdown_name, measure_id, numerator_id, measure_name))
    
    if len(raw_count_dfs) >= batch_size:
      batch_count_df = unionAll(*raw_count_dfs)
      insert_agg_df(batch_count_df, db_output, "bbrb_final_raw")
      raw_count_dfs = []

if raw_count_dfs:      
  batch_count_df = unionAll(*raw_count_dfs)
  insert_agg_df(batch_count_df, db_output, "bbrb_final_raw")

# COMMAND ----------

# DBTITLE 1,Product Agg for Crude Rate Measures
for measure_id in crude_rate_measure_ids:    
    measure_dict = product_measure_metadata[measure_id]
    measure_name = measure_dict["name"]
    measure_freq = measure_dict["freq"]
    measure_rp_startdate = mh_freq_to_rp_startdate(measure_freq, rp_startdate_1m)
    source_table = measure_dict["source_table"]
    filter_clause = measure_dict["filter_clause"]
    aggregate_field = measure_dict["aggregate_field"]
    aggregate_function = measure_dict["aggregate_function"]
    numerator_id = measure_dict["numerator_id"]
    denominator_id = measure_dict["denominator"]
    suppression_type = measure_dict["suppression"]
    measure_breakdowns = measure_dict["breakdowns"]

    for breakdown in measure_breakdowns:
        breakdown_name = breakdown["breakdown_name"]
        print(f"{measure_id}: {breakdown_name}")
        primary_level = F.col("PRIMARY_LEVEL")
        primary_level_desc = F.col("PRIMARY_LEVEL_DESCRIPTION")
        secondary_level = F.col("SECONDARY_LEVEL")
        secondary_level_desc = F.col("SECONDARY_LEVEL_DESCRIPTION")
        #create agg_df
        agg_df = aggregate_function(
            db_output, db_source, "bbrb_final_raw", filter_clause,
            measure_rp_startdate, rp_enddate, primary_level, primary_level_desc, secondary_level, secondary_level_desc,
            aggregate_field, breakdown_name, status, measure_id, numerator_id, denominator_id,
            measure_name, output_columns)
    
        raw_crude_df = (
            agg_df
            .withColumn("MEASURE_VALUE", F.coalesce(F.col("MEASURE_VALUE"), F.lit(0)))
            .select(*output_columns)      
        )
        
        raw_crude_dfs.append(raw_crude_df)
        supp_details.append((suppression_type, breakdown_name, measure_id, numerator_id, measure_name))
        
        if len(raw_crude_dfs) >= batch_size:
            batch_crude_df = unionAll(*raw_crude_dfs)
            insert_agg_df(batch_crude_df, db_output, "bbrb_final_raw")
            raw_crude_dfs = []

if raw_crude_dfs:      
  batch_crude_df = unionAll(*raw_crude_dfs)
  insert_agg_df(batch_crude_df, db_output, "bbrb_final_raw")

# COMMAND ----------

# DBTITLE 1,Suppression
raw_insert_df = spark.table(f"{db_output}.bbrb_final_raw")

# de-duplicate tasks (same measure/breakdown can appear multiple times due to list building above)
seen = set()
unique_tasks = []
for t in supp_details:
    key = (t[0], t[1], t[2], t[3])  # suppression_type, breakdown_name, measure_id, numerator_id
    if key not in seen:
        seen.add(key)
        unique_tasks.append(t)

for suppression_type, breakdown_name, measure_id, numerator_id, measure_name in unique_tasks:
    print(f"{measure_id}: {breakdown_name}")

    if breakdown_name in unsup_breakdowns:
        supp_df = (
            raw_insert_df
            .filter(
                (F.col("MEASURE_ID") == measure_id) &
                (F.col("BREAKDOWN") == breakdown_name) &
                (F.col("REPORTING_PERIOD_END") == rp_enddate) &
                (F.col("STATUS") == status) &
                (F.col("SOURCE_DB") == db_source)
            )
        )
    else:
        supp_df = mhsds_suppression(
            raw_insert_df, suppression_type, breakdown_name,
            measure_id, rp_enddate, status, numerator_id, db_source
        )

    supp_df = (
        supp_df
        .withColumn("MEASURE_VALUE", F.coalesce(F.col("MEASURE_VALUE"), F.lit("_")))
        .select(*output_columns)
    )
    supp_dfs.append(supp_df)
    
    if len(supp_dfs) >= batch_size:
        batch_supp_df = unionAll(*supp_dfs)
        insert_agg_df(batch_supp_df, db_output, "bbrb_final_suppressed")
        supp_dfs = []

if supp_dfs:      
  batch_supp_df = unionAll(*supp_dfs)
  insert_agg_df(batch_supp_df, db_output, "bbrb_final_suppressed")

# COMMAND ----------

