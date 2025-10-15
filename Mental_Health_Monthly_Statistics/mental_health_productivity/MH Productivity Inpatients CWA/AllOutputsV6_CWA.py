# Databricks notebook source
# dbutils.widgets.removeAll()

# COMMAND ----------

dbutils.widgets.text("db_input", "")
dbutils.widgets.text("db_source", "")
dbutils.widgets.text("rp_start", "")
dbutils.widgets.text("rp_enddate", "")
dbutils.widgets.text("month_id_end", "")
dbutils.widgets.text("month_id_start", "")

# COMMAND ----------

db_output = dbutils.widgets.get("db_output")
db_source = dbutils.widgets.get("db_source")
rp_start = dbutils.widgets.get("rp_start")
rp_enddate = dbutils.widgets.get("rp_enddate")
month_id_end = dbutils.widgets.get("month_id_end")
month_id_start = dbutils.widgets.get("month_id_start")

assert db_output
assert db_source
assert rp_start
assert rp_enddate
assert month_id_start
assert month_id_end

print(db_output)
print(db_source)
print(rp_start)
print(rp_enddate)
print(month_id_start)
print(month_id_end)

# COMMAND ----------

# Code produces Cost Weighted Activity values for 47 providers listed in Productivity team's spreadsheet. Other providers grouped together

# For v6 data ie from the start of April 2024. 
# Mapping of v6 MHAdmittedPatientClass on to v5 HospitalBedTypeMH occurs in cmd 11 to allow time series of data to extend across version change.

# Cost Weighted Activity CWA values are calculated by ward stay hospital bed type (field HospitalBedTypeMH on table MHS502WardStay) for following model:
#         - activity set to the bed type mean length of stay up to the Trimpoint. Set any excess beddays above Trimpoint at 50% value. 

# Costs are then applied for each bed type using Productivity team's spreadsheet and community cost for zero LoSs and then summed to produce overall CWA for each provider 

# Notes: 1) Trimpoints for each bed type calculated as upper quartile threshold value for non-zero ward stays. 
#        2) 23/24 Trimpoints and mean LoS are applied to ALL YEARS. These are stored in table $db_output.beddays_ended_ws_2324.
#           CODE WILL NEED RUNNING FOR 23/24 FIRST for cmd 16 to produce table to be used for all other years.
#        3) Zero length of stays output are set 0 activity. The number of zero LoSs for each bed type are output so zero LoSs can be costed separately 
#        4) For ward stays that span more than one financial year, the activity will be reduced proportionately. 

# Code below is an edited version of MH bulletin code to produce sum of beddays - check aggregate of beddays matches bulletin output for each year for all bed types.

# Amongst other calculations this version produces bed days in RP in excess of the 75th percentile for 23/24 - calculated by ignoring zero LoS and setting excess values to trimpoint

# There has been some re-mapping of bed types since the first set of data packs were sent out in Feb 25.

# Output in cmd 17, 18, 19, 20
# cmd 17: 47 trusts Excess bed days for Non-secure and Unknown bed types combined
# cmd 18: 47 trusts CWA (cost weighted activity) by Secure, Non-secure and Unknown bed types - 75th percentile and Full recognition models.
# cmd 19: 47 trusts Mean length of stay (LoS) for Non-secure and Unknown bed types combined
# cmd 20: 47 trusts all above values by provider and bed type.

# COMMAND ----------

 %sql --code to create MHB_MHS001 table from mhb_assets notebook
 DROP TABLE IF EXISTS $db_output.MHB_MHS001MPI_v6;
 CREATE TABLE IF NOT EXISTS $db_output.MHB_MHS001MPI_v6 USING DELTA AS
 ---get all mhs001mpi data for the financial year
 SELECT * FROM
 (
 SELECT 
 LocalPatientId
 ,OrgIDLocalPatientId
 ,OrgIDResidenceResp
 ,OrgIDEduEstab
 ,NHSNumber
 ,NHSNumberStatus
 ,Gender
 ,GenderIDCode
 ,CASE WHEN GenderIDCode IN ('1','2','3','4') THEN GenderIDCode
       WHEN Gender IN ('1','2','9') THEN Gender
       ELSE 'Unknown' END AS Der_Gender
 ,MaritalStatus
 ,EthnicCategory
 ,LanguageCodePreferred
 ,RecordNumber
 ,MHS001UniqID
 ,OrgIDProv
 ,CASE 
   when OrgIDCCGRes in ('00C','00K','00M') THEN '16C'
   when OrgIDCCGRes in ('05F','05J','05T','06D') THEN '18C'
   when OrgIDCCGRes in ('06M','06V','06W','06Y','07J') THEN '26A'
   when OrgIDCCGRes in ('01C','01R','02D','02F') THEN '27D'
   when OrgIDCCGRes in ('02N','02W','02R') THEN '36J'
   when OrgIDCCGRes in ('07V','08J','08R','08P','08T','08X') THEN '36L'
   when OrgIDCCGRes in ('03D','03E','03M') THEN '42D'
   when OrgIDCCGRes in ('04E','04H','04K','04L','04M','04N') THEN '52R'
   when OrgIDCCGRes in ('09G','09H','09X') THEN '70F'
   when OrgIDCCGRes in ('03T','04D','99D','04Q') THEN '71E'
   when OrgIDCCGRes in ('07N','07Q','08A','08K','08L','08Q') THEN '72Q'
   when OrgIDCCGRes in ('03V','04G') THEN '78H'
   when OrgIDCCGRes in ('00D','00J') THEN '84H'
   when OrgIDCCGRes in ('09C','09E','09J','09W','10A','10D','10E','99J') THEN '91Q'
   when OrgIDCCGRes in ('09L','09N','09Y','99H') THEN '92A'
   when OrgIDCCGRes in ('11E','12D','99N') THEN '92G'
   when OrgIDCCGRes in ('07M','07R','07X','08D','08H') THEN '93C'
   when OrgIDCCGRes in ('09F','09P','99K') THEN '97R'
   ELSE OrgIDCCGRes
   END as OrgIDCCGRes
 ,Person_ID
 ,UniqSubmissionID
 ,AgeRepPeriodStart
 ,AgeRepPeriodEnd
 ,AgeDeath
 ,PostcodeDistrict
 ,DefaultPostcode
 ,LSOA2011
 ,LADistrictAuth
 ,County
 ,ElectoralWard
 ,UniqMonthID
 ,NHSDEthnicity
 ,PatMRecInRP
 ,RecordStartDate
 ,RecordEndDate
 ,CCGGPRes
 ,IMDQuart
 ,PersDeathDate
 ,dense_rank() OVER (PARTITION BY Person_ID, OrgIDProv ORDER BY UniqMonthID DESC, RecordNumber DESC) AS RANK

 FROM $db_source.MHS001MPI
 WHERE UniqMonthID between $month_id_start and $month_id_end
 AND (RecordEndDate is null or RecordEndDate >= '$rp_enddate') AND RecordStartDate BETWEEN '$rp_start' AND '$rp_enddate' ---mhs001mpi records in the financial year only
 )
 WHERE RANK = '1'

# COMMAND ----------

 %sql  --code to create MPI_max_month table from 01.generic_prep notebook
 CREATE OR REPLACE TEMP VIEW MPI_max_month AS
 ---gets max UniqMonthID for a person_id where PatMRecInRP is true (latest submitted mhs001mpi record for a person_id in month)
 SELECT			x.Person_id,
 				MAX(x.uniqmonthid) AS uniqmonthid --change back to monthid for 19-20 (record_number for 18/9)
 FROM			$db_output.MHB_MHS001MPI x	
 where           PatMRecInRP = true 
 GROUP BY		x.Person_id

# COMMAND ----------

 %sql --code to create MPI_part1 table from 01.generic_prep notebook
 CREATE OR REPLACE TEMP VIEW MPI_part1 AS
 ---joins max UniqMonthID back onto mpi table to get latest information for each person. Uses PatMrecInRP for unique person details within same month
 Select          distinct x.*
 from            $db_output.MHB_MHS001MPI x  
 INNER JOIN      MPI_max_month AS z
                 ON x.Person_id = z.Person_id 
                 AND x.uniqmonthid = z.uniqmonthid 
 where           x.PatMRecInRP = true 

