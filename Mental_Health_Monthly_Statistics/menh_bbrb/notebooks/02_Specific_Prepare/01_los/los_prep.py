# Databricks notebook source
# dbutils.widgets.text("db_output", "personal_db")
# db_output = dbutils.widgets.get("db_output")
# dbutils.widgets.text("db_source", "testdata_menh_bbrb_mhsds_database")
# db_source = dbutils.widgets.get("db_source")
# dbutils.widgets.text("end_month_id", "1459")
# end_month_id = dbutils.widgets.get("end_month_id")
# dbutils.widgets.text("rp_startdate_qtr", "2021-08-01")
# rp_startdate_qtr = dbutils.widgets.get("rp_startdate_qtr")
# dbutils.widgets.text("rp_enddate", "2021-10-31")
# rp_enddate = dbutils.widgets.get("rp_enddate")

# COMMAND ----------

db_output = dbutils.widgets.get("db_output")
db_source = dbutils.widgets.get("db_source")
end_month_id = dbutils.widgets.get("end_month_id")
rp_startdate_qtr = dbutils.widgets.get("rp_startdate_qtr")
rp_enddate = dbutils.widgets.get("rp_enddate")

# COMMAND ----------

spark.sql(f"DROP TABLE IF EXISTS {db_output}.spells1")
if int(end_month_id) > 1467:
  spark.sql(f"""
             CREATE TABLE {db_output}.spells1
 
              SELECT 
 
              A.PERSON_ID, 
              A.UniqMonthID,
              A.UniqHospProvSpellID,
              A.OrgIDProv,
              E.NAME AS PROV_NAME,
              A.StartDateHospProvSpell,
              A.DischDateHospProvSpell,
              DATEDIFF(A.DischDateHospProvSpell, A.StartDateHospProvSpell) as HOSP_LOS,
              B.UniqWardStayID,
              B.MHAdmittedPatientClass,
              B.StartDateWardStay,
              B.EndDateWardStay,
              DATEDIFF(B.EndDateWardStay, B.StartDateWardStay) as WARD_LOS,
              C.AgeRepPeriodEnd,
              ccg.SubICBGPRes AS IC_REC_GP_RES,
              ccg.SubICBGPRes_Mapped AS IC_REC_GP_RES_MAPPED
 
              FROM
              {db_source}.MHS501HospProvSpell a 
              LEFT JOIN {db_source}.MHS502WARDSTAY B on a.UniqHospProvSpellID = b.UniqHospProvSpellID and a.Recordnumber = b.RecordNumber and b.EndDateWardStay = a.DischDateHospProvSpell
              LEFT JOIN {db_source}.MHS001MPI C ON A.RECORDNUMBER = C.RECORDNUMBER
              LEFT JOIN {db_output}.bbrb_org_daily_latest E ON A.ORGIDPROV = E.ORG_CODE
              LEFT JOIN {db_output}.bbrb_ccg_in_quarter ccg ON C.Person_ID = ccg.Person_ID
 
 
              WHERE
              (a.RECORDENDDATE IS NULL OR a.RECORDENDDATE > '{rp_enddate}')
              AND a.RECORDSTARTDATE BETWEEN '{rp_startdate_qtr}' AND '{rp_enddate}'
              AND A.DischDateHospProvSpell BETWEEN '{rp_startdate_qtr}' AND '{rp_enddate}'
             """)
else:
  spark.sql(f"""
             CREATE TABLE {db_output}.spells1
 
              SELECT 
 
              A.PERSON_ID, 
              A.UniqMonthID,
              A.UniqHospProvSpellID,
              A.OrgIDProv,
              E.NAME AS PROV_NAME,
              A.StartDateHospProvSpell,
              A.DischDateHospProvSpell,
              DATEDIFF(A.DischDateHospProvSpell, A.StartDateHospProvSpell) as HOSP_LOS,
              B.UniqWardStayID,
              B.MHAdmittedPatientClass,
              B.StartDateWardStay,
              B.EndDateWardStay,
              DATEDIFF(B.EndDateWardStay, B.StartDateWardStay) as WARD_LOS,
              C.AgeRepPeriodEnd,
              ccg.SubICBGPRes AS IC_REC_GP_RES,
              ccg.SubICBGPRes_Mapped AS IC_REC_GP_RES_MAPPED
 
              FROM
              {db_source}.MHS501HospProvSpell a 
              LEFT JOIN {db_source}.MHS502WARDSTAY B on a.UniqHospProvSpellID = b.UniqHospProvSpellID and a.Recordnumber = b.RecordNumber
              LEFT JOIN {db_source}.MHS001MPI C ON A.RECORDNUMBER = C.RECORDNUMBER
              LEFT JOIN {db_output}.bbrb_org_daily_latest E ON A.ORGIDPROV = E.ORG_CODE 
              LEFT JOIN {db_output}.bbrb_ccg_in_quarter ccg ON C.Person_ID = ccg.Person_ID
 
              WHERE
              (a.RECORDENDDATE IS NULL OR a.RECORDENDDATE > '{rp_enddate}') AND a.RECORDSTARTDATE BETWEEN '{rp_startdate_qtr}' AND '{rp_enddate}'
              AND A.DischDateHospProvSpell BETWEEN '{rp_startdate_qtr}' AND '{rp_enddate}'
             """)

