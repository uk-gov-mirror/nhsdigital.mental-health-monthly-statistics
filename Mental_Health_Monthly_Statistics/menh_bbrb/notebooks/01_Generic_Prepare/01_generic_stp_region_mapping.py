# Databricks notebook source
statuses = ["Provisional", "Performance", "Final"]
 
# dbutils.widgets.text("db_output","menh_bbrb")
# dbutils.widgets.text("db_source","mhsds_database")
# dbutils.widgets.dropdown("status","Provisional", statuses)
# dbutils.widgets.text("pub_month", "202201")
# dbutils.widgets.text("rp_enddate", "2021-12-31")
# dbutils.widgets.text("reference_data", "reference_data")
# dbutils.widgets.text("end_month_id", "")

 
db_output  = dbutils.widgets.get("db_output")
db_source = dbutils.widgets.get("db_source")
status = dbutils.widgets.get("status")
pub_month = dbutils.widgets.get("pub_month")
reference_data = dbutils.widgets.get("reference_data")
rp_enddate = dbutils.widgets.get("rp_enddate")
end_month_id = dbutils.widgets.get("end_month_id")

print(db_output, db_source, status, pub_month,reference_data,rp_enddate)

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_org_daily_in_year 
 SELECT 
 ORG_CODE,
 NAME
 FROM      (SELECT
           DISTINCT 
           ORG_CODE, 
           NAME,
           ROW_NUMBER()OVER(PARTITION BY ORG_CODE ORDER BY SYSTEM_CREATED_DATE DESC) AS RN
           FROM $reference_data.org_daily
           WHERE (BUSINESS_END_DATE >= add_months(last_day('$rp_startdate_12m'), 1) OR ISNULL(BUSINESS_END_DATE))
           AND BUSINESS_START_DATE <= add_months(last_day('$rp_startdate_1m'), 1)    
           AND ORG_TYPE_CODE NOT IN ('MP', 'IR', 'F', 'GO', 'CN'))
 WHERE RN = 1;

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_org_daily_latest 
 SELECT DISTINCT ORG_CODE, 
                 NAME
            FROM $reference_data.org_daily
           WHERE (BUSINESS_END_DATE >= add_months('$rp_enddate', 1) OR ISNULL(BUSINESS_END_DATE))
                 AND BUSINESS_START_DATE <= add_months('$rp_enddate', 1)    
                 AND ORG_TYPE_CODE NOT IN ('MP', 'IR', 'F', 'GO', 'CN');

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_org_daily
 SELECT DISTINCT ORG_CODE,
                 NAME,
                 ORG_TYPE_CODE,
                 ORG_OPEN_DATE, 
                 ORG_CLOSE_DATE, 
                 BUSINESS_START_DATE, 
                 BUSINESS_END_DATE
            FROM $reference_data.org_daily
           WHERE (BUSINESS_END_DATE >= add_months('$rp_enddate', 1) OR ISNULL(BUSINESS_END_DATE))
                 AND BUSINESS_START_DATE <= add_months('$rp_enddate', 1)    
                 AND (ORG_CLOSE_DATE >= '$rp_enddate' OR ISNULL(ORG_CLOSE_DATE))              
                 AND ORG_OPEN_DATE <= '$rp_enddate'

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_org_daily_latest_mhsds_providers
 SELECT DISTINCT od.ORG_CODE, 
                 od.NAME
 FROM (SELECT DISTINCT OrgIDProvider from $db_source.mhs000header where UniqMonthID = $end_month_id) h
 INNER JOIN $db_output.bbrb_org_daily_latest od on h.OrgIDProvider = od.ORG_CODE

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_org_daily_past_12_months_mhsds_providers
 SELECT DISTINCT od.ORG_CODE, 
                 od.NAME
 FROM (SELECT DISTINCT OrgIDProvider from $db_source.mhs000header where UniqMonthID between $end_month_id-11 and $end_month_id) h
 INNER JOIN $db_output.bbrb_org_daily_in_year od on h.OrgIDProvider = od.ORG_CODE

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_org_daily_past_quarter_mhsds_providers
 SELECT DISTINCT od.ORG_CODE, 
                 od.NAME
 FROM (SELECT DISTINCT OrgIDProvider from $db_source.mhs000header where UniqMonthID between $end_month_id-2 and $end_month_id) h
 INNER JOIN $db_output.bbrb_org_daily_in_year od on h.OrgIDProvider = od.ORG_CODE

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_org_relationship_daily
 SELECT 
 REL_TYPE_CODE,
 REL_FROM_ORG_CODE,
 REL_TO_ORG_CODE, 
 REL_OPEN_DATE,
 REL_CLOSE_DATE
 FROM 
 $reference_data.org_relationship_daily
 WHERE
 (REL_CLOSE_DATE >= '$rp_enddate' OR ISNULL(REL_CLOSE_DATE))              
 AND REL_OPEN_DATE <= '$rp_enddate'

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.bbrb_stp_mapping
 SELECT 
 A.ORG_CODE as STP_CODE, 
 A.NAME as STP_NAME, 
 C.ORG_CODE as CCG_CODE, 
 C.NAME as CCG_NAME,
 E.ORG_CODE as REGION_CODE,
 E.NAME as REGION_NAME
 FROM 
 $db_output.bbrb_org_daily A
 LEFT JOIN $db_output.bbrb_org_relationship_daily B ON A.ORG_CODE = B.REL_TO_ORG_CODE AND B.REL_TYPE_CODE = 'CCST'
 LEFT JOIN $db_output.bbrb_org_daily C ON B.REL_FROM_ORG_CODE = C.ORG_CODE
 LEFT JOIN $db_output.bbrb_org_relationship_daily D ON A.ORG_CODE = D.REL_FROM_ORG_CODE AND D.REL_TYPE_CODE = 'STCE'
 LEFT JOIN $db_output.bbrb_org_daily E ON D.REL_TO_ORG_CODE = E.ORG_CODE
 WHERE
 A.ORG_TYPE_CODE = 'ST'
 AND B.REL_TYPE_CODE is not null
 AND C.NAME NOT LIKE '%ENTITY%'
 UNION
 SELECT
 "UNKNOWN" as STP_CODE, 
 "UNKNOWN" as STP_NAME, 
 "UNKNOWN" as CCG_CODE, 
 "UNKNOWN" as CCG_NAME,
 "UNKNOWN" as REGION_CODE,
 "UNKNOWN" as REGION_NAME

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.ccg_mapping_2021
 (select CCG_CODE as CCG_UNMAPPED
        ,CCG_CODE as CCG21CDH
        ---------,geo_ccg.GEOGRAPHY_CODE as CCG21CD 
        ,CCG_NAME as CCG21NM 
        -------,geo_stp.GEOGRAPHY_CODE as STP21CD
        ,STP_CODE as STP21CDH 
        ,STP_NAME as STP21NM
        -------,geo_region.GEOGRAPHY_CODE as NHSER21CD 
        ,REGION_CODE as NHSER21CDH 
        ,REGION_NAME as NHSER21NM  
 from $db_output.bbrb_stp_mapping stp_map
 -- inner join $reference_data.ONS_CHD_GEO_EQUIVALENTS geo_ccg
 -- on stp_map.ccg_code = geo_ccg.DH_GEOGRAPHY_CODE
 -- inner join $reference_data.ONS_CHD_GEO_EQUIVALENTS geo_stp
 -- on stp_map.stp_code = geo_stp.DH_GEOGRAPHY_CODE
 -- inner join $reference_data.ONS_CHD_GEO_EQUIVALENTS geo_region
 -- on stp_map.region_code = geo_region.DH_GEOGRAPHY_CODE
 -- where geo_ccg.is_current = 1
 -- and geo_stp.is_current = 1
 -- and geo_region.is_current = 1
 order by ccg_code
 )