# COMMAND ----------

 %sql --code to create MPI table from 01.generic_prep notebook
 DROP TABLE IF EXISTS $db_output.MPI_v6;
 CREATE TABLE         $db_output.MPI_v6 AS
 ---incorporates majority of required demographic breakdowns into the final mpi table
 select          a.*,
                 case when AgeRepPeriodEnd between 0 and 17 then 'Under 18'
                      when AgeRepPeriodEnd >= 18 then '18 and over' 
                      else 'Unknown' end as age_group_higher_level,
                 case when AgeRepPeriodEnd between 0 and 5 then '0 to 5'
                      when AgeRepPeriodEnd between 6 and 10 then '6 to 10'
                      when AgeRepPeriodEnd between 11 and 15 then '11 to 15'
                      when AgeRepPeriodEnd = 16 then '16'
                      when AgeRepPeriodEnd = 17 then '17'
                      when AgeRepPeriodEnd = 18 then '18'
                      when AgeRepPeriodEnd = 19 then '19'
                      when AgeRepPeriodEnd between 20 and 24 then '20 to 24'
                      when AgeRepPeriodEnd between 25 and 29 then '25 to 29'
                      when AgeRepPeriodEnd between 30 and 34 then '30 to 34'
                      when AgeRepPeriodEnd between 35 and 39 then '35 to 39'
                      when AgeRepPeriodEnd between 40 and 44 then '40 to 44'
                      when AgeRepPeriodEnd between 45 and 49 then '45 to 49'
                      when AgeRepPeriodEnd between 50 and 54 then '50 to 54'
                      when AgeRepPeriodEnd between 55 and 59 then '55 to 59'
                      when AgeRepPeriodEnd between 60 and 64 then '60 to 64'
                      when AgeRepPeriodEnd between 65 and 69 then '65 to 69'
                      when AgeRepPeriodEnd between 70 and 74 then '70 to 74'
                      when AgeRepPeriodEnd between 75 and 79 then '75 to 79'
                      when AgeRepPeriodEnd between 80 and 84 then '80 to 84'
                      when AgeRepPeriodEnd between 85 and 89 then '85 to 89'
                      when AgeRepPeriodEnd >= '90' then '90 or over' else 'Unknown' end as age_group_lower_chap1,
                  CASE WHEN AgeRepPeriodEnd BETWEEN 0 and 13 THEN 'Under 14'
                       WHEN AgeRepPeriodEnd BETWEEN 14 and 15 THEN '14 to 15'
                       WHEN AgeRepPeriodEnd BETWEEN 16 and 17 THEN '16 to 17'
                       WHEN AgeRepPeriodEnd BETWEEN 18 AND 19 THEN '18 to 19'
                       WHEN AgeRepPeriodEnd BETWEEN 20 AND 24 THEN '20 to 24'
                       WHEN AgeRepPeriodEnd BETWEEN 25 AND 29 THEN '25 to 29'
                       WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                       WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                       WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                       WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                       WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                       WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                       WHEN AgeRepPeriodEnd BETWEEN 60 AND 64 THEN '60 to 64'
                       WHEN AgeRepPeriodEnd BETWEEN 65 AND 69 THEN '65 to 69'
                       WHEN AgeRepPeriodEnd BETWEEN 70 AND 74 THEN '70 to 74'
                       WHEN AgeRepPeriodEnd BETWEEN 75 AND 79 THEN '75 to 79'
                       WHEN AgeRepPeriodEnd BETWEEN 80 AND 84 THEN '80 to 84'
                       WHEN AgeRepPeriodEnd BETWEEN 85 AND 89 THEN '85 to 89' 
                       WHEN AgeRepPeriodEnd >= 90 THEN '90 or over' else 'Unknown' END As age_group_lower_chap45,
                  CASE WHEN AgeRepPeriodEnd BETWEEN 0 and 17 THEN 'Under 18'
                       WHEN AgeRepPeriodEnd BETWEEN 18 and 24 THEN '18 to 24'
                       WHEN AgeRepPeriodEnd BETWEEN 25 and 29 THEN '25 to 29'                
                       WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                       WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                       WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                       WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                       WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                       WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                       WHEN AgeRepPeriodEnd >= 60 THEN '60 or over' else 'Unknown' END AS age_group_lower_chap7,
                   CASE WHEN AgeRepPeriodEnd BETWEEN 0 AND 14 THEN 'Under 15'
                        WHEN AgeRepPeriodEnd BETWEEN 15 AND 19 THEN '15 to 19'
                        WHEN AgeRepPeriodEnd BETWEEN 20 AND 24 THEN '20 to 24'
                        WHEN AgeRepPeriodEnd BETWEEN 25 AND 29 THEN '25 to 29'
                        WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                        WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                        WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                        WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                        WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                        WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                        WHEN AgeRepPeriodEnd BETWEEN 60 AND 64 THEN '60 to 64'
                        WHEN AgeRepPeriodEnd > 64 THEN '65 and over' ELSE 'Unknown' END as age_group_lower_chap11,  
                    CASE WHEN AgeRepPeriodEnd BETWEEN 0 AND 17 THEN 'Under 18'
                        WHEN AgeRepPeriodEnd BETWEEN 18 AND 19 THEN '18 to 19'
                        WHEN AgeRepPeriodEnd BETWEEN 20 AND 24 THEN '20 to 24'
                        WHEN AgeRepPeriodEnd BETWEEN 25 AND 29 THEN '25 to 29'
                        WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                        WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                        WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                        WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                        WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                        WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                        WHEN AgeRepPeriodEnd BETWEEN 60 AND 64 THEN '60 to 64'
                        WHEN AgeRepPeriodEnd BETWEEN 65 AND 69 THEN '65 to 69'
                        WHEN AgeRepPeriodEnd BETWEEN 70 AND 74 THEN '70 to 74'
                        WHEN AgeRepPeriodEnd BETWEEN 75 AND 79 THEN '75 to 79'
                        WHEN AgeRepPeriodEnd BETWEEN 80 AND 84 THEN '80 to 84'
                        WHEN AgeRepPeriodEnd BETWEEN 85 AND 89 THEN '85 to 89'
                        WHEN AgeRepPeriodEnd >= 90 THEN '90 and over' ELSE 'Unknown' END as age_group_lower_chap12,                      
                    CASE WHEN a.NHSDEthnicity IN ('A', 'B', 'C') THEN 'White'
                         WHEN a.NHSDEthnicity IN ('D', 'E', 'F', 'G') THEN 'Mixed'
                         WHEN a.NHSDEthnicity IN ('H', 'J', 'K', 'L') THEN 'Asian or Asian British'
                         WHEN a.NHSDEthnicity IN ('M', 'N', 'P') THEN 'Black or Black British'
                         WHEN a.NHSDEthnicity IN ('R', 'S') THEN 'Other Ethnic Groups'
                         WHEN a.NHSDEthnicity = 'Z' THEN 'Not Stated'
                         WHEN a.NHSDEthnicity = '99' THEN 'Not Known'
                         ELSE 'Unknown' END AS UpperEthnicity,
              CASE WHEN a.NHSDEthnicity = 'A' THEN 'A'
                    WHEN a.NHSDEthnicity = 'B' THEN 'B'
                    WHEN a.NHSDEthnicity = 'C' THEN 'C'
                    WHEN a.NHSDEthnicity = 'D' THEN 'D'
                    WHEN a.NHSDEthnicity = 'E' THEN 'E'
                    WHEN a.NHSDEthnicity = 'F' THEN 'F'
                    WHEN a.NHSDEthnicity = 'G' THEN 'G'
                    WHEN a.NHSDEthnicity = 'H' THEN 'H'
                    WHEN a.NHSDEthnicity = 'J' THEN 'J'
                    WHEN a.NHSDEthnicity = 'K' THEN 'K'
                    WHEN a.NHSDEthnicity = 'L' THEN 'L'
                    WHEN a.NHSDEthnicity = 'M' THEN 'M'
                    WHEN a.NHSDEthnicity = 'N' THEN 'N'
                    WHEN a.NHSDEthnicity = 'P' THEN 'P'
                    WHEN a.NHSDEthnicity = 'R' THEN 'R'
                    WHEN a.NHSDEthnicity = 'S' THEN 'S'
                    WHEN a.NHSDEthnicity = 'Z' THEN 'Not Stated'
                    WHEN a.NHSDEthnicity = '99' THEN 'Not Known'
                            ELSE 'Unknown' END AS LowerEthnicity,
                  'Unknown' AS IMD_Decile,
                  'Unknown' AS IMD_Quintile
 from            MPI_part1 a
 -- left join       [DATABASE].[DEPRIVATION_REF] r 
 --                 on a.LSOA2011 = r.LSOA_CODE_2011 
 --                 and r.imd_year = '$IMD_year'

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMP VIEW MPI_max_month_prov AS
 ---A person may have been treated in more than one provider, could contain different person information. For the purposes of provider breakdowns, require 1 set of person details per provider
 SELECT			x.orgidprov
                 ,x.Person_id
 				,MAX(x.uniqmonthid) AS uniqmonthid
 FROM			$db_output.MHB_MHS001MPI_v6 x	
 GROUP BY		x.orgidprov
                 ,x.Person_id

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.MPI_PROV_v6;
 CREATE TABLE         $db_output.MPI_PROV_v6 AS
 ---incorporates majority of required demographic breakdowns into the final mpi provider table
 Select          distinct x.*,
                 case when AgeRepPeriodEnd between 0 and 17 then 'Under 18'
                           when AgeRepPeriodEnd >= 18 then '18 and over'
                           else 'Unknown' end as age_group_higher_level,
                  case when AgeRepPeriodEnd between 0 and 5 then '0 to 5'
                      when AgeRepPeriodEnd between 6 and 10 then '6 to 10'
                      when AgeRepPeriodEnd between 11 and 15 then '11 to 15'
                      when AgeRepPeriodEnd = 16 then '16'
                      when AgeRepPeriodEnd = 17 then '17'
                      when AgeRepPeriodEnd = 18 then '18'
                      when AgeRepPeriodEnd = 19 then '19'
                      when AgeRepPeriodEnd between 20 and 24 then '20 to 24'
                      when AgeRepPeriodEnd between 25 and 29 then '25 to 29'
                      when AgeRepPeriodEnd between 30 and 34 then '30 to 34'
                      when AgeRepPeriodEnd between 35 and 39 then '35 to 39'
                      when AgeRepPeriodEnd between 40 and 44 then '40 to 44'
                      when AgeRepPeriodEnd between 45 and 49 then '45 to 49'
                      when AgeRepPeriodEnd between 50 and 54 then '50 to 54'
                      when AgeRepPeriodEnd between 55 and 59 then '55 to 59'
                      when AgeRepPeriodEnd between 60 and 64 then '60 to 64'
                      when AgeRepPeriodEnd between 65 and 69 then '65 to 69'
                      when AgeRepPeriodEnd between 70 and 74 then '70 to 74'
                      when AgeRepPeriodEnd between 75 and 79 then '75 to 79'
                      when AgeRepPeriodEnd between 80 and 84 then '80 to 84'
                      when AgeRepPeriodEnd between 85 and 89 then '85 to 89'
                      when AgeRepPeriodEnd >= '90' then '90 or over' else 'Unknown' end as age_group_lower_chap1,
                  CASE WHEN AgeRepPeriodEnd BETWEEN 0 and 13 THEN 'Under 14'
                       WHEN AgeRepPeriodEnd BETWEEN 14 and 15 THEN '14 to 15'
                       WHEN AgeRepPeriodEnd BETWEEN 16 and 17 THEN '16 to 17'
                       WHEN AgeRepPeriodEnd BETWEEN 18 AND 19 THEN '18 to 19'
                       WHEN AgeRepPeriodEnd BETWEEN 20 AND 24 THEN '20 to 24'
                       WHEN AgeRepPeriodEnd BETWEEN 25 AND 29 THEN '25 to 29'
                       WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                       WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                       WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                       WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                       WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                       WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                       WHEN AgeRepPeriodEnd BETWEEN 60 AND 64 THEN '60 to 64'
                       WHEN AgeRepPeriodEnd BETWEEN 65 AND 69 THEN '65 to 69'
                       WHEN AgeRepPeriodEnd BETWEEN 70 AND 74 THEN '70 to 74'
                       WHEN AgeRepPeriodEnd BETWEEN 75 AND 79 THEN '75 to 79'
                       WHEN AgeRepPeriodEnd BETWEEN 80 AND 84 THEN '80 to 84'
                       WHEN AgeRepPeriodEnd BETWEEN 85 AND 89 THEN '85 to 89' 
                       WHEN AgeRepPeriodEnd >= 90 THEN '90 or over' else 'Unknown' END As age_group_lower_chap45,
                  CASE WHEN AgeRepPeriodEnd BETWEEN 0 and 17 THEN 'Under 18'
                       WHEN AgeRepPeriodEnd BETWEEN 18 and 24 THEN '18 to 24'
                       WHEN AgeRepPeriodEnd BETWEEN 25 and 29 THEN '16 to 17'
                       WHEN AgeRepPeriodEnd BETWEEN 18 AND 19 THEN '18 to 19'
                       WHEN AgeRepPeriodEnd BETWEEN 20 AND 24 THEN '20 to 24'
                       WHEN AgeRepPeriodEnd BETWEEN 25 AND 29 THEN '25 to 29'
                       WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                       WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                       WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                       WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                       WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                       WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                       WHEN AgeRepPeriodEnd >= 60 THEN '60 or over' else 'Unknown' END AS age_group_lower_chap7, 
                       CASE WHEN AgeRepPeriodEnd BETWEEN 0 AND 14 THEN 'Under 15'
                        WHEN AgeRepPeriodEnd BETWEEN 15 AND 19 THEN '15 to 19'
                        WHEN AgeRepPeriodEnd BETWEEN 20 AND 24 THEN '20 to 24'
                        WHEN AgeRepPeriodEnd BETWEEN 25 AND 29 THEN '25 to 29'
                        WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                        WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                        WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                        WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                        WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                        WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                        WHEN AgeRepPeriodEnd BETWEEN 60 AND 64 THEN '60 to 64'
                        WHEN AgeRepPeriodEnd > 64 THEN '65 and over' ELSE 'Unknown' END as age_group_lower_chap11, 
                        CASE WHEN AgeRepPeriodEnd BETWEEN 0 AND 17 THEN 'Under 18'
                        WHEN AgeRepPeriodEnd BETWEEN 18 AND 19 THEN '18 to 19'
                        WHEN AgeRepPeriodEnd BETWEEN 20 AND 24 THEN '20 to 24'
                        WHEN AgeRepPeriodEnd BETWEEN 25 AND 29 THEN '25 to 29'
                        WHEN AgeRepPeriodEnd BETWEEN 30 AND 34 THEN '30 to 34'
                        WHEN AgeRepPeriodEnd BETWEEN 35 AND 39 THEN '35 to 39'
                        WHEN AgeRepPeriodEnd BETWEEN 40 AND 44 THEN '40 to 44'
                        WHEN AgeRepPeriodEnd BETWEEN 45 AND 49 THEN '45 to 49'
                        WHEN AgeRepPeriodEnd BETWEEN 50 AND 54 THEN '50 to 54'
                        WHEN AgeRepPeriodEnd BETWEEN 55 AND 59 THEN '55 to 59'
                        WHEN AgeRepPeriodEnd BETWEEN 60 AND 64 THEN '60 to 64'
                        WHEN AgeRepPeriodEnd BETWEEN 65 AND 69 THEN '65 to 69'
                        WHEN AgeRepPeriodEnd BETWEEN 70 AND 74 THEN '70 to 74'
                        WHEN AgeRepPeriodEnd BETWEEN 75 AND 79 THEN '75 to 79'
                        WHEN AgeRepPeriodEnd BETWEEN 80 AND 84 THEN '80 to 84'
                        WHEN AgeRepPeriodEnd BETWEEN 85 AND 89 THEN '85 to 89'
                        WHEN AgeRepPeriodEnd >= 90 THEN '90 and over' ELSE 'Unknown' END as age_group_lower_chap12,  
                    CASE WHEN x.NHSDEthnicity IN ('A', 'B', 'C') THEN 'White'
                         WHEN x.NHSDEthnicity IN ('D', 'E', 'F', 'G') THEN 'Mixed'
                         WHEN x.NHSDEthnicity IN ('H', 'J', 'K', 'L') THEN 'Asian or Asian British'
                         WHEN x.NHSDEthnicity IN ('M', 'N', 'P') THEN 'Black or Black British'
                         WHEN x.NHSDEthnicity IN ('R', 'S') THEN 'Other Ethnic Groups'
                         WHEN x.NHSDEthnicity = 'Z' THEN 'Not Stated'
                         WHEN x.NHSDEthnicity = '99' THEN 'Not Known'
                         ELSE 'Unknown' END AS UpperEthnicity,
              CASE WHEN x.NHSDEthnicity = 'A' THEN 'A'
                    WHEN x.NHSDEthnicity = 'B' THEN 'B'
                    WHEN x.NHSDEthnicity = 'C' THEN 'C'
                    WHEN x.NHSDEthnicity = 'D' THEN 'D'
                    WHEN x.NHSDEthnicity = 'E' THEN 'E'
                    WHEN x.NHSDEthnicity = 'F' THEN 'F'
                    WHEN x.NHSDEthnicity = 'G' THEN 'G'
                    WHEN x.NHSDEthnicity = 'H' THEN 'H'
                    WHEN x.NHSDEthnicity = 'J' THEN 'J'
                    WHEN x.NHSDEthnicity = 'K' THEN 'K'
                    WHEN x.NHSDEthnicity = 'L' THEN 'L'
                    WHEN x.NHSDEthnicity = 'M' THEN 'M'
                    WHEN x.NHSDEthnicity = 'N' THEN 'N'
                    WHEN x.NHSDEthnicity = 'P' THEN 'P'
                    WHEN x.NHSDEthnicity = 'R' THEN 'R'
                    WHEN x.NHSDEthnicity = 'S' THEN 'S'
                    WHEN x.NHSDEthnicity = 'Z' THEN 'Not Stated'
                    WHEN x.NHSDEthnicity = '99' THEN 'Not Known'
                            ELSE 'Unknown' END AS LowerEthnicity,
                 'Unknown' AS IMD_Decile,
                 'Unknown' AS IMD_Quintile
 from            $db_output.MHB_MHS001MPI_v6 x  
 INNER JOIN      MPI_max_month_prov AS z
                     ON x.Person_id = z.Person_id 
                     AND x.uniqmonthid = z.uniqmonthid
                     and x.orgidprov = z.orgidprov
 -- left join       [DATABASE].[DEPRIVATION_REF] r 
 --                     on x.LSOA2011 = r.LSOA_CODE_2011 
 --                     and r.imd_year = '$IMD_year'

