# Databricks notebook source
 %py
 db_output=dbutils.widgets.get("db_output")
 print(db_output)
 assert db_output
 provider_table=dbutils.widgets.get("provider_table")
 print(provider_table)
 assert provider_table

# COMMAND ----------

# DBTITLE 1,Break down Values
 %sql
 TRUNCATE TABLE $db_output.cyp_ed_wt_breakdown_values;
 INSERT INTO $db_output.cyp_ed_wt_breakdown_values VALUES
   ('England'),
   ('England; Age'),
   ('England; Gender'),
   ('England; Ethnicity'),
   ('England; IMD Decile'),
   ('England; Intervention'),
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
   
 /* Age group breakdowns for England level only */
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '0 to 5' as secondary_level, '0 to 5' as secondary_level_desc, 'England; Age' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '6 to 10' as secondary_level, '6 to 10' as secondary_level_desc, 'England; Age' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '11 to 15' as secondary_level, '11 to 15' as secondary_level_desc, 'England; Age' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '16' as secondary_level, '16' as secondary_level_desc, 'England; Age' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '17' as secondary_level, '17' as secondary_level_desc, 'England; Age' as breakdown
   
 /* Gender breakdowns for England level only */
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '1' as secondary_level, 'Male (including trans man)' as secondary_level_desc, 
 'England; Gender' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '2' as secondary_level, 'Female (including trans woman)' as secondary_level_desc, 
 'England; Gender' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '3' as secondary_level, 'Non-binary' as secondary_level_desc, 'England; Gender' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '9' as secondary_level, 'Indeterminate (unable to be classified as either male or female)' as secondary_level_desc, 'England; Gender' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '4' as secondary_level, 'Other (not listed)' as secondary_level_desc, 
 'England; Gender' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'UNKNOWN' as secondary_level, 'UNKNOWN' as secondary_level_desc, 'England; Gender' as breakdown
   
 /* IMD Decile breakdowns for England level only */
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '01 Most deprived' as secondary_level, '01 Most deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '02 More deprived' as secondary_level, '02 More deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '03 More deprived' as secondary_level, '03 More deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '04 More deprived' as secondary_level, '04 More deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '05 More deprived' as secondary_level, '05 More deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '06 Less deprived' as secondary_level, '06 Less deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '07 Less deprived' as secondary_level, '07 Less deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '08 Less deprived' as secondary_level, '08 Less deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '09 Less deprived' as secondary_level, '09 Less deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, '10 Least deprived' as secondary_level, '10 Least deprived' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'UNKNOWN' as secondary_level, 'UNKNOWN' as secondary_level_desc, 
 'England; IMD Decile' as breakdown
   
 /* Interventions breakdowns for England level only */
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Family therapy' as secondary_level, 'Family therapy' as secondary_level_desc, 
 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Cognitive behavioural therapy for eating disorders (valid up to March 2026)' as secondary_level, 'Cognitive behavioural therapy for eating disorders (valid up to March 2026)'  as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Interpersonal psychotherapy' as secondary_level, 'Interpersonal psychotherapy' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Guided self-help cognitive behavioral therapy' as secondary_level, 'Guided self-help cognitive behavioral therapy' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Eating-disorder-focused focal psychodynamic therapy' as secondary_level, 'Eating-disorder-focused focal psychodynamic therapy' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Group cognitive behavioural therapy for eating disorder' as secondary_level, 'Group cognitive behavioural therapy for eating disorder' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Adolescent-focused psychotherapy for anorexia nervosa' as secondary_level, 'Adolescent-focused psychotherapy for anorexia nervosa' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Guided self-help for bulimia nervosa' as secondary_level, 'Guided self-help for bulimia nervosa' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Shared care' as secondary_level, 'Shared care' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Guided self help for bulimia nervosa and binge eating' as secondary_level, 'Guided self help for bulimia nervosa and binge eating' as secondary_level_desc, 'England; Intervention' as breakdown
 --OLD CODES, REMOVE IN APRIL 2027
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Cognitive behavioural therapy for eating disorders (valid up to March 2026)' as secondary_level, 'Cognitive behavioural therapy for eating disorders (valid up to March 2026)' as secondary_level_desc, 'England; Intervention' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Focal psychodynamic therapy (valid up to March 2026)' as secondary_level, 'Focal psychodynamic therapy (valid up to March 2026)' as secondary_level_desc, 'England; Intervention' as breakdown
   
 /* Ethnicity breakdowns for England level only */
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'White' as secondary_level, 'White' as secondary_level_desc, 'England; Ethnicity' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Mixed' as secondary_level, 'Mixed' as secondary_level_desc, 'England; Ethnicity' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Asian or Asian British' as secondary_level, 'Asian or Asian British' as secondary_level_desc, 'England; Ethnicity' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Black or Black British' as secondary_level, 'Black or Black British' as secondary_level_desc, 'England; Ethnicity' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Other Ethnic Groups' as secondary_level, 'Other Ethnic Groups' as secondary_level_desc, 'England; Ethnicity' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'Not Stated' as secondary_level, 'Not Stated' as secondary_level_desc, 'England; Ethnicity' as breakdown
 UNION ALL
 SELECT 'England' as primary_level, 'England' as primary_level_desc, 'UNKNOWN' as secondary_level, 'UNKNOWN' as secondary_level_desc, 'England; Ethnicity' as breakdown

 UNION ALL
 SELECT DISTINCT
   ORG_CODE as primary_level, 
   NAME as primary_level_desc, 
   'NONE' as secondary_level,
   'NONE' as secondary_level_desc,
   'Provider' as breakdown 
  FROM $provider_table
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
 ('ED85', 'Referrals with eating disorder issues entering treatment in RP, aged 0-17'),
 ('ED86', 'Referrals with eating disorder issues categorised as urgent entering treatment in RP, aged 0-17'),
 ('ED86a', 'Referrals with eating disorder issues categorised as urgent entering treatment within one week, in RP, aged 0-17'),
 ('ED86b', 'Referrals with eating disorder issues categorised as urgent entering treatment within 1-4 weeks, in RP, aged 0-17'),
 ('ED86c', 'Referrals with eating disorder issues categorised as urgent entering treatment within 4-12 weeks, in RP, aged 0-17'),
 ('ED86d', 'Referrals with eating disorder issues categorised as urgent entering treatment after 12 weeks, in RP, aged 0-17'),
 ('ED86e', 'Proportion of referrals with eating disorders categorized as urgent cases entering treatment within one week in RP, aged 0-17'),
 ('ED86f', 'Proportion of referrals with eating disorder issues categorised as urgent entering treatment within 1-4 weeks, in RP, aged 0-17'),
 ('ED86g', 'Proportion of referrals  with eating disorder issues categorised as urgent entering treatment within 4-12 weeks, in RP, aged 0-17'),
 ('ED86h', 'Proportion of referrals  with eating disorder issues categorised as urgent entering treatment after 12 weeks, in RP, aged 0-17'),
 ('ED87', 'Referrals eating disorder issues categorised as routine entering treatment in RP, aged 0-17'),
 ('ED87a', 'Referrals with eating disorder issues categorised as routine entering treatment within one week, in RP, aged 0-17'),
 ('ED87b', 'Referrals with eating disorder issues categorised as routine entering treatment within 1-4 weeks, in RP, aged 0-17'),
 ('ED87c', 'Referrals with eating disorder issues categorised as routine entering treatment within 4-12 weeks, in RP, aged 0-17'),
 ('ED87d', 'Referrals with eating disorder issues categorised as routine entering treatment after 12 weeks, in RP, aged 0-17'),
 ('ED87e', 'Proportion of referrals with eating disorders categorized as routine cases entering treatment within four weeks in RP, aged 0-17'),
 ('ED87f', 'Proportion of referrals with eating disorder issues categorised as routine entering treatment within one week, in RP, aged 0-17'),
 ('ED87g', 'Proportion of referrals with eating disorder issues categorised as routine entering treatment within 1-4 weeks, in RP, aged 0-17'),
 ('ED87h', 'Proportion of referrals with eating disorder issues categorised as routine entering treatment within 4-12 weeks, in RP, aged 0-17'),
 ('ED87i', 'Proportion of referrals with eating disorder issues categorised as routine entering treatment after 12 weeks, in RP, aged 0-17'),
 ('ED87j', 'Referrals with eating disorder issues categorised as routine entering treatment within 4 weeks, in RP, aged 0-17'),
 ('ED88', 'Referrals with eating disorder issues waiting for treatment at end of RP, aged 0-17'),
 ('ED89', 'Referrals with eating disorder issues categorized as urgent waiting for treatment end RP, aged 0-17'),
 ('ED89a', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for one week, end RP, aged 0-17'),
 ('ED89b', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for 1-4 weeks, end RP, aged 0-17'),
 ('ED89c', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for 4-12 weeks, end RP, aged 0-17'),
 ('ED89d', 'Referrals with eating disorder issues categorized as urgent waiting for treatment for more than 12 weeks, end RP, aged 0-17'),
 ('ED89e', 'Proportion of referrals with eating disorder issues categorized as urgent waiting for treatment for one week, end RP, aged 0-17'),
 ('ED89f', 'Proportion of referrals with eating disorder issues categorized as urgent waiting for treatment for 1-4 weeks, end RP, aged 0-17'),
 ('ED89g', 'Proportion of referrals with eating disorder issues categorized as urgent waiting for treatment for 4-12 weeks, end RP, aged 0-17'),
 ('ED89h', 'Proportion of referrals with eating disorder issues categorized as urgent waiting for treatment for more than 12 weeks, end RP, aged 0-17'),
 ('ED90', 'Referrals with eating disorder issues categorized as routine waiting for treatment end RP, aged 0-17'),
 ('ED90a', 'Referrals with eating disorder issues categorized as routine waiting for treatment for one week, end RP, aged 0-17'),
 ('ED90b', 'Referrals with eating disorder issues categorized as routine waiting for treatment for 1-4 weeks, end RP, aged 0-17'),
 ('ED90c', 'Referrals with eating disorder issues categorized as routine waiting for treatment for 4-12 weeks, end RP, aged 0-17'),
 ('ED90d', 'Referrals with eating disorder issues categorized as routine waiting for treatment for more than 12 weeks, end RP, aged 0-17'),
 ('ED90e', 'Proportion of referrals with eating disorder issues categorized as routine waiting for treatment for one week, end RP, aged 0-17'),
 ('ED90f', 'Proportion of referrals with eating disorder issues categorized as routine waiting for treatment for 1-4 weeks, end RP, aged 0-17'),
 ('ED90g', 'Proportion of referrals with eating disorder issues categorized as routine waiting for treatment for 4-12 weeks, end RP, aged 0-17'),
 ('ED90h', 'Proportion of referrals with eating disorder issues categorized as routine waiting for treatment for more than 12 weeks, end RP, aged 0-17'),
 ('ED91', 'Median waiting time between referral and first contact for referrals that had their first contact in the RP, with eating disorder issues categorized as routine, aged 0-17'),
 ('ED92', 'Median waiting time between referral and first contact for referrals that had their first contact in the RP, with eating disorder issues categorized as urgent, aged 0-17'),
 ('ED93', '90th percentile waiting time between referral and first contact for referrals that had their first contact in the RP, with eating disorder issues categorized as routine, aged 0-17'),
 ('ED94', '90th percentile waiting time between referral and first contact for referrals that had their first contact in the RP, with eating disorder issues categorized as urgent, aged 0-17'),
 ('ED95', 'Median waiting time for referrals still waiting for treatment, with eating disorder issues categorized as routine, aged 0-17'),
 ('ED96', 'Median waiting time referrals still waiting for treatment, with eating disorder issues categorized as urgent, aged 0-17'),
 ('ED97', '90th percentile waiting time for referrals still waiting for treatment, with eating disorder issues categorized as routine, aged 0-17'),
 ('ED98', '90th percentile waiting time referrals still waiting for treatment, with eating disorder issues categorized as urgent, aged 0-17'),
 ('ED99', 'Number of referrals recieving a second contact in the RP, with eating disorder issues categorized as routine, aged 0-17'),
 ('ED100', 'Number of referrals recieving a second contact in the RP, with eating disorder issues categorized as urgent, aged 0-17'),
 ('ED101', 'Median waiting time from first to second contact for referrals receiving a second contact in the RP, with eating disorder issues categorized as routine, aged 0-17'),
 ('ED102', 'Median waiting time from first to second contact for referrals receiving a second contact in the RP, with eating disorder issues categorized as urgent, aged 0-17'),
 ('ED103', '90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with eating disorder issues categorized as routine, aged 0-17'),
 ('ED104', '90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with eating disorder issues categorized as urgent, aged 0-17'),
 ('ED105', 'People with eating disorder issues still waiting for treatment at the end of the RP aged 18 or over'),
 ('ED106', 'Median waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP aged 18 or over'),
 ('ED107', '90th percentile waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP aged 18 or over')