# COMMAND ----------

 %md
 ## New Sub ICB Mapping as of Apr26

# COMMAND ----------

 %sql
 ---needed to map OrgIDSubICBLocGP to post Apr26 Sub ICBs
 INSERT OVERWRITE TABLE $db_output.OrgIDSubICBLocGP_Mapping
 select gp.OrganisationId, subicb.TargetOrganisationID, 
 gp.StartDate as GP_StartDate, gp.EndDate as GP_EndDate, subicb.StartDate as SubICB_StartDate, subicb.EndDate as SubICB_EndDate
 from reference_data.odsapiroledetails gp
 inner join reference_data.odsapirelationshipdetails subicb 
             on gp.OrganisationID = subicb.OrganisationID 
             and subicb.RelationshipID = "RE4" ---GP Practice (OrganisationID) is "Commissioned by"
             and subicb.TargetPrimaryRoleID = "RO98" ---TargetOrganisationID is Clinical Commissioning Group
 where (subicb.EndDate is null or subicb.EndDate > "2026-03-31") --Sub ICB is Active after April 2026 Merges

# COMMAND ----------

 %sql
 ---needed to map OrgIDSubICBLocGP to pre Apr26 Sub ICBs
 INSERT OVERWRITE TABLE $db_output.OrgIDSubICBLocGP_Mapping_preApr26
 select gp.OrganisationId, subicb.TargetOrganisationID, 
 gp.StartDate as GP_StartDate, gp.EndDate as GP_EndDate, subicb.StartDate as SubICB_StartDate, subicb.EndDate as SubICB_EndDate
 from reference_data.odsapiroledetails gp
 inner join reference_data.odsapirelationshipdetails subicb 
             on gp.OrganisationID = subicb.OrganisationID 
             and subicb.RelationshipID = "RE4" ---GP Practice (OrganisationID) is "Commissioned by"
             and subicb.TargetPrimaryRoleID = "RO98" ---TargetOrganisationID is Clinical Commissioning Group