# COMMAND ----------

 %sql --code to create MHB_MHS502WardStay from mhb_assets notebook
 DROP TABLE IF EXISTS $db_output.MHB_MHS502WardStay_v6;
 CREATE TABLE IF NOT EXISTS $db_output.MHB_MHS502WardStay_v6 USING DELTA AS
 ---get all mhs502wardstay data for the financial year
 SELECT *
 FROM $db_source.MHS502WardStay
 WHERE UniqMonthID between $month_id_start and $month_id_end
 AND (RecordEndDate is null or RecordEndDate >= '$rp_enddate') AND RecordStartDate BETWEEN '$rp_start' AND '$rp_enddate' ---get all mhs502wardstay records in the financial year only

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMP VIEW bedtype_prov AS
 ---get distinct provider, person_id, bed type and associated bed days in the financial year
 select                distinct  OrgIDProv
                       ,Person_ID 
                       ,UniqWardStayID
                       ,StartDateWardStay
                       ,EndDateWardStay
                       ,CASE WHEN MHAdmittedPatientClass = '200' THEN '10'
                             WHEN MHAdmittedPatientClass = '201' THEN '11'
                             WHEN MHAdmittedPatientClass = '202' THEN '12'
                             WHEN MHAdmittedPatientClass = '203' THEN '13'
                             WHEN MHAdmittedPatientClass = '204' THEN '14'
                             WHEN MHAdmittedPatientClass = '205' THEN '15'
                             WHEN MHAdmittedPatientClass = '206' THEN '19'
                             WHEN MHAdmittedPatientClass = '207' THEN '20'
                             WHEN MHAdmittedPatientClass = '208' THEN '21'
                             WHEN MHAdmittedPatientClass = '209' THEN '22'
                             WHEN MHAdmittedPatientClass = '210' THEN '40'
                             WHEN MHAdmittedPatientClass = '211' THEN '39'
                             WHEN MHAdmittedPatientClass IN ('35','36','37','38') THEN '35' --GROUPING OLD V5 BED TYPES TOGETHER TO MATCH WITH V6
                             WHEN MHAdmittedPatientClass = '212' THEN '35'
                             WHEN MHAdmittedPatientClass = '213' THEN '35'
                             WHEN MHAdmittedPatientClass = '300' THEN '23'
                             WHEN MHAdmittedPatientClass = '301' THEN '24'
                             WHEN MHAdmittedPatientClass = '26' THEN '25' --GROUPING OLD V5 BED TYPES TOGETHER TO MATCH WITH V6
                             WHEN MHAdmittedPatientClass = '302' THEN '25'
                             WHEN MHAdmittedPatientClass = '303' THEN '27'
                             WHEN MHAdmittedPatientClass = '304' THEN '28'
                             WHEN MHAdmittedPatientClass = '305' THEN '29'
                             WHEN MHAdmittedPatientClass = '306' THEN '31'
                             WHEN MHAdmittedPatientClass = '307' THEN '32'
                             WHEN MHAdmittedPatientClass = '308' THEN '33'
                             WHEN MHAdmittedPatientClass = '309' THEN '34'
                             WHEN MHAdmittedPatientClass = '310' THEN '30'
                             WHEN MHAdmittedPatientClass = '311' THEN '30'                        
                             ELSE null
                        END as HospitalBedTypeMH
                       ,MHAdmittedPatientClass
                       ,InactTimeWS
                       ,CASE WHEN (EndDateWardStay IS NULL AND InactTimeWS IS NULL) THEN DATE_ADD('$rp_enddate',1)
                                          WHEN InactTimeWS IS NOT NULL THEN InactTimeWS
                                          ELSE EndDateWardStay END as EndOrInactDate
                       ,sum(datediff(CASE WHEN (EndDateWardStay IS NULL AND InactTimeWS IS NULL) THEN DATE_ADD('$rp_enddate',1)
                                          WHEN InactTimeWS IS NOT NULL THEN InactTimeWS
                                          ELSE EndDateWardStay END
                             ,CASE WHEN StartDateWardStay < '$rp_start' THEN '$rp_start'
                                   ELSE StartDateWardStay END)) as Beddays
                       ,sum(case when EndDateWardStay between '$rp_start' and '$rp_enddate' 
                                 then datediff(CASE WHEN InactTimeWS IS NOT NULL THEN InactTimeWS ELSE EndDateWardStay END, StartDateWardStay) 
                                 end) as bed_days_ws_full
                       ,count(distinct case when EndDateWardStay between '$rp_start' and '$rp_enddate' 
                                 then UniqWardStayID end) as EndedDistinctWardStaysinYear
                       ,count(case when EndDateWardStay between '$rp_start' and '$rp_enddate' 
                                 then UniqWardStayID end) as EndedWardStaysinYear
 from                  $db_output.MHB_MHS502WardStay_v6 
 group by              OrgIDProv
                       ,Person_ID
                       ,UniqWardStayID
                       ,StartDateWardStay
                       ,EndDateWardStay
                       ,CASE WHEN MHAdmittedPatientClass = '200' THEN '10'
                             WHEN MHAdmittedPatientClass = '201' THEN '11'
                             WHEN MHAdmittedPatientClass = '202' THEN '12'
                             WHEN MHAdmittedPatientClass = '203' THEN '13'
                             WHEN MHAdmittedPatientClass = '204' THEN '14'
                             WHEN MHAdmittedPatientClass = '205' THEN '15'
                             WHEN MHAdmittedPatientClass = '206' THEN '19'
                             WHEN MHAdmittedPatientClass = '207' THEN '20'
                             WHEN MHAdmittedPatientClass = '208' THEN '21'
                             WHEN MHAdmittedPatientClass = '209' THEN '22'
                             WHEN MHAdmittedPatientClass = '210' THEN '40'
                             WHEN MHAdmittedPatientClass = '211' THEN '39'
                             WHEN MHAdmittedPatientClass IN ('35','36','37','38') THEN '35' --GROUPING OLD V5 BED TYPES TOGETHER TO MATCH WITH V6
                             WHEN MHAdmittedPatientClass = '212' THEN '35'
                             WHEN MHAdmittedPatientClass = '213' THEN '35'
                             WHEN MHAdmittedPatientClass = '300' THEN '23'
                             WHEN MHAdmittedPatientClass = '301' THEN '24'
                             WHEN MHAdmittedPatientClass = '26' THEN '25' --GROUPING OLD V5 BED TYPES TOGETHER TO MATCH WITH V6
                             WHEN MHAdmittedPatientClass = '302' THEN '25'
                             WHEN MHAdmittedPatientClass = '303' THEN '27'
                             WHEN MHAdmittedPatientClass = '304' THEN '28'
                             WHEN MHAdmittedPatientClass = '305' THEN '29'
                             WHEN MHAdmittedPatientClass = '306' THEN '31'
                             WHEN MHAdmittedPatientClass = '307' THEN '32'
                             WHEN MHAdmittedPatientClass = '308' THEN '33'
                             WHEN MHAdmittedPatientClass = '309' THEN '34'
                             WHEN MHAdmittedPatientClass = '310' THEN '30'
                             WHEN MHAdmittedPatientClass = '311' THEN '30'                        
                             ELSE null
                        END
                       ,MHAdmittedPatientClass
                       ,InactTimeWS
                       ,CASE WHEN (EndDateWardStay IS NULL AND InactTimeWS IS NULL) THEN DATE_ADD('$rp_enddate',1)
                                          WHEN InactTimeWS IS NOT NULL THEN InactTimeWS
                                          ELSE EndDateWardStay END

