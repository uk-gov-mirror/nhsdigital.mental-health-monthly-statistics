# Databricks notebook source
 %py
 db_output=dbutils.widgets.get("db_output")
 print(db_output)
 assert db_output
 month_id=dbutils.widgets.get("month_id")
 print(month_id)
 assert month_id
 db_source=dbutils.widgets.get("db_source")
 print(db_source)
 assert db_source
 rp_startdate=dbutils.widgets.get("rp_startdate")
 print(rp_startdate)
 assert rp_startdate
 rp_enddate=dbutils.widgets.get("rp_enddate")
 print(rp_enddate)
 assert rp_enddate

# COMMAND ----------

# DBTITLE 1,CYP_ED01 - ED85- National - Total referrals for children and young people with eating disorder entering treatment in RP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED85- National - Total CYP ED referrals entering treatment by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED85- National - Total CYP ED referrals entering treatment by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED85- National - Total CYP ED referrals entering treatment by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED85- National - Total CYP ED referrals entering treatment by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED85- National - Total CYP ED referrals entering treatment by intervention
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Intervention' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Intervention AS SECONDARY_LEVEL
        ,Intervention AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by Intervention, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01 - ED85 - Provider- Total referrals for children and young people with eating disorder entering treatment in RP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
  FROM $db_output.CYP_ED_WT_STEP4  step4
  WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
  group by step4.orgidprov, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01 - ED85 - CCG - Total referrals for children and young people with eating disorder entering treatment in RP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE($ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
  FROM $db_output.CYP_ED_WT_STEP4  step4
  left join $db_output.MHS001_CCG_LATEST ccg
  on step4.Person_ID = ccg.Person_ID
  WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
  group by ccg.$ccg_agg_field,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01 - ED85 - STP- Total referrals for children and young people with eating disorder entering treatment in RP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
  FROM $db_output.CYP_ED_WT_STEP4  step4
  left join $db_output.MHS001_CCG_LATEST ccg
  on step4.Person_ID = ccg.Person_ID
  left join $stp_reg_ref_table stp
  on ccg.$ccg_agg_field = stp.CCG_CODE
  WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
  group by stp.STP_CODE,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01 - ED85 - Region - Total referrals for children and young people with eating disorder entering treatment in RP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED85' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
  FROM $db_output.CYP_ED_WT_STEP4  step4
  left join $db_output.MHS001_CCG_LATEST ccg
  on step4.Person_ID = ccg.Person_ID
  left join $stp_reg_ref_table stp
  on ccg.$ccg_agg_field = stp.CCG_CODE
  WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
  group by stp.Region_code,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01a - ED86 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' as METRIC
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED86 National Urgent CYP ED referrals entering treatment by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED86 National Urgent CYP ED referrals entering treatment by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED86 National Urgent CYP ED referrals entering treatment by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED86 National Urgent CYP ED referrals entering treatment by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED86 National Urgent CYP ED referrals entering treatment by intervention
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Intervention' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Intervention AS SECONDARY_LEVEL
        ,Intervention AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' AS METRIC
        ,COUNT(DISTINCT UniqServReqID) METRIC_VALUE
        ,SOURCE_DB
   FROM $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
   WHERE UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
   group by Intervention, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01a - ED86 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' as METRIC
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by step4.orgidprov,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01a - ED86 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE($ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' as METRIC
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 FROM $db_output.CYP_ED_WT_STEP4   step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)


 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by $ccg_agg_field,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01a - ED86 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' as METRIC
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 FROM $db_output.CYP_ED_WT_STEP4   step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)


 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01a - ED86 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86' as METRIC
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 FROM $db_output.CYP_ED_WT_STEP4   step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)


 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, stp.Region_code

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - NATIONAL PREP
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01aa_ad_national_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED86a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED86b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED86c'
              WHEN  step4.waiting_time > 12 THEN 'ED86d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by UniqServReqID,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ae - ED86 - NATIONAL
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01aa_ad_national_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB


# COMMAND ----------

