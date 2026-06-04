# Databricks notebook source
# DBTITLE 1,Break down Values
 %sql
 TRUNCATE TABLE $db_output.cyp_ed_wt_breakdown_values;
 INSERT INTO $db_output.cyp_ed_wt_breakdown_values VALUES
   ('England'),
   ('CCG - GP Practice or Residence'),
   ('Provider'),
   ('STP - GP Practice or Residence'),
   ('Commissioning Region');


# COMMAND ----------

 %sql
 TRUNCATE TABLE $db_output.cyp_ed_wt_level_values_1;

 INSERT INTO $db_output.cyp_ed_wt_level_values_1
 SELECT 
   'England' as primary_level, 
   'England' as primary_level_desc,
   'NONE' as secondary_level,
   'NONE' as secondary_level_desc,
   'England' as breakdown
 UNION ALL
 SELECT DISTINCT
   ORG_CODE as primary_level, 
   NAME as primary_level_desc, 
   'NONE' as secondary_level,
   'NONE' as secondary_level_desc,
   'Provider' as breakdown 
  FROM $db_output.providers_between_rp_start_end_dates 
 UNION ALL
 SELECT DISTINCT
   $ccg_code_field as level, 
   COALESCE($ccg_desc_field, "UNKNOWN") as level_desc, 
   'NONE' as secondary_level,
   'NONE' as secondary_level_desc,
   'CCG - GP Practice or Residence' as breakdown 
 FROM $ccg_ref_table -- WARNING: The data in this view differs depending on each month rp_enddate
 UNION ALL
 SELECT distinct
   $stp_code_field as Level, 
   $stp_desc_field as level_desc, 
   'NONE' as secondary_level,
   'NONE' as secondary_level_desc,
   'STP - GP Practice or Residence' as breakdown
   from $stp_reg_ref_table
 UNION ALL
 SELECT distinct
   $reg_code_field as level, 
   $reg_desc_field as level_desc, 
   'NONE' as secondary_level,
   'NONE' as secondary_level_desc,
   'Commissioning Region' as breakdown
   from $stp_reg_ref_table

# COMMAND ----------

 %sql
 TRUNCATE TABLE $db_output.cyp_ed_wt_metric_values;
 INSERT INTO $db_output.cyp_ed_wt_metric_values VALUES 
 ('ED85', 'Referrals with eating disorder issues entering treatment in RP, aged 0-18'),
 ('ED86', 'Referrals with eating disorder issues categorised as urgent entering treatment in RP, aged 0-18'),
 ('ED86a', 'Referrals with eating disorder issues categorised as urgent entering treatment within one week, in RP, aged 0-18'),
 ('ED86b', 'Referrals with eating disorder issues categorised as urgent entering treatment within 1-4 weeks, in RP, aged 0-18'),
 ('ED86c', 'Referrals with eating disorder issues categorised as urgent entering treatment within 4-12 weeks, in RP, aged 0-18'),
 ('ED86d', 'Referrals with eating disorder issues categorised as urgent entering treatment after 12 weeks, in RP, aged 0-18'),
 ('ED86e', 'Proportion of referrals with eating disorders categorized as urgent cases entering treatment within one week in RP, aged 0-18'),
 ('ED87', 'Referrals eating disorder issues categorised as routine entering treatment in RP, aged 0-18'),
 ('ED87a', 'Referrals with eating disorder issues categorised as routine entering treatment within one week, in RP, aged 0-18'),
 ('ED87b', 'Referrals with eating disorder issues categorised as routine entering treatment within 1-4 weeks, in RP, aged 0-18'),
 ('ED87c', 'Referrals with eating disorder issues categorised as routine entering treatment within 4-12 weeks, in RP, aged 0-18'),
 ('ED87d', 'Referrals with eating disorder issues categorised as routine entering treatment after 12 weeks, in RP, aged 0-18'),
 ('ED87e', 'Proportion of referrals with eating disorders categorized as routine cases entering treatment within four weeks in RP, aged 0-18'),
 ('ED88', 'Referrals with eating disorder issues waiting for treatment at end of RP, aged 0-18'),
 ('ED89', 'Referrals with eating disorder issues categorized as urgent waiting for treatment end RP, aged 0-18'),
 ('ED89a', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for one week, end RP, aged 0-18'),
 ('ED89b', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for 1-4 weeks, end RP, aged 0-18'),
 ('ED89c', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for 4-12 weeks, end RP, aged 0-18'),
 ('ED89d', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for more than 12 weeks, end RP, aged 0-18'),
 ('ED90', 'Referrals with eating disorder issues categorized as routine waiting for treatment end RP, aged 0-18'),
 ('ED90a', 'Referrals with eating disorder issues categorized as routine waiting for treatment for one week, end RP, aged 0-18'),
 ('ED90b', 'Referrals with eating disorder issues categorized as routine waiting for treatment for 1-4 weeks, end RP, aged 0-18'),
 ('ED90c', 'Referrals with eating disorder issues categorized as routine waiting for treatment for 4-12 weeks, end RP, aged 0-18'),
 ('ED90d', 'Referrals with eating disorder issues categorized as routine waiting for treatment for more than 12 weeks, end RP, aged 0-18')  