# COMMAND ----------

 %sql
 ---get all valid/open healthcare provider records for the financial year
 DROP TABLE IF EXISTS $db_output.mhb_org_daily_v6;
 CREATE TABLE         $db_output.mhb_org_daily_v6 USING DELTA AS
 SELECT *
 FROM reference_data.org_daily
 WHERE (BUSINESS_END_DATE >= add_months('$rp_enddate', 1) OR ISNULL(BUSINESS_END_DATE))
   AND BUSINESS_START_DATE <= add_months('$rp_enddate', 1)
   AND ORG_TYPE_CODE NOT IN ('MP', 'IR', 'F', 'GO', 'CN'); ---not including MP constituency, social service inspectorate region, family practitioner committee, government office region or cancer network
   
 OPTIMIZE $db_output.mhb_org_daily_v6;

# COMMAND ----------

 %sql
 ---gets all valid orgs between the startdate and enddate widgets
 DROP TABLE IF EXISTS $db_output.mhb_rd_org_daily_latest_v6;
 CREATE TABLE  $db_output.mhb_rd_org_daily_latest_v6 USING DELTA AS
 SELECT               ORG_CODE,
                      NAME
 FROM                 $db_output.mhb_org_daily_v6
 WHERE                (BUSINESS_END_DATE >= '$rp_enddate' OR BUSINESS_END_DATE IS NULL)
                      AND ORG_TYPE_CODE != 'CC' --- not commissioning groups 
                      AND (ORG_CLOSE_DATE >= '$rp_enddate' OR ORG_CLOSE_DATE IS NULL)
                      AND ORG_OPEN_DATE <= '$rp_enddate'
 --                      AND NAME NOT LIKE '%HUB' ---exclude commissioning hubs
 --                      AND NAME NOT LIKE '%NATIONAL%';