# DBTITLE 1,CYP_ED01aa - ED86a National breakdown by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86a' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and step4.waiting_time <= 1 
 group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa - ED86a National breakdown by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86a' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and step4.waiting_time <= 1 
 group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa - ED86a National breakdown by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86a' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and step4.waiting_time <= 1 
 group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa - ED86a National breakdown by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86a' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and step4.waiting_time <= 1 
 group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa - ED86a National breakdown by intervention
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Intervention' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Intervention AS SECONDARY_LEVEL
        ,Intervention AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED86a' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and step4.waiting_time <= 1 
 group by Intervention, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - Provider - PREP
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01aa_ad_provider_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED86a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED86b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED86c'
              WHEN  step4.waiting_time > 12 THEN 'ED86d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by OrgIDProv,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01aa_ad_provider_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - CCG - PREP
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01aa_ad_ccg_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE($ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED86a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED86b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED86c'
              WHEN  step4.waiting_time > 12 THEN 'ED86d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)


 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by $ccg_agg_field,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - CCG
 %sql
  INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01aa_ad_ccg_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB


# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - STP - PREP
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01aa_ad_stp_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED86a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED86b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED86c'
              WHEN  step4.waiting_time > 12 THEN 'ED86d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)


 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by STP_CODE,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01aa_ad_stp_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB


# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - Region - PREP
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01aa_ad_region_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED86a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED86b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED86c'
              WHEN  step4.waiting_time > 12 THEN 'ED86d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4  step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)


 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by metric,SOURCE_DB, stp.Region_code

# COMMAND ----------

# DBTITLE 1,CYP_ED01aa-CYP_ED01ad - ED86 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01aa_ad_region_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ae - ED86 - National
 %sql
 -- INSERT INTO $db_output.cyp_ed_wt_unformatted
 -- select 
 --        '$month_id' AS MONTH_ID
 --        ,'$status' AS STATUS
 --        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
 --        ,'$rp_enddate' AS REPORTING_PERIOD_END
 --        ,'England' AS BREAKDOWN
 --        ,'England' AS PRIMARY_LEVEL
 --        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
 --        ,'NONE' AS SECONDARY_LEVEL
 --        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
 --        ,'ED86e' METRIC 
 --        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 1 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
 --        ,SOURCE_DB
 -- from $db_output.CYP_ED_WT_STEP4  step4

 -- INNER JOIN $db_output.validcodes as vc
 -- ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 -- and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 -- where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source'
 -- group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ae - ED86 - Provider
 %sql
 -- INSERT INTO $db_output.cyp_ed_wt_unformatted
 -- select 
 --        '$month_id' AS MONTH_ID
 --        ,'$status' AS STATUS
 --        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
 --        ,'$rp_enddate' AS REPORTING_PERIOD_END
 --        ,'Provider' AS BREAKDOWN
 --        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
 --        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
 --        ,'NONE' AS SECONDARY_LEVEL
 --        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
 --        ,'ED86e' METRIC 
 --        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 1 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
 --        ,SOURCE_DB
 -- from $db_output.CYP_ED_WT_STEP4  step4

 -- INNER JOIN $db_output.validcodes as vc
 -- ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 -- and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 -- where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source'
 -- group by OrgIDProv,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ae - ED86 - CCG
 %sql
 -- INSERT INTO $db_output.cyp_ed_wt_unformatted
 -- select 
 --        '$month_id' AS MONTH_ID
 --        ,'$status' AS STATUS
 --        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
 --        ,'$rp_enddate' AS REPORTING_PERIOD_END
 --        ,'CCG - GP Practice or Residence' AS BREAKDOWN
 --        ,COALESCE($ccg_agg_field,NULL) AS PRIMARY_LEVEL
 --        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
 --        ,'NONE' AS SECONDARY_LEVEL
 --        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
 --        ,'ED86e' METRIC 
 --        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 1 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
 --        ,SOURCE_DB
 -- from $db_output.CYP_ED_WT_STEP4  step4

 -- INNER JOIN $db_output.validcodes as vc
 -- ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 -- and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)


 -- left join $db_output.MHS001_CCG_LATEST ccg
 -- on step4.Person_ID = ccg.Person_ID

 -- where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source'
 -- group by $ccg_agg_field,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ae - ED86 - STP
 %sql
 -- INSERT INTO $db_output.cyp_ed_wt_unformatted
 -- select 
 --        '$month_id' AS MONTH_ID
 --        ,'$status' AS STATUS
 --        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
 --        ,'$rp_enddate' AS REPORTING_PERIOD_END
 --        ,'STP - GP Practice or Residence' AS BREAKDOWN
 --        ,COALESCE(stp.STP_CODE,NULL) AS PRIMARY_LEVEL
 --        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
 --        ,'NONE' AS SECONDARY_LEVEL
 --        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
 --        ,'ED86e' METRIC 
 --        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 1 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
 --        ,SOURCE_DB
 -- from $db_output.CYP_ED_WT_STEP4  step4

 -- INNER JOIN $db_output.validcodes as vc
 -- ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 -- and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 -- left join $db_output.MHS001_CCG_LATEST ccg
 -- on step4.Person_ID = ccg.Person_ID
 -- left join $stp_reg_ref_table stp
 -- on ccg.$ccg_agg_field = stp.CCG_CODE

 -- where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source'
 -- group by STP_CODE,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ae - ED86 - Region
 %sql
 -- INSERT INTO $db_output.cyp_ed_wt_unformatted
 -- select 
 --        '$month_id' AS MONTH_ID
 --        ,'$status' AS STATUS
 --        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
 --        ,'$rp_enddate' AS REPORTING_PERIOD_END
 --        ,'Commissioning Region' AS BREAKDOWN
 --        ,COALESCE(stp.Region_code,NULL) AS PRIMARY_LEVEL
 --        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
 --        ,'NONE' AS SECONDARY_LEVEL
 --        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
 --        ,'ED86e' METRIC 
 --        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 1 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
 --        ,SOURCE_DB
 -- from $db_output.CYP_ED_WT_STEP4  step4

 -- INNER JOIN $db_output.validcodes as vc
 -- ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 -- and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 -- left join $db_output.MHS001_CCG_LATEST ccg
 -- on step4.Person_ID = ccg.Person_ID
 -- left join $stp_reg_ref_table stp
 -- on ccg.$ccg_agg_field = stp.CCG_CODE

 -- where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source'
 -- group by Region_code,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01b - ED87 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 where  UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED87 National routine CYP ED referrals entering treatment by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where  UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED87 National routine CYP ED referrals entering treatment by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where  UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED87 National routine CYP ED referrals entering treatment by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where  UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED87 National routine CYP ED referrals entering treatment by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where  UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,ED87 National routine CYP ED referrals entering treatment by intervention
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Intervention' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Intervention AS SECONDARY_LEVEL
        ,Intervention AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
 and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
  
 where  UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Intervention, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01b - ED87 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        , Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
   ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue 
   and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by OrgIDProv,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01b - ED87 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE($ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by $ccg_agg_field,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01b - ED87 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(STP_CODE,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by STP_CODE,metric,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01b - ED87 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87' as METRIC  
        ,count(distinct UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by metric,SOURCE_DB, stp.Region_code

# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - National - prep
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01ba_to_ED01bd_National_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED87a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED87b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED87c'
              WHEN  step4.waiting_time > 12 THEN 'ED87d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by UniqServReqID,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01ba_to_ED01bd_National_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB


# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - Provider- prep
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01ba_to_ED01bd_Provider_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION 
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED87a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED87b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED87c'
              WHEN  step4.waiting_time > 12 THEN 'ED87d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id'
 and Status = '$status'
  and SOURCE_DB = '$db_source'
  AND rp_startdate_run = '$rp_startdate_run'
 group by step4.orgidprov,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,UntitledCYP_ED01ba-CYP_ED01bd - ED87 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01ba_to_ED01bd_Provider_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB


# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - CCG - prep
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01ba_to_ED01bd_CCG_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE($ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED87a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED87b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED87c'
              WHEN  step4.waiting_time > 12 THEN 'ED87d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id'
 and Status = '$status'
  and SOURCE_DB = '$db_source'
  AND rp_startdate_run = '$rp_startdate_run'
 group by $ccg_agg_field,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01ba_to_ED01bd_CCG_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB


# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - STP - prep
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01ba_to_ED01bd_STP_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED87a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED87b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED87c'
              WHEN  step4.waiting_time > 12 THEN 'ED87d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01ba_to_ED01bd_STP_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB


# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - Region - prep
 %sql
 CREATE OR REPLACE GLOBAL TEMP VIEW agg_CYP_ED01ba_to_ED01bd_region_prep AS
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step4.waiting_time <= 1 THEN 'ED87a' 
              WHEN  step4.waiting_time > 1 AND step4.waiting_time <= 4 THEN 'ED87b'
              WHEN  step4.waiting_time > 4 AND step4.waiting_time <= 12 THEN 'ED87c'
              WHEN  step4.waiting_time > 12 THEN 'ED87d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by METRIC,SOURCE_DB, stp.Region_code

# COMMAND ----------

# DBTITLE 1,CYP_ED01ba-CYP_ED01bd - ED87 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT  MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,SUM(METRIC_VALUE) as METRIC_VALUE
        ,SOURCE_DB
 from global_temp.agg_CYP_ED01ba_to_ED01bd_region_prep
 group by MONTH_ID
        ,STATUS
        ,REPORTING_PERIOD_START
        ,REPORTING_PERIOD_END
        ,BREAKDOWN
        ,PRIMARY_LEVEL
        ,PRIMARY_LEVEL_DESCRIPTION
        ,SECONDARY_LEVEL
        ,SECONDARY_LEVEL_DESCRIPTION
        ,METRIC
        ,METRIC_VALUE
        ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01be - ED87 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87e' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01be - ED87 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87e' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by step4.orgidprov,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01be - ED87 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87e' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by ccg.$ccg_agg_field,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01be - ED87 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87e' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01be - ED87 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87e' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) / CAST(COUNT(DISTINCT UniqServReqID) AS FLOAT)*100 AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.Region_code,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87j - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87j - National by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87j - National by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87j - National by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87j - National by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87j - National by intervention
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Intervention' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Intervention AS SECONDARY_LEVEL
        ,Intervention AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Intervention, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by step4.orgidprov,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)

 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by ccg.$ccg_agg_field,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED01j - ED87 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED87j' AS METRIC
        ,CAST(COUNT(DISTINCT CASE WHEN waiting_time <= 4 THEN UniqServReqID END) AS FLOAT) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step4.ClinRespPriorityType = vc.ValidValue and step4.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step4.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step4.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.Region_code,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - National by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - National by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - National by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - National by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by step6.orgidprov,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by ccg.$ccg_agg_field,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(stp_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02 - ED88 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,Coalesce(Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED88' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.Region_code,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - National by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6 
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - National by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6 
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - National by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6 
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - National by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6 
  
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by step6.orgidprov,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)

 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by ccg.$ccg_agg_field,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(stp_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02a - ED89 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,Coalesce(Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED89' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.Region_code, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02aa_to_ED02ad - ED89 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England'
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
         ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED89a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED89b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED89c'
              WHEN  step6.waiting_time > 12 THEN 'ED89d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
  
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02aa_to_ED02ad - ED89 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
         ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED89a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED89b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED89c'
              WHEN  step6.waiting_time > 12 THEN 'ED89d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by step6.orgidprov,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02aa_to_ED02ad - ED89 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
         ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED89a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED89b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED89c'
              WHEN  step6.waiting_time > 12 THEN 'ED89d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)

 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by ccg.$ccg_agg_field,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02aa_to_ED02ad - ED89 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(stp_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
         ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED89a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED89b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED89c'
              WHEN  step6.waiting_time > 12 THEN 'ED89d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)

 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE, METRIC ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02aa_to_ED02ad - ED89 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,Coalesce(Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
         ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED89a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED89b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED89c'
              WHEN  step6.waiting_time > 12 THEN 'ED89d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6  step6 

 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED86_89' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue 
 and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)

 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.Region_code, METRIC ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - National by age group
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Age' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Age_Group AS SECONDARY_LEVEL
        ,Age_Group AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Age_Group, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - National by gender
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Gender' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,Gender AS SECONDARY_LEVEL
        ,GenderDesc AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by Gender, GenderDesc, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - National by ethnicity
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; Ethnicity' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,EthnicityHigher AS SECONDARY_LEVEL
        ,EthnicityHigher AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by EthnicityHigher, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - National by IMD decile
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England; IMD Decile' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,IMD_Decile AS SECONDARY_LEVEL
        ,IMD_Decile AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by IMD_Decile, SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and ClinRespPriorityType = 3
 group by step6.orgidprov,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by ccg.$ccg_agg_field,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(stp_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE, METRIC ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02b - ED90 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,Coalesce(Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED90' AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.Region_code, METRIC ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02ba_to_ED02bd - ED90 - National
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England'
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED90a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED90b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED90c'
              WHEN  step6.waiting_time > 12 THEN 'ED90d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02ba_to_ED02bd - ED90 - Provider
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED90a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED90b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED90c'
              WHEN  step6.waiting_time > 12 THEN 'ED90d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by step6.orgidprov,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02ba_to_ED02bd - ED90 - CCG
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED90a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED90b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED90c'
              WHEN  step6.waiting_time > 12 THEN 'ED90d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by ccg.$ccg_agg_field,METRIC,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02ba_to_ED02bd - ED90 - STP
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(stp_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
  ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED90a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED90b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED90c'
              WHEN  step6.waiting_time > 12 THEN 'ED90d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.STP_CODE, METRIC ,SOURCE_DB

# COMMAND ----------

# DBTITLE 1,CYP_ED02ba_to_ED02bd - ED90 - Region
 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,Coalesce(Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
  ,(CASE WHEN  step6.waiting_time <= 1 THEN 'ED90a' 
              WHEN  step6.waiting_time > 1 AND step6.waiting_time <= 4 THEN 'ED90b'
              WHEN  step6.waiting_time > 4 AND step6.waiting_time <= 12 THEN 'ED90c'
              WHEN  step6.waiting_time > 12 THEN 'ED90d' END) AS METRIC
        ,count(distinct UniqServReqID) AS METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 step6
 INNER JOIN $db_output.validcodes as vc
 ON vc.tablename = 'mhs101referral' and vc.field = 'ClinRespPriorityType' and vc.Measure = 'ED87_90' and vc.type = 'include' and step6.ClinRespPriorityType = vc.ValidValue and step6.SubmissionMonthID >= vc.FirstMonth and (vc.LastMonth is null or step6.SubmissionMonthID <= vc.LastMonth)
 left join $db_output.MHS001_CCG_LATEST ccg
 on step6.Person_ID = ccg.Person_ID
 left join $stp_reg_ref_table stp
 on ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by stp.Region_code, METRIC ,SOURCE_DB

# COMMAND ----------

 %sql
 INSERT INTO $db_output.cyp_ed_wt_unformatted
 SELECT 
 NUM.MONTH_ID, 
 NUM.STATUS, 
 NUM.REPORTING_PERIOD_START,
 NUM.REPORTING_PERIOD_END,
 NUM.BREAKDOWN,
 NUM.PRIMARY_LEVEL,
 NUM.PRIMARY_LEVEL_DESCRIPTION,
 NUM.SECONDARY_LEVEL,
 NUM.SECONDARY_LEVEL_DESCRIPTION,
 CASE
   WHEN NUM.METRIC = 'ED86a' THEN 'ED86e'
   WHEN NUM.METRIC = 'ED86b' THEN 'ED86f'
   WHEN NUM.METRIC = 'ED86c' THEN 'ED86g'
   WHEN NUM.METRIC = 'ED86d' THEN 'ED86h'
   WHEN NUM.METRIC = 'ED87a' THEN 'ED87f' --ED87e is calculated separately as it includes those waiting less than a week and between 1 and 4 weeks
   WHEN NUM.METRIC = 'ED87j' THEN 'ED87e' --ED87e now calculated here as ED87j includes those waiting less than 4 weeks
   WHEN NUM.METRIC = 'ED87b' THEN 'ED87g'
   WHEN NUM.METRIC = 'ED87c' THEN 'ED87h'
   WHEN NUM.METRIC = 'ED87d' THEN 'ED87i'
   WHEN NUM.METRIC = 'ED89a' THEN 'ED89e'
   WHEN NUM.METRIC = 'ED89b' THEN 'ED89f'
   WHEN NUM.METRIC = 'ED89c' THEN 'ED89g'
   WHEN NUM.METRIC = 'ED89d' THEN 'ED89h'
   WHEN NUM.METRIC = 'ED90a' THEN 'ED90e'
   WHEN NUM.METRIC = 'ED90b' THEN 'ED90f'
   WHEN NUM.METRIC = 'ED90c' THEN 'ED90g'
   WHEN NUM.METRIC = 'ED90d' THEN 'ED90h'
   END AS METRIC,
 (CAST(NUM.METRIC_VALUE AS FLOAT) / CAST(DEN.METRIC_VALUE AS FLOAT))*100 AS METRIC_VALUE,
 NUM.SOURCE_DB
 FROM
 $db_output.cyp_ed_wt_unformatted NUM
 INNER JOIN $db_output.cyp_ed_wt_unformatted DEN
   ON NUM.REPORTING_PERIOD_START = DEN.REPORTING_PERIOD_START AND NUM.REPORTING_PERIOD_END = DEN.REPORTING_PERIOD_END AND NUM.STATUS = DEN.STATUS AND NUM.BREAKDOWN = DEN.BREAKDOWN AND NUM.PRIMARY_LEVEL = DEN.PRIMARY_LEVEL AND NUM.SECONDARY_LEVEL = DEN.SECONDARY_LEVEL AND NUM.SOURCE_DB = DEN.SOURCE_DB
   AND (
         (NUM.METRIC = 'ED86a' and DEN.METRIC = 'ED86') OR
         (NUM.METRIC = 'ED86b' and DEN.METRIC = 'ED86') OR
         (NUM.METRIC = 'ED86c' and DEN.METRIC = 'ED86') OR
         (NUM.METRIC = 'ED86d' and DEN.METRIC = 'ED86') OR
         (NUM.METRIC = 'ED87a' and DEN.METRIC = 'ED87') OR
         (NUM.METRIC = 'ED87b' and DEN.METRIC = 'ED87') OR
         (NUM.METRIC = 'ED87c' and DEN.METRIC = 'ED87') OR
         (NUM.METRIC = 'ED87d' and DEN.METRIC = 'ED87') OR
         (NUM.METRIC = 'ED87j' and DEN.METRIC = 'ED87') OR
         (NUM.METRIC = 'ED89a' and DEN.METRIC = 'ED89') OR
         (NUM.METRIC = 'ED89b' and DEN.METRIC = 'ED89') OR
         (NUM.METRIC = 'ED89c' and DEN.METRIC = 'ED89') OR
         (NUM.METRIC = 'ED89d' and DEN.METRIC = 'ED89') OR
         (NUM.METRIC = 'ED90a' and DEN.METRIC = 'ED90') OR
         (NUM.METRIC = 'ED90b' and DEN.METRIC = 'ED90') OR
         (NUM.METRIC = 'ED90c' and DEN.METRIC = 'ED90') OR
         (NUM.METRIC = 'ED90d' and DEN.METRIC = 'ED90') )

# COMMAND ----------

# DBTITLE 1,ED91 & ED92 - National
 %sql
 -- ED91 Median waiting time between referral and first contact, first contact in the RP, routine
 -- ED92 Median waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED91'
              WHEN Priority_Type = 'Urgent' THEN 'ED92'
              END AS METRIC
         ,PERCENTILE(waiting_time_days, 0.5)
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 as step4
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, METRIC

# COMMAND ----------

# DBTITLE 1,ED91 & ED92 - Provider
 %sql
 -- ED91 Median waiting time between referral and first contact, first contact in the RP, routine
 -- ED92 Median waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED91'
              WHEN Priority_Type = 'Urgent' THEN 'ED92'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by orgidprov,SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED91 & ED92 - CCG (sub-ICB)
 %sql
 -- ED91 Median waiting time between referral and first contact, first contact in the RP, routine
 -- ED92 Median waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED91'
              WHEN Priority_Type = 'Urgent' THEN 'ED92'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step4.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by ccg.$ccg_agg_field, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED91 & ED92 - STP (ICB)
 %sql
 -- ED91 Median waiting time between referral and first contact, first contact in the RP, routine
 -- ED92 Median waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(stp.STP_Code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED91'
              WHEN Priority_Type = 'Urgent' THEN 'ED92'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step4.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE 

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.STP_CODE, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED91 & ED92 - Region
 %sql
 -- ED91 Median waiting time between referral and first contact, first contact in the RP, routine
 -- ED92 Median waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,Coalesce(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED91'
              WHEN Priority_Type = 'Urgent' THEN 'ED92'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step4.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE 

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.Region_code, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED93 & ED94 - National
 %sql
 -- ED93: 90th percentile waiting time between referral and first contact, first contact in the RP, routine
 -- ED94: 90th percentile waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED93'
              WHEN Priority_Type = 'Urgent' THEN 'ED94'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, METRIC

# COMMAND ----------

# DBTITLE 1,ED93 & ED94 - Provider
 %sql
 -- ED93: 90th percentile waiting time between referral and first contact, first contact in the RP, routine
 -- ED94: 90th percentile waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,Coalesce(OrgIDProv,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED93'
              WHEN Priority_Type = 'Urgent' THEN 'ED94'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by orgidprov,SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED93 & ED94 - CCG (sub-ICB)
 %sql
 -- ED93: 90th percentile waiting time between referral and first contact, first contact in the RP, routine
 -- ED94: 90th percentile waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(ccg.$ccg_agg_field,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED93'
              WHEN Priority_Type = 'Urgent' THEN 'ED94'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP4 step4

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step4.Person_ID = ccg.Person_ID

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by ccg.$ccg_agg_field, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED93 & ED94 - STP (ICB)
 %sql
 -- ED93: 90th percentile waiting time between referral and first contact, first contact in the RP, routine
 -- ED94: 90th percentile waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,Coalesce(stp.STP_Code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED93'
              WHEN Priority_Type = 'Urgent' THEN 'ED94'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_step4 step4

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step4.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE 

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.STP_CODE, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED93 & ED94 - Region
 %sql
 -- ED93: 90th percentile waiting time between referral and first contact, first contact in the RP, routine
 -- ED94: 90th percentile waiting time between referral and first contact, first contact in the RP, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,Coalesce(stp.Region_code,NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED93'
              WHEN Priority_Type = 'Urgent' THEN 'ED94'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_step4 step4

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step4.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE 

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.Region_code, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED95 & ED96 - National
 %sql
 --ED95: median days waiting for those still waiting for treatment, routine
 --ED96: median days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED95'
              WHEN Priority_Type = 'Urgent' THEN 'ED96'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED95 & ED96 - Provider
 %sql
 --ED95: median days waiting for those still waiting for treatment, routine
 --ED96: median days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED95'
              WHEN Priority_Type = 'Urgent' THEN 'ED96'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by OrgIDProv, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED95 & ED96 - CCG (sub-ICB)
 %sql
 --ED95: median days waiting for those still waiting for treatment, routine
 --ED96: median days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED95'
              WHEN Priority_Type = 'Urgent' THEN 'ED96'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 as step6
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step6.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by ccg.$ccg_agg_field, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED95 & ED96 - STP (ICB)
 %sql
 --ED95: median days waiting for those still waiting for treatment, routine
 --ED96: median days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
       ,CASE WHEN Priority_Type = 'Routine' THEN 'ED95'
              WHEN Priority_Type = 'Urgent' THEN 'ED96'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 as step6
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step6.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.STP_CODE, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED95 & ED96 - Region
 %sql
 --ED95: median days waiting for those still waiting for treatment, routine
 --ED96: median days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
       ,CASE WHEN Priority_Type = 'Routine' THEN 'ED95'
              WHEN Priority_Type = 'Urgent' THEN 'ED96'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 as step6
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step6.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.Region_code, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED97 & ED98 - National
 %sql
 --ED97: 90th percentile days waiting for those still waiting for treatment, routine
 --ED98: 90th percentile days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED97'
              WHEN Priority_Type = 'Urgent' THEN 'ED98'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED97 & ED98 - Provider
 %sql
 --ED97: 90th percentile days waiting for those still waiting for treatment, routine
 --ED98: 90th percentile days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED97'
              WHEN Priority_Type = 'Urgent' THEN 'ED98'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by OrgIDProv, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED97 & ED98 - CCG (sub-ICB)
 %sql
 --ED97: 90th percentile days waiting for those still waiting for treatment, routine
 --ED98: 90th percentile days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED97'
              WHEN Priority_Type = 'Urgent' THEN 'ED98'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 as step6
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step6.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by ccg.$ccg_agg_field, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED97 & ED98 - STP (ICB)
 %sql
 --ED97: 90th percentile days waiting for those still waiting for treatment, routine
 --ED98: 90th percentile days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED97'
              WHEN Priority_Type = 'Urgent' THEN 'ED98'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 as step6
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step6.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.STP_CODE, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED97 & ED98 - Region
 %sql
 --ED97: 90th percentile days waiting for those still waiting for treatment, routine
 --ED98: 90th percentile days waiting for those still waiting for treatment, urgent

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED97'
              WHEN Priority_Type = 'Urgent' THEN 'ED98'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP6 as step6
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step6.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by stp.Region_code, SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED99 & ED100 - National
 %sql
 --ED99: Number of referrals recieving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED100: Number of referrals recieving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED99'
              WHEN Priority_Type = 'Urgent' THEN 'ED100'
              END AS METRIC
        ,COUNT(DISTINCT UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED99 & ED100 - Provider
 %sql
 --ED99: Number of referrals recieving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED100: Number of referrals recieving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED99'
              WHEN Priority_Type = 'Urgent' THEN 'ED100'
              END AS METRIC
        ,COUNT(DISTINCT UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, OrgIDProv, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED99 & ED100 - CCG (sub-ICB)
 %sql
 --ED99: Number of referrals recieving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED100: Number of referrals recieving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED99'
              WHEN Priority_Type = 'Urgent' THEN 'ED100'
              END AS METRIC
        ,COUNT(DISTINCT UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, ccg.$ccg_agg_field, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED99 & ED100 - STP (ICB)
 %sql
 --ED99: Number of referrals recieving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED100: Number of referrals recieving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED99'
              WHEN Priority_Type = 'Urgent' THEN 'ED100'
              END AS METRIC
        ,COUNT(DISTINCT UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, stp.STP_CODE, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED99 & ED100 - Region
 %sql
 --ED99: Number of referrals recieving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED100: Number of referrals recieving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED99'
              WHEN Priority_Type = 'Urgent' THEN 'ED100'
              END AS METRIC
        ,COUNT(DISTINCT UniqServReqID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, stp.Region_code, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED101 & ED102 - National
 %sql
 --ED101: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED102: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED101'
              WHEN Priority_Type = 'Urgent' THEN 'ED102'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED101 & ED102 - Provider
 %sql
 --ED101: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED102: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED101'
              WHEN Priority_Type = 'Urgent' THEN 'ED102'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, OrgIDProv, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED101 & ED102 - CCG (sub-ICB)
 %sql
 --ED101: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED102: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED101'
              WHEN Priority_Type = 'Urgent' THEN 'ED102'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, ccg.$ccg_agg_field, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED101 & ED102 - STP (ICB)
 %sql
 --ED101: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED102: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED101'
              WHEN Priority_Type = 'Urgent' THEN 'ED102'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, stp.STP_CODE, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED101 & ED102 - Region
 %sql
 --ED101: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED102: Median waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED101'
              WHEN Priority_Type = 'Urgent' THEN 'ED102'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, stp.Region_code, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED103 & ED104 - National
 %sql
 --ED103: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED104: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED103'
              WHEN Priority_Type = 'Urgent' THEN 'ED104'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED103 & ED104 - Provider
 %sql
 --ED103: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED104: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED103'
              WHEN Priority_Type = 'Urgent' THEN 'ED104'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, OrgIDProv, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED103 & ED104 - CCG (sub-ICB)
 %sql
 --ED103: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED104: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED103'
              WHEN Priority_Type = 'Urgent' THEN 'ED104'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, ccg.$ccg_agg_field, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED103 & ED104 - STP (ICB)
 %sql
 --ED103: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED104: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED103'
              WHEN Priority_Type = 'Urgent' THEN 'ED104'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, stp.STP_CODE, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED103 & ED104 - Region
 %sql
 --ED103: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as routine, aged 0-18
 --ED104: 90th percentile waiting time from first to second contact for referrals receiving a second contact in the RP, with ED, categorized as urgent, aged 0-18

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,CASE WHEN Priority_Type = 'Routine' THEN 'ED103'
              WHEN Priority_Type = 'Urgent' THEN 'ED104'
              END AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP8 as step8

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step8.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 and Priority_Type IS NOT NULL
 group by SOURCE_DB, stp.Region_code, METRIC
 order by PRIMARY_LEVEL, METRIC

# COMMAND ----------

# DBTITLE 1,ED105 - National
 %sql
 --ED105: People with eating disorder issues but still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED105' AS METRIC
        ,COUNT(distinct Person_ID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP9 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED105 - Provider
 %sql
 --ED105: People with eating disorder issues but still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED105' AS METRIC
        ,COUNT(distinct Person_ID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP9 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, OrgIDProv
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED105 - CCG (subICB)
 %sql
 --ED105: People with eating disorder issues but still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED105' AS METRIC
        ,COUNT(distinct step9.Person_ID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP9 as step9
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step9.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, ccg.$ccg_agg_field
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED105 - STP (ICB)
 %sql
 --ED105: People with eating disorder issues but still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED105' AS METRIC
        ,COUNT(distinct step9.Person_ID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP9 as step9

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step9.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, stp.STP_CODE 
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED105 - Region
 %sql
 --ED105: People with eating disorder issues but still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED105' AS METRIC
        ,COUNT(distinct step9.Person_ID) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP9 as step9

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step9.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, stp.Region_code
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED106 - National
 %sql
 --ED106: Median waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED106' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED106 - Provider
 %sql
 --ED106: Median waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED106' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source'
 group by SOURCE_DB, OrgIDProv
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED106 - CCG (sub-ICB)
 %sql
 --ED106: Median waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED106' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 as step10
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step10.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, ccg.$ccg_agg_field
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED106 - STP (ICB)
 %sql
 --ED106: Median waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED106' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 as step10

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step10.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, stp.STP_CODE
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED106 - Region
 %sql
 --ED106: Median waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED106' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.5) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 as step10

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step10.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, stp.Region_code
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED107 - National
 %sql
 --ED107: 90th percentile waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'England' AS BREAKDOWN
        ,'England' AS PRIMARY_LEVEL
        ,'England' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED107' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED107 - Provider
 %sql
 --ED107: 90th percentile waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Provider' AS BREAKDOWN
        ,COALESCE(OrgIDProv, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED107' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, OrgIDProv
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED107 - CCG (sub-ICB)
 %sql
 --ED107: 90th percentile waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'CCG - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(ccg.$ccg_agg_field, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED107' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 as step10
 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step10.Person_ID = ccg.Person_ID
 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, ccg.$ccg_agg_field
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED107 - STP (ICB)
 %sql
 --ED107: 90th percentile waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'STP - GP Practice or Residence' AS BREAKDOWN
        ,COALESCE(stp.STP_CODE, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED107' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 as step10

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step10.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, stp.STP_CODE
 order by PRIMARY_LEVEL

# COMMAND ----------

# DBTITLE 1,ED107 - Region
 %sql
 --ED107: 90th percentile waiting time of referrals with eating disorder issues still waiting for treatment at the end of the RP that turned 18 and are no longer in scope

 INSERT INTO $db_output.cyp_ed_wt_unformatted
 select 
        '$month_id' AS MONTH_ID
        ,'$status' AS STATUS
        ,'$rp_startdate_run' AS REPORTING_PERIOD_START
        ,'$rp_enddate' AS REPORTING_PERIOD_END
        ,'Commissioning Region' AS BREAKDOWN
        ,COALESCE(stp.Region_code, NULL) AS PRIMARY_LEVEL
        ,'NONE' AS PRIMARY_LEVEL_DESCRIPTION
        ,'NONE' AS SECONDARY_LEVEL
        ,'NONE' AS SECONDARY_LEVEL_DESCRIPTION
        ,'ED107' AS METRIC
        ,PERCENTILE(waiting_time_days, 0.9) as METRIC_VALUE
        ,SOURCE_DB
 from $db_output.CYP_ED_WT_STEP10 as step10

 LEFT JOIN $db_output.MHS001_CCG_LATEST ccg ON step10.Person_ID = ccg.Person_ID
 LEFT JOIN $stp_reg_ref_table stp ON ccg.$ccg_agg_field = stp.CCG_CODE

 where UniqMonthID = '$month_id' AND Status = '$status' and SOURCE_DB = '$db_source' AND rp_startdate_run = '$rp_startdate_run'
 group by SOURCE_DB, stp.Region_code
 order by PRIMARY_LEVEL