# COMMAND ----------

 %sql
 ----this step needs to be done to bin invalid/expired ccg/sub-icb codes into UNKNOWN
 INSERT OVERWRITE TABLE $db_output.spells 
 SELECT DISTINCT
 A.PERSON_ID as Person_ID, 
 A.UniqHospProvSpellID,
 A.OrgIDProv,
 A.PROV_NAME as Provider_Name,
 A.StartDateHospProvSpell,
 A.DischDateHospProvSpell,
 A.HOSP_LOS as Hosp_LOS,
 A.UniqWardStayID,
 A.MHAdmittedPatientClass,
 A.StartDateWardStay,
 A.EndDateWardStay,
 A.WARD_LOS as Ward_LOS,
 A.AgeRepPeriodEnd,
 COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') AS CCG_Code,
 COALESCE(stp.CCG_Name, co.CCG_Name,'UNKNOWN') AS CCG_Name,
 COALESCE(stp.Region_Code, co.Region_Code,'UNKNOWN') AS Region_Code,
 COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') AS Region_Name,
 COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') AS STP_Code,
 COALESCE(stp.STP_Name, co.STP_Name,'UNKNOWN') AS STP_Name,
 CASE WHEN (A.UniqMonthID > 1488 AND A.MHAdmittedPatientClass = '200') OR (A.UniqMonthID <= 1488 AND A.MHAdmittedPatientClass = '10') THEN 'Adult Acute'
      WHEN (A.UniqMonthID > 1488 AND A.MHAdmittedPatientClass = '201') OR (A.UniqMonthID <= 1488 AND A.MHAdmittedPatientClass = '11') THEN 'Older Adult Acute'
      WHEN (A.UniqMonthID > 1488 AND A.MHAdmittedPatientClass = '202') OR (A.UniqMonthID <= 1488 AND A.MHAdmittedPatientClass = '12') THEN 'PICU'
      ELSE 'Invalid' END AS Acute_Bed
  
 FROM $db_output.spells1 A
 LEFT JOIN $db_output.bbrb_stp_mapping stp on A.IC_REC_GP_RES = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.commissioning_org_mapping co ON A.IC_REC_GP_RES_MAPPED = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'

# COMMAND ----------

 %sql
 OPTIMIZE $db_output.spells

# COMMAND ----------

 %sql
 ----this step needs to be done to bin invalid/expired ccg/sub-icb codes into UNKNOWN - also need to only include 1 item per row so only latest Acute_Bed day is used for subsetting
 INSERT OVERWRITE TABLE $db_output.distinct_spells_filter 
 SELECT
 a.Person_ID, 
 a.UniqHospProvSpellID,
 a.OrgIDProv,
 Provider_Name,
 StartDateHospProvSpell,
 DischDateHospProvSpell,
 Hosp_LOS,
 AgeRepPeriodEnd,
 CCG_Code,
 CCG_Name,
 REGION_CODE,
 REGION_Name,
 STP_CODE,
 STP_Name,
 Acute_Bed,
 ROW_NUMBER() OVER(PARTITION BY a.UniqHospProvSpellID ORDER BY IFNULL(a.EndDateWardStay,'2100-03-31') DESC, b.MHS502UNIQID DESC) AS WS_Order_Desc
  
 FROM $db_output.spells A
 LEFT JOIN $db_source.MHS502WARDSTAY B on a.UniqHospProvSpellID = b.UniqHospProvSpellID and a.Person_ID = b.Person_ID and b.EndDateWardStay = a.DischDateHospProvSpell
 WHERE
 Acute_Bed <> 'Invalid' and AgeRepPeriodEnd >= 18

# COMMAND ----------

 %sql
 ----this step needs to be done to bin invalid/expired ccg/sub-icb codes into UNKNOWN
 INSERT OVERWRITE TABLE $db_output.distinct_spells 
 SELECT DISTINCT
 Person_ID, 
 UniqHospProvSpellID,
 OrgIDProv,
 Provider_Name,
 StartDateHospProvSpell,
 DischDateHospProvSpell,
 Hosp_LOS,
 AgeRepPeriodEnd,
 CCG_Code,
 CCG_Name,
 REGION_CODE,
 REGION_Name,
 STP_CODE,
 STP_Name
  
 FROM $db_output.distinct_spells_filter A
 WHERE
 Acute_Bed <> 'Invalid' and AgeRepPeriodEnd >= 18

# COMMAND ----------

 %sql
 ----only include Adult Acute and PICU beds at latest stay
 INSERT OVERWRITE TABLE $db_output.distinct_spells_adult_acute_PICU 
 SELECT DISTINCT
 Person_ID, 
 UniqHospProvSpellID,
 OrgIDProv,
 Provider_Name,
 StartDateHospProvSpell,
 DischDateHospProvSpell,
 Hosp_LOS,
 AgeRepPeriodEnd,
 CCG_Code,
 CCG_Name,
 REGION_CODE,
 REGION_Name,
 STP_CODE,
 STP_Name
  
 FROM $db_output.distinct_spells_filter A
 WHERE
 A.WS_Order_Desc = 1
 AND Acute_Bed IN ("Adult Acute","PICU")

# COMMAND ----------

 %sql
 ----only include Older Adult Acute beds at latest stay
 INSERT OVERWRITE TABLE $db_output.distinct_spells_older_adult_acute
 SELECT DISTINCT
 Person_ID, 
 UniqHospProvSpellID,
 OrgIDProv,
 Provider_Name,
 StartDateHospProvSpell,
 DischDateHospProvSpell,
 Hosp_LOS,
 AgeRepPeriodEnd,
 CCG_Code,
 CCG_Name,
 REGION_CODE,
 REGION_Name,
 STP_CODE,
 STP_Name
  
 FROM $db_output.distinct_spells_filter A
 WHERE
 A.WS_Order_Desc = 1
 AND Acute_Bed IN ("Older Adult Acute")