# COMMAND ----------

# Code to create beddays_ended_ws_2324 table so only run if widgets set up for 23/24 run

print(rp_start, rp_enddate, month_id_start, month_id_end)
if month_id_start == '1477' and month_id_end == '1488' and rp_start == '2023-04-01' and '2024-03-31':
  print('code run to create/overwrite beddays_ended_ws_2324 table')
  spark.sql(f"""DROP TABLE IF EXISTS {db_output}.beddays_ended_ws_2324""")
  spark.sql(f"""CREATE TABLE         {db_output}.beddays_ended_ws_2324 AS

select  
  CASE 
  WHEN btp.HospitalBedTypeMH IN ('35','36','37','38') THEN '35'
  WHEN btp.HospitalBedTypeMH IN ('26') THEN '25'
  WHEN btp.HospitalBedTypeMH in ('10','11','12','13','14','15','17','19','20','21','22','23','24','25','27','28','30','34','35','36','37','38','39','40') 
  THEN btp.HospitalBedTypeMH
  ELSE 'Unknown' END AS HBTypeCleaned
, count(UniqWardStayID) as WardStays
, count(case when EndDateWardStay between '{rp_start}' and '{rp_enddate}' then UniqWardStayID end) as EndedWardStays
, count(case when bed_days_ws_full = 0 then UniqWardStayID end) as ZeroWardStays
, count(distinct Person_ID) as patients
, sum(beddays) as SumDaysInYear
, sum(bed_days_ws_full) as SumDays
, cast(avg(bed_days_ws_full) as decimal(5,1)) as MeanDays
, cast(avg(case when btp.HospitalBedTypeMH in ('19','20','21','27','28') then null
                  else case when bed_days_ws_full > 0 then bed_days_ws_full end end) as decimal(5,1)) as MeanDaysnoZ
, cast(avg(case when btp.HospitalBedTypeMH in ('19','20','21','27','28') then null
                  else case when bed_days_ws_full > 0 and bed_days_ws_full < WSend75th then bed_days_ws_full end end) as decimal(5,1)) as MeanDaysnoZLim75
, cast(avg(case when btp.HospitalBedTypeMH in ('19','20','21','27','28') then null
            else case when bed_days_ws_full = 0 or bed_days_ws_full is null then null  
            else case when bed_days_ws_full < WSend75th then bed_days_ws_full else WSend75th end end end) as decimal(5,1)) as MeanDaysnoZLim75b
, cast(avg(case when btp.HospitalBedTypeMH in ('19','20','21','27','28') then null
                  else case when bed_days_ws_full > 0 and bed_days_ws_full < WSend95th then bed_days_ws_full end end) as decimal(5,1)) as MeanDaysnoZLim95
, cast(avg(case when btp.HospitalBedTypeMH in ('19','20','21','27','28') then null
                  else case when bed_days_ws_full > 0 and bed_days_ws_full < WSend99th then bed_days_ws_full end end) as decimal(5,1)) as MeanDaysnoZLim99
, min(bed_days_ws_full) as MinDays
, max(bed_days_ws_full) as MaxDays
, percentile(bed_days_ws_full,0.5) as MedianDays
, percentile(bed_days_ws_full,0.75) - percentile(bed_days_ws_full,0.25) as IQR
, percentile(bed_days_ws_full,0.25) as LowerQuartile
, percentile(bed_days_ws_full,0.75) as UpperQuartile
--, percentile(bed_days_ws_full,0.75) + (1.5*(percentile(bed_days_ws_full,0.75) - percentile(bed_days_ws_full,0.25))) as TrimPoint
, percentile(case when btp.HospitalBedTypeMH in ('19','20','21','27','28') then null
                  else case when bed_days_ws_full > 0 then bed_days_ws_full end end,0.75) as TrimPointUQnoZ
, count(case when bed_days_ws_full > 0 then UniqWardStayID end) as CountNoZ
from bedtype_prov btp
inner join (
select case when HospitalBedTypeMH is null then 'Unknown' else HospitalBedTypeMH end as HospitalBedTypeMH
,cast(percentile(case when bed_days_ws_full > 0 then bed_days_ws_full end,0.95) as decimal(10,1)) as WSend95th
,cast(percentile(case when bed_days_ws_full > 0 then bed_days_ws_full end,0.99) as decimal(10,1)) as WSend99th
,cast(percentile(case when bed_days_ws_full > 0 then bed_days_ws_full end,0.75) as decimal(10,1)) as WSend75th
from bedtype_prov
group by case when HospitalBedTypeMH is null then 'Unknown' else HospitalBedTypeMH end 
)ptiles on ptiles.HospitalBedTypeMH = case when btp.HospitalBedTypeMH is null then 'Unknown' else btp.HospitalBedTypeMH end 
group by CASE 
  WHEN btp.HospitalBedTypeMH IN ('35','36','37','38') THEN '35'
  WHEN btp.HospitalBedTypeMH IN ('26') THEN '25'
  WHEN btp.HospitalBedTypeMH in ('10','11','12','13','14','15','17','19','20','21','22','23','24','25','27','28','30','34','35','36','37','38','39','40') 
  THEN btp.HospitalBedTypeMH
  ELSE 'Unknown' END """)