# COMMAND ----------

 %sql
 ---needed to map OrgIDSubICBLocResidence
 INSERT OVERWRITE TABLE $db_output.OrgIDSubICBLocResidence_Mapping
 select distinct PCDS, CCG, RECORD_START_DATE, RECORD_END_DATE
 from $reference_data.postcode_special_release_2026
 where CCG is not null and
 RECORD_START_DATE <= "$rp_enddate" and (RECORD_END_DATE is null or RECORD_END_DATE > "$rp_enddate") --PostCode is Active during time period

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW commissioning_org_names AS
 WITH ranked AS (
   SELECT
       OrganisationID,
       Name,
       StartDate AS Date,
       ROW_NUMBER() OVER (PARTITION BY OrganisationID ORDER BY StartDate DESC) AS rn
   FROM $reference_data.ODSAPIOrganisationDetails
 )
 SELECT OrganisationID, Name
 FROM ranked
 WHERE rn = 1

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW valid_subicb_role_details AS
 SELECT
   OrganisationID, StartDate, EndDate, RoleId, PrimaryRole, DateType

 FROM (
 SELECT
     rd.OrganisationID,
     rd.StartDate,
     rd.EndDate,
     rd.RoleId,
     rd.PrimaryRole,
     rd.DateType,
     ROW_NUMBER() OVER (PARTITION BY rd.OrganisationID ORDER BY rd.DateType ASC, rd.StartDate DESC) AS rn
   FROM $reference_data.ODSAPIRoleDetails rd
   WHERE rd.RoleId = 'RO319'
     AND rd.PrimaryRole = 0
 ) rd
 WHERE rn = 1
 AND rd.StartDate <= add_months("2026-03-31", 1)
 AND (rd.EndDate >= add_months("2026-03-31", 1) OR rd.EndDate IS NULL)

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW valid_subicb_no_hubs AS
 SELECT a.*
 FROM valid_subicb_role_details a
 INNER JOIN commissioning_org_names b
   ON a.OrganisationID = b.OrganisationID
 WHERE b.Name NOT RLIKE 'HUB|NATIONAL|ENTITY'

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW valid_icb_targets as
 select distinct OrganisationID, TargetOrganisationID 
 from $reference_data.odsapirelationshipdetails icb
 where icb.TargetPrimaryRoleID = "RO261"
 AND icb.StartDate <= add_months("2026-03-31", 1)
 AND (icb.EndDate >= add_months("2026-03-31", 1) OR icb.EndDate IS NULL)

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW valid_region_targets as
 select distinct OrganisationID, TargetOrganisationID 
 from $reference_data.odsapirelationshipdetails reg
 where reg.TargetPrimaryRoleID = "RO209"
 AND reg.StartDate <= add_months("2026-03-31", 1)
 AND (reg.EndDate >= add_months("2026-03-31", 1) OR reg.EndDate IS NULL)

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.commissioning_org_mapping
 SELECT
   CASE
     WHEN sub.OrganisationID = 'U2G6B' THEN 'D4U1Y'
     ELSE sub.OrganisationID
     END 
     AS ORIGINAL_CCG_CODE,
 CASE 
     WHEN sub.OrganisationID = 'U2G6B' THEN 0.589
     WHEN sub.OrganisationID = '92A' THEN 1.133
     WHEN sub.OrganisationID = 'D9Y0V' THEN 1.108
     ELSE 1 
     END
     AS POPULATION_FACTOR,
   sub.OrganisationID              AS CCG_Code,
   subn.Name                       AS CCG_Name,
   icb.TargetOrganisationID         AS STP_Code,
   icbn.Name                        AS STP_Name,
   reg.TargetOrganisationID         AS Region_Code,
   regn.Name                        AS Region_Name
 FROM valid_subicb_no_hubs sub
 LEFT JOIN commissioning_org_names subn
   ON sub.OrganisationID = subn.OrganisationID
 LEFT JOIN valid_icb_targets icb
   ON sub.OrganisationID = icb.OrganisationID
 LEFT JOIN commissioning_org_names icbn
   ON icb.TargetOrganisationID = icbn.OrganisationID
 LEFT JOIN valid_region_targets reg
   ON icb.TargetOrganisationID = reg.OrganisationID
 LEFT JOIN commissioning_org_names regn
   ON reg.TargetOrganisationID = regn.OrganisationID
 WHERE icb.TargetOrganisationID IS NOT NULL
   AND reg.TargetOrganisationID IS NOT NULL


 UNION
 SELECT
 "UNKNOWN" as ORIGINAL_CCG_CODE,
 1 as POPULATION_FACTOR,
 "UNKNOWN" as STP_CODE, 
 "UNKNOWN" as STP_NAME, 
 "UNKNOWN" as CCG_CODE, 
 "UNKNOWN" as CCG_NAME,
 "UNKNOWN" as REGION_CODE,
 "UNKNOWN" as REGION_NAME