else:
  print('code by-passed - will use 23/24 beddays_ended_ws_2324 table')

# COMMAND ----------

 %sql

 select 
 HBTypeCleaned, MeanDaysnoZLim75b, TrimPointUQnoZ
 from $db_output.beddays_ended_ws_2324

# COMMAND ----------

 %sql --Output Excess bed days for 47 NHS trust providers Excess bed days, Non-Secure and Unknown bed types only

 select '$rp_start' as StartDate, '$rp_enddate' as EndDate
 , case when ProviderCode is null then 'England' else ProviderCode end as ProviderCode
 , case when ProviderType is null then 'England' else ProviderType end as ProviderType
 , 'NON-SECURE AND UNKNOWN BED TYPES' as HOSPITAL_BEDTYPE_CAT

 --UNSUPPRESSED OUTPUT
 , sum(WardStays) as WardStays
 , sum(ZeroLoSs) as ZeroLoSs
 , sum(BeddaysinYear) as BeddaysinYear
 , sum(ExcessBedDays) as ExcessBeddaysinYear
 , cast(sum(CostExcessBedDays) as decimal(15,0)) as CostExcessBedDays

 --SUPPRESSED OUTPUT
 , case when ProviderCode is not null then
 		case when sum(WardStays) < 5 or sum(WardStays) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(WardStays) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(WardStays) is null then cast('0' as string) else cast(sum(WardStays) as string) end end as WardStays
 , case when ProviderCode is not null then
 		case when sum(ZeroLoSs) < 5 or sum(ZeroLoSs) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(ZeroLoSs) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(ZeroLoSs) is null then cast('0' as string) else cast(sum(ZeroLoSs) as string) end end as ZeroLoSs
 , case when ProviderCode is not null then
 		case when sum(WardStays) < 5 or sum(BeddaysinYear) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(BeddaysinYear) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(BeddaysinYear) is null then cast('0' as string) else cast(sum(BeddaysinYear) as string) end end as BeddaysinYear
 , case when ProviderCode is not null then
 		case when sum(WardStays) < 5 or sum(ExcessBedDays) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(ExcessBedDays) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(ExcessBedDays) is null then cast('0' as string) else cast(sum(ExcessBedDays) as string) end end as ExcessBedDays
 , case when ProviderCode is not null then
 		case when sum(CostExcessBedDays) < 5 or sum(CostExcessBedDays) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(CostExcessBedDays) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(CostExcessBedDays) is null then cast('0' as string) 
                   else cast(cast(sum(CostExcessBedDays) as decimal(15,0)) as string) end end as CostExcessBedDays
 from (
 select 
 /*CASE WHEN OrgIDProv in ('RVN','RRP','RWX','RXT','TAJ','TAD','RT1','TAF','RV3','RXA','RJ8','RYG','RX4','RXM','RWV','RDY','RYK','RWK','R1L', 'RXV','RWR','RV9','RXY','RW5','RGD','RT5','RP7','RW4','RRE','RMY','RAT','RLY','RHA','RNU','RPG','RT2','RXE','TAH','RV5','RQY','RXG','RW1','RXX','RX2','RNK','RX3','RKL')
              THEN OrgIDProv
              ELSE 'Other providers' END as ProviderCode */
 OrgIDProv as ProviderCode
 , CASE WHEN OrgIDProv in ('RVN','RRP','RWX','RXT','TAJ','TAD','RT1','TAF','RV3','RXA','RJ8','RYG','RX4','RXM','RWV','RDY','RYK','RWK','R1L', 'RXV','RWR','RV9','RXY','RW5','RGD','RT5','RP7','RW4','RRE','RMY','RAT','RLY','RHA','RNU','RPG','RT2','RXE','TAH','RV5','RQY','RXG','RW1','RXX','RX2','RNK','RX3','RKL')  THEN 'Core Trust'
        WHEN left(OrgIDProv, 1) in ('R', 'T') THEN 'Other Trusts'
        ELSE 'Non-NHS providers' END as ProviderType             
 , CASE WHEN agg.HBTypeCleaned is not null THEN agg.HBTypeCleaned ELSE aggunk.HBTypeCleaned END as Hospital_Bed_Type 
 , CASE WHEN agg.HBTypeCleaned is not null THEN CASE WHEN agg.TrimPointUQnoZ is null THEN '-' ELSE agg.TrimPointUQnoZ END ELSE aggunk.TrimPointUQnoZ END as Trimpoint
 , count(distinct UniqWardStayID) as WardStays
 , count(distinct CASE WHEN bed_days_ws_full = 0 THEN UniqWardStayID END) as ZeroLoSs
 , count(case when EndDateWardStay between '$rp_start' and '$rp_enddate' then UniqWardStayID end) as EndedWardStays
 , sum(beddays) as BeddaysinYear
 , sum(bed_days_ws_full) as EndedBeddaysinYear
 , cast(avg(case when bed_days_ws_full >= 0 then bed_days_ws_full end) as decimal(5,1)) as MeanLoSdays
 , sum(CASE WHEN bed_days_ws_full = 0 THEN 0   --Zero LoS record as zero activity here and assign costs afterwards
        WHEN agg.TrimPointUQnoZ is null and agg.HBTypeCleaned is not null THEN beddays
        WHEN agg.HBTypeCleaned is not null
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - agg.TrimPointUQnoZ, 0) 
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(agg.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, agg.TrimPointUQnoZ) - agg.TrimPointUQnoZ,0)  
                  END
        WHEN agg.HBTypeCleaned is null  --HBT doesn't have cost so group toegther
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - aggunk.TrimPointUQnoZ, 0)
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(aggunk.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, aggunk.TrimPointUQnoZ) - aggunk.TrimPointUQnoZ,0)  
                  END
        ELSE null END) as ExcessBedDays
 , sum(CASE WHEN bed_days_ws_full = 0 THEN 0   --Zero LoS record as zero activity here and assign costs afterwards
        WHEN agg.TrimPointUQnoZ is null and agg.HBTypeCleaned is not null THEN beddays
        WHEN agg.HBTypeCleaned is not null
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - agg.TrimPointUQnoZ, 0) 
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(agg.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, agg.TrimPointUQnoZ) - agg.TrimPointUQnoZ,0)  
                  END
        WHEN agg.HBTypeCleaned is null  --HBT doesn't have cost so group toegther
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - aggunk.TrimPointUQnoZ, 0)
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(aggunk.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, aggunk.TrimPointUQnoZ) - aggunk.TrimPointUQnoZ,0)  
                  END
        ELSE null END)
        * 711.52 --Blanket bed day cost 
        as CostExcessBedDays
 from (
 select OrgIDProv, Person_ID, UniqWardStayID, StartDateWardStay, EndDateWardStay, HospitalBedTypeMH, InactTimeWS, EndOrInactDate
 , beddays, bed_days_ws_full, EndedDistinctWardStaysinYear, EndedWardStaysinYear
 from bedtype_prov 
 where HospitalBedTypeMH in ('10','11','12','13','14','15','17','22','23','24','25','30','34','35','36','37','38','39','40') --Non-secure beds only
 or (HospitalBedTypeMH not in ('10','11','12','13','14','15','17','22','23','24','25','30','34','35','36','37','38','39','40','19','20','21','27','28') or HospitalBedTypeMH is null)  --Unknown 
 ) bed
 left join $db_output.beddays_ended_ws_2324 agg on bed.HospitalBedTypeMH = agg.HBTypeCleaned 
 left join $db_output.beddays_ended_ws_2324 aggunk on aggunk.HBTypeCleaned = 'Unknown'
 group by rollup((OrgIDProv
        , CASE WHEN OrgIDProv in ('RVN','RRP','RWX','RXT','TAJ','TAD','RT1','TAF','RV3','RXA','RJ8','RYG','RX4','RXM','RWV','RDY','RYK','RWK','R1L', 'RXV','RWR','RV9','RXY','RW5','RGD','RT5','RP7','RW4','RRE','RMY','RAT','RLY','RHA','RNU','RPG','RT2','RXE','TAH','RV5','RQY','RXG','RW1','RXX','RX2','RNK','RX3','RKL')  THEN 'Core Trust'
        WHEN left(OrgIDProv, 1) in ('R', 'T') THEN 'Other Trusts'
        ELSE 'Non-NHS providers' END 
        , CASE WHEN agg.HBTypeCleaned is not null THEN agg.HBTypeCleaned ELSE aggunk.HBTypeCleaned END 
        , CASE WHEN agg.HBTypeCleaned is not null THEN CASE WHEN agg.TrimPointUQnoZ is null THEN '-' ELSE agg.TrimPointUQnoZ END ELSE aggunk.TrimPointUQnoZ END))
 )
 group by ProviderCode, ProviderType  
 order by  ProviderType, ProviderCode  

# COMMAND ----------

# DBTITLE 1,CWA output - to pivot in the format needed
 %sql --Output Cost Weighted Activity for 47 NHS trust providers split by Secure, Non-Secure and Unknown bed types 

 DROP TABLE IF EXISTS $db_output.cwa_output;
 CREATE TABLE         $db_output.cwa_output USING DELTA AS

 select '$rp_start' as StartDate, '$rp_enddate' as EndDate
 , case when ProviderCode is null then 'England' else ProviderCode end as ProviderCode
 , case when ProviderType is null then 'England' else ProviderType end as ProviderType
 , CASE WHEN ProviderCode is null THEN 'ALL BED TYPES'
        WHEN Hospital_Bed_Type in ('19','20','21','27','28') THEN 'SECURE' 
        WHEN Hospital_Bed_Type in ('10','11','12','13','14','15','17','22','23','24','25','30','34','35','36','37','38','39','40') THEN 'NON-SECURE' 
        ELSE 'UNKNOWN' END AS HOSPITAL_BEDTYPE_CAT

 --UNSUPPRESSED OUTPUT
 /*, sum(WardStays) as WardStays
 , sum(ZeroLoSs) as ZeroLoSs
 , sum(BeddaysinYear) as BeddaysinYear
 , sum(ExcessBedDays) as ExcessBeddaysinYear
 , cast(sum(CostExcessBedDays) as decimal(15,0)) as CostExcessBedDays
 , cast(sum(Model4CWA) as decimal(15,0)) as CWA75thpcttile
 , cast(sum(FullrecognitionCWA) as decimal(15,0)) as FullrecognitionCWA */

 --SUPPRESSED OUTPUT
 , case when ProviderCode is not null then
 		case when sum(WardStays) < 5 or sum(WardStays) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(WardStays) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(WardStays) is null then cast('0' as string) else cast(sum(WardStays) as string) end end as WardStays
 , case when ProviderCode is not null then
 		case when sum(ZeroLoSs) < 5 or sum(ZeroLoSs) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(ZeroLoSs) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(ZeroLoSs) is null then cast('0' as string) else cast(sum(ZeroLoSs) as string) end end as ZeroLoSs
 , case when ProviderCode is not null then
 		case when sum(WardStays) < 5 or sum(BeddaysinYear) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(BeddaysinYear) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(BeddaysinYear) is null then cast('0' as string) else cast(sum(BeddaysinYear) as string) end end as BeddaysinYear
 , case when ProviderCode is not null then
 		case when sum(WardStays) < 5 or sum(ExcessBedDays) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(ExcessBedDays) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(ExcessBedDays) is null then cast('0' as string) else cast(sum(ExcessBedDays) as string) end end as ExcessBedDays
 , case when ProviderCode is not null then
 		case when sum(CostExcessBedDays) < 5 or sum(CostExcessBedDays) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(CostExcessBedDays) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(CostExcessBedDays) is null then cast('0' as string) 
                   else cast(cast(sum(CostExcessBedDays) as decimal(15,0)) as string) end end as CostExcessBedDays
 , case when ProviderCode is not null then
 		case when sum(Model4CWA) < 5 or sum(Model4CWA) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(Model4CWA) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(Model4CWA) is null then cast('0' as string) else cast(cast(sum(Model4CWA) as decimal(15,0)) as string) end end as CWA75thpcttile
 , case when ProviderCode is not null then
 		case when sum(FullrecognitionCWA) < 5 or sum(FullrecognitionCWA) is null then cast('*' as string)
 		else cast(cast(round((cast(cast(sum(FullrecognitionCWA) as decimal) as int))/5.0,0) * 5 as int) as string) end 
         else case when sum(FullrecognitionCWA) is null then cast('0' as string) 
                   else cast(cast(sum(FullrecognitionCWA) as decimal(15,0)) as string) end end as FullrecognitionCWA
 from (
 select 
 /*CASE WHEN OrgIDProv in ('RVN','RRP','RWX','RXT','TAJ','TAD','RT1','TAF','RV3','RXA','RJ8','RYG','RX4','RXM','RWV','RDY','RYK','RWK','R1L', 'RXV','RWR','RV9','RXY','RW5','RGD','RT5','RP7','RW4','RRE','RMY','RAT','RLY','RHA','RNU','RPG','RT2','RXE','TAH','RV5','RQY','RXG','RW1','RXX','RX2','RNK','RX3','RKL')
              THEN OrgIDProv
              ELSE 'Other providers' END as ProviderCode */
 OrgIDProv as ProviderCode
 , CASE WHEN OrgIDProv in ('RVN','RRP','RWX','RXT','TAJ','TAD','RT1','TAF','RV3','RXA','RJ8','RYG','RX4','RXM','RWV','RDY','RYK','RWK','R1L', 'RXV','RWR','RV9','RXY','RW5','RGD','RT5','RP7','RW4','RRE','RMY','RAT','RLY','RHA','RNU','RPG','RT2','RXE','TAH','RV5','RQY','RXG','RW1','RXX','RX2','RNK','RX3','RKL')  THEN 'Core Trust'
        WHEN left(OrgIDProv, 1) in ('R', 'T') THEN 'Other Trusts'
        ELSE 'Non-NHS providers' END as ProviderType             
 , CASE WHEN agg.HBTypeCleaned is not null THEN agg.HBTypeCleaned ELSE aggunk.HBTypeCleaned END as Hospital_Bed_Type 
 , CASE WHEN agg.HBTypeCleaned is not null THEN CASE WHEN agg.TrimPointUQnoZ is null THEN '-' ELSE agg.TrimPointUQnoZ END ELSE aggunk.TrimPointUQnoZ END as Trimpoint
 , count(distinct UniqWardStayID) as WardStays
 , count(distinct CASE WHEN bed_days_ws_full = 0 THEN UniqWardStayID END) as ZeroLoSs
 , sum(beddays) as BeddaysinYear
 , cast(avg(case when bed_days_ws_full >= 0 then bed_days_ws_full end) as decimal(5,1)) as MeanDays
 , sum(CASE WHEN bed_days_ws_full = 0 THEN 0   --Zero LoS record as zero activity here and assign costs afterwards
        WHEN agg.TrimPointUQnoZ is null and agg.HBTypeCleaned is not null THEN beddays
        WHEN agg.HBTypeCleaned is not null
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - agg.TrimPointUQnoZ, 0) 
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(agg.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, agg.TrimPointUQnoZ) - agg.TrimPointUQnoZ,0)  
                  END
        WHEN agg.HBTypeCleaned is null  --HBT doesn't have cost so group toegther
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - aggunk.TrimPointUQnoZ, 0)
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(aggunk.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, aggunk.TrimPointUQnoZ) - aggunk.TrimPointUQnoZ,0)  
                  END
        ELSE null END) as ExcessBedDays
 , sum(CASE WHEN bed_days_ws_full = 0 THEN 0   --Zero LoS record as zero activity here and assign costs afterwards
        WHEN agg.TrimPointUQnoZ is null and agg.HBTypeCleaned is not null THEN beddays
        WHEN agg.HBTypeCleaned is not null
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - agg.TrimPointUQnoZ, 0) 
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(agg.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, agg.TrimPointUQnoZ) - agg.TrimPointUQnoZ,0)  
                  END
        WHEN agg.HBTypeCleaned is null  --HBT doesn't have cost so group toegther
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - aggunk.TrimPointUQnoZ, 0)
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(beddays - greatest(aggunk.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, aggunk.TrimPointUQnoZ) - aggunk.TrimPointUQnoZ,0)  
                  END
        ELSE null END)
        * 711.52 --Blanket bed day cost 
        as CostExcessBedDays
 , sum((CASE WHEN bed_days_ws_full = 0 THEN 0   --Zero LoS record as zero activity here and assign costs afterwards
        WHEN agg.TrimPointUQnoZ is null and agg.HBTypeCleaned is not null THEN beddays
        WHEN agg.HBTypeCleaned is not null
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN case when beddays <= agg.TrimPointUQnoZ then agg.MeanDaysnoZLim75b
                            else agg.MeanDaysnoZLim75b + 0.5*greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - agg.TrimPointUQnoZ, 0) end
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(agg.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay), 0) * agg.MeanDaysnoZLim75b / agg.TrimPointUQnoZ
                       + 0.5*greatest(beddays - greatest(agg.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN least(datediff('$rp_enddate', StartDateWardStay)+1, agg.TrimPointUQnoZ) * agg.MeanDaysnoZLim75b / agg.TrimPointUQnoZ 
                       + 0.5*greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, agg.TrimPointUQnoZ) - agg.TrimPointUQnoZ,0)  
                  END
        WHEN agg.HBTypeCleaned is null  --HBT doesn't have cost so group toegther
        THEN CASE WHEN StartDateWardStay >= '$rp_start' and coalesce(EndDateWardStay,InactTimeWS) <= '$rp_enddate'  
                  THEN case when beddays <= aggunk.TrimPointUQnoZ then aggunk.MeanDaysnoZLim75b
                         else aggunk.MeanDaysnoZLim75b + 0.5*greatest(datediff(coalesce(EndDateWardStay,InactTimeWS), StartDateWardStay) - aggunk.TrimPointUQnoZ, 0) end
                  WHEN StartDateWardStay < '$rp_start' 
                  THEN greatest(aggunk.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay), 0) * aggunk.MeanDaysnoZLim75b / aggunk.TrimPointUQnoZ
                       + 0.5*greatest(beddays - greatest(aggunk.TrimPointUQnoZ - datediff('$rp_start', StartDateWardStay),0), 0)                    
                  WHEN StartDateWardStay >= '$rp_start' and (coalesce(EndDateWardStay,InactTimeWS) > '$rp_enddate' or coalesce(EndDateWardStay,InactTimeWS) is null) 
                  THEN least(datediff('$rp_enddate', StartDateWardStay)+1, aggunk.TrimPointUQnoZ) * aggunk.MeanDaysnoZLim75b / aggunk.TrimPointUQnoZ 
                       + 0.5*greatest(greatest(datediff('$rp_enddate', StartDateWardStay)+1, aggunk.TrimPointUQnoZ) - aggunk.TrimPointUQnoZ,0)  
                  END
        ELSE null END))  
       * 711.52  --Blanket bed day cost for all bed types
       + count(CASE WHEN bed_days_ws_full = 0 THEN UniqWardStayID END)*302 as Model4CWA 
 , sum((CASE WHEN bed_days_ws_full = 0 THEN 0   --Zero LoS record as zero activity here and assign costs afterwards
             ELSE beddays END) 
       * 711.52  --single 23/24 cost
       ) + count(CASE WHEN bed_days_ws_full = 0 THEN UniqWardStayID END)*302 as FullrecognitionCWA
 from (
 select OrgIDProv, Person_ID, UniqWardStayID, StartDateWardStay, EndDateWardStay, HospitalBedTypeMH, InactTimeWS, EndOrInactDate
 , beddays, bed_days_ws_full, EndedDistinctWardStaysinYear, EndedWardStaysinYear
 from bedtype_prov 
 ) bed
 left join $db_output.beddays_ended_ws_2324 agg on bed.HospitalBedTypeMH = agg.HBTypeCleaned 
 left join $db_output.beddays_ended_ws_2324 aggunk on aggunk.HBTypeCleaned = 'Unknown'
 group by rollup((OrgIDProv
        , CASE WHEN OrgIDProv in ('RVN','RRP','RWX','RXT','TAJ','TAD','RT1','TAF','RV3','RXA','RJ8','RYG','RX4','RXM','RWV','RDY','RYK','RWK','R1L', 'RXV','RWR','RV9','RXY','RW5','RGD','RT5','RP7','RW4','RRE','RMY','RAT','RLY','RHA','RNU','RPG','RT2','RXE','TAH','RV5','RQY','RXG','RW1','RXX','RX2','RNK','RX3','RKL')  THEN 'Core Trust'
        WHEN left(OrgIDProv, 1) in ('R', 'T') THEN 'Other Trusts'
        ELSE 'Non-NHS providers' END 
        , CASE WHEN agg.HBTypeCleaned is not null THEN agg.HBTypeCleaned ELSE aggunk.HBTypeCleaned END 
        , CASE WHEN agg.HBTypeCleaned is not null THEN CASE WHEN agg.TrimPointUQnoZ is null THEN '-' ELSE agg.TrimPointUQnoZ END ELSE aggunk.TrimPointUQnoZ END))
 )
 group by ProviderCode, ProviderType  
 , CASE WHEN ProviderCode is null THEN 'ALL BED TYPES'
        WHEN Hospital_Bed_Type in ('19','20','21','27','28') THEN 'SECURE' 
        WHEN Hospital_Bed_Type in ('10','11','12','13','14','15','17','22','23','24','25','30','34','35','36','37','38','39','40') THEN 'NON-SECURE' 
        ELSE 'UNKNOWN' END 
 order by  ProviderType , ProviderCode, CASE WHEN HOSPITAL_BEDTYPE_CAT = 'SECURE' THEN 1 ELSE 2 END, HOSPITAL_BEDTYPE_CAT

# COMMAND ----------

 %sql

 CREATE OR REPLACE TEMPORARY VIEW mh_prod_org_daily as

 SELECT 
 ORG_CODE,
 NAME
 from
 (
 select distinct ORG_CODE,  NAME,
 row_number() over(partition by org_code order by case when org_is_current = 1 then 0 else 1 end asc, case when business_end_date is null then 0 else 1 end asc
                                                   ,business_end_date desc, business_start_date desc) as rank
 from reference_data.org_daily 
 )
 where rank = 1

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.mh_cwa_output;
 CREATE TABLE         $db_output.mh_cwa_output USING DELTA AS

 select a.*, NAME 
 from $db_output.cwa_output a 
 left join mh_prod_org_daily b on a.ProviderCode = b.ORG_CODE


# COMMAND ----------

# DBTITLE 1,formatted CWA output to export
 %py
 import pandas as pd 
 import numpy as np

 db_output = dbutils.widgets.get("db_output")

 df = spark.table(f'{db_output}.mh_cwa_output').toPandas()

 output = df.pivot_table(
     index= ['ProviderType','ProviderCode', 'NAME' ],
     columns='HOSPITAL_BEDTYPE_CAT',
     values=['CWA75thpcttile', 'FullrecognitionCWA'])

 pivot_df = pd.DataFrame(output)
 pivot_final = pivot_df.reset_index()

 pivot_final.columns = ['_'.join(str(s).strip() for s in col if s) for col in pivot_final.columns]

 pivot_final.rename(columns = {'CWA75thpcttile_NON-SECURE':'IP_Non_Secure_Beds',                            
                                         'FullrecognitionCWA_NON-SECURE':'IP_Non_Secure_Beds_Full_recognition',
                                          'FullrecognitionCWA_SECURE':'IP_Secure_Beds','FullrecognitionCWA_UNKNOWN':'IP_Bed_Type_Unknown_Full_recognition'}, inplace = True)

 cwa_final = pivot_final[['ProviderType', 'ProviderCode', 'NAME', 'IP_Secure_Beds', 'IP_Non_Secure_Beds', 'IP_Bed_Type_Unknown_Full_recognition', 'IP_Non_Secure_Beds_Full_recognition']]
 display(cwa_final)


# COMMAND ----------

 %py

 df = spark.createDataFrame(cwa_final)

 df.createOrReplaceTempView("CWA_Final")

# COMMAND ----------

 %sql
 CREATE OR REPLACE TABLE $db_output.MH_Inpatient_CWA USING DELTA AS 

 select * 
 from CWA_Final