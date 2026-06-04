# Databricks notebook source
# DBTITLE 1,Sub-National and National Age Band Population - Uses Latest Mid-Year Estimates
 %sql
 INSERT OVERWRITE TABLE $db_output.age_band_pop
 SELECT 
 a.AGE_GROUP, 
 COALESCE(B.CCG_CODE, A.CCG_CODE) AS CCG_CODE,
 COALESCE(B.CCG_NAME, A.CCG_NAME) AS CCG_NAME,
 COALESCE(B.STP_CODE, A.STP_CODE) AS STP_CODE,
 COALESCE(B.STP_NAME, A.STP_NAME) AS STP_NAME,
 COALESCE(B.REGION_CODE, A.REGION_CODE) AS REGION_CODE,
 COALESCE(B.REGION_NAME, A.REGION_NAME) AS REGION_NAME,
 a.Age_Group_IPS, 
 a.Age_Group_OAPs,
 a.Age_Group_MHA,
 a.Age_Group_CYP,
 a.Age_Group_Higher_Level,
 A.POPULATION_COUNT * COALESCE(B.POPULATION_FACTOR, 1) AS POPULATION_COUNT
 FROM
 (select 
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end as Age_Group,
 COALESCE(stp.CCG_Code, 'UNKNOWN') as CCG_Code,
 COALESCE(stp.CCG_Name, 'UNKNOWN') as CCG_Name,
 COALESCE(stp.STP_Code, 'UNKNOWN') as STP_Code,
 COALESCE(stp.STP_Name, 'UNKNOWN') as STP_Name,
 COALESCE(stp.Region_Code, 'UNKNOWN') as Region_Code,
 COALESCE(stp.Region_Name, 'UNKNOWN') as Region_Name,
 a.Age_Group_IPS, 
 a.Age_Group_OAPs,
 a.Age_Group_MHA,
 a.Age_Group_CYP,
 a.Age_Group_Higher_Level,
 ---Need to add new age groups here whenever new ones are added in
 SUM(p.POPULATION_COUNT) as POPULATION_COUNT 
  
 from $reference_data.ons_population_v2 p
 left join $reference_data.ons_chd_geo_equivalents ons on p.GEOGRAPHIC_SUBGROUP_CODE = ons.GEOGRAPHY_CODE and left(ons.GEOGRAPHY_CODE, 3) = "E38" and YEAR_OF_CHANGE in (2022, 2023) and (DATE_OF_TERMINATION is null or DATE_OF_TERMINATION between '2024-04-01' and '2026-03-31') --Sets ONS mappings to the 25-26 mapping so this can be left until the population data is available
 left join $db_output.bbrb_stp_mapping stp on ons.DH_GEOGRAPHY_CODE = stp.CCG_CODE ---map ccg to stp/region level
 left join $db_output.age_band_desc a on p.AGE_LOWER = a.AgeRepPeriodEnd and '$end_month_id' >= a.FirstMonth and (a.LastMonth is null or '$end_month_id' <= a.LastMonth)
 where year_of_count = (select max(year_of_count) from $reference_data.ons_population_v2 where GEOGRAPHIC_GROUP_CODE = 'E38') ---looks at latest data rather than depending on what month is being ran
 and GEOGRAPHIC_GROUP_CODE = 'E38' ---ccg-level population
 group by 
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end,
 stp.CCG_Code, stp.CCG_Name, stp.STP_Code, stp.STP_Name, stp.Region_Code, stp.Region_Name, a.Age_Group_IPS, a.Age_Group_OAPs, a.Age_Group_MHA, a.Age_Group_CYP, a.Age_Group_Higher_Level)
 AS A
 LEFT JOIN $db_output.commissioning_org_mapping AS B ON A.CCG_CODE = B.ORIGINAL_CCG_CODE and '$end_month_id' >= '$apr26_icb_swap_month_id' 

# COMMAND ----------

# DBTITLE 1,Sub-National and National Gender Population - Uses Latest Mid-Year Estimates
 %sql
 INSERT OVERWRITE TABLE $db_output.gender_pop
 SELECT
 AGE_GROUP, 
 COALESCE(B.CCG_CODE, A.CCG_CODE) AS CCG_CODE,
 COALESCE(B.CCG_NAME, A.CCG_NAME) AS CCG_NAME,
 COALESCE(B.STP_CODE, A.STP_CODE) AS STP_CODE,
 COALESCE(B.STP_NAME, A.STP_NAME) AS STP_NAME,
 COALESCE(B.REGION_CODE, A.REGION_CODE) AS REGION_CODE,
 COALESCE(B.REGION_NAME, A.REGION_NAME) AS REGION_NAME,
 a.Der_Gender,
 a.Der_Gender_Desc,
 A.POPULATION_COUNT * COALESCE(B.POPULATION_FACTOR, 1) AS POPULATION_COUNT
 FROM 
 (select 
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end as Age_Group,
 COALESCE(stp.CCG_Code, 'UNKNOWN') as CCG_Code,
 COALESCE(stp.CCG_Name, 'UNKNOWN') as CCG_Name,
 COALESCE(stp.STP_Code, 'UNKNOWN') as STP_Code,
 COALESCE(stp.STP_Name, 'UNKNOWN') as STP_Name,
 COALESCE(stp.Region_Code, 'UNKNOWN') as Region_Code,
 COALESCE(stp.Region_Name, 'UNKNOWN') as Region_Name,
 gen.Der_Gender,
 gen.Der_Gender_Desc,
 SUM(POPULATION_COUNT) as POPULATION_COUNT    
  
 from $reference_data.ons_population_v2 p
 left join $reference_data.ons_chd_geo_equivalents ons on p.GEOGRAPHIC_SUBGROUP_CODE = ons.GEOGRAPHY_CODE and left(ons.GEOGRAPHY_CODE, 3) = "E38" and YEAR_OF_CHANGE in (2022, 2023) and (DATE_OF_TERMINATION is null or DATE_OF_TERMINATION between '2024-04-01' and '2026-03-31') --Sets ONS mappings to the 25-26 mapping so this can be left until the population data is available
 left join $db_output.bbrb_stp_mapping stp on ons.DH_GEOGRAPHY_CODE = stp.CCG_CODE ---map ccg to stp/region level
 left join $db_output.gender_desc gen
   on case when p.GENDER = "M" then 1
      when p.GENDER = "F" then 2
      end = gen.Der_Gender
    and '$end_month_id' >= gen.FirstMonth and (gen.LastMonth is null or '$end_month_id' <= gen.LastMonth)
 where year_of_count = (select max(year_of_count) from $reference_data.ons_population_v2 where GEOGRAPHIC_GROUP_CODE = 'E38') ---looks at latest data rather than depending on what month is being ran $$$
 and GEOGRAPHIC_GROUP_CODE = 'E38'
 group by case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end,
 stp.CCG_Code, stp.CCG_Name, stp.STP_Code, stp.STP_Name, stp.Region_Code, stp.Region_Name, gen.Der_Gender, gen.Der_Gender_Desc)
 AS A
 LEFT JOIN $db_output.commissioning_org_mapping AS B ON A.CCG_CODE = B.ORIGINAL_CCG_CODE and '$end_month_id' >= '$apr26_icb_swap_month_id' 

# COMMAND ----------

# DBTITLE 1,Sub-National and National Gender Population - Uses Census 2021 data
 %sql
 INSERT OVERWRITE TABLE $db_output.eth_pop
 SELECT 
 AGE_GROUP, 
 COALESCE(B.CCG_CODE, A.CCG_CODE) AS CCG_CODE,
 COALESCE(B.CCG_NAME, A.CCG_NAME) AS CCG_NAME,
 COALESCE(B.STP_CODE, A.STP_CODE) AS STP_CODE,
 COALESCE(B.STP_NAME, A.STP_NAME) AS STP_NAME,
 COALESCE(B.REGION_CODE, A.REGION_CODE) AS REGION_CODE,
 COALESCE(B.REGION_NAME, A.REGION_NAME) AS REGION_NAME,
 a.LowerEthnicityCode,
 a.LowerEthnicityName,
 a.UpperEthnicity,
 a.WNWEthnicity,
 A.POPULATION_COUNT * COALESCE(B.POPULATION_FACTOR, 1) AS POPULATION_COUNT
 FROM
 (select 
 case when (c.age_code > 17 and c.age_code < 65) then "18-64"
      when c.age_code > 64 then "65+"
      when c.age_code < 18 then "0-17" end as Age_Group,
 COALESCE(stp.CCG_Code, 'UNKNOWN') as CCG_Code,
 COALESCE(stp.CCG_Name, 'UNKNOWN') as CCG_Name,
 COALESCE(stp.STP_Code, 'UNKNOWN') as STP_Code,
 COALESCE(stp.STP_Name, 'UNKNOWN') as STP_Name,
 COALESCE(stp.Region_Code, 'UNKNOWN') as Region_Code,
 COALESCE(stp.Region_Name, 'UNKNOWN') as Region_Name,
 eth.LowerEthnicityCode,
 eth.LowerEthnicityName,
 eth.UpperEthnicity,
 eth.WNWEthnicity,
 sum(observation) as POPULATION_COUNT
  
 from $reference_data.ons_2021_census c
 left join (SELECT *
 FROM $reference_data.ONS_CHD_GEO_EQUIVALENTS AS od
 WHERE DATE_OF_OPERATION = (SELECT MAX(DATE_OF_OPERATION) FROM $reference_data.ONS_CHD_GEO_EQUIVALENTS AS od2 WHERE od.GEOGRAPHY_CODE = od2.GEOGRAPHY_CODE and od2.DATE_OF_OPERATION < '2026-04-01')) od --Added date of operation here to try and force it to keep 
 on c.area_type_code = od.GEOGRAPHY_CODE and area_type_group_code = "E38"
 left join $db_output.bbrb_stp_mapping stp on od.DH_GEOGRAPHY_CODE = stp.CCG_CODE ---map ccg to stp/region level
 left join $db_output.ethnicity_desc eth on c.ethnic_group_code = eth.Census21EthnicityCode
 where area_type_group_code = "E38" ---Sub ICB grouping only
 and ethnic_group_code != -8 ---exclude does not apply ethnicity
 and ons_date = (select max(ons_date) from $reference_data.ons_2021_census where area_type_group_code = "E38")
 group by case when (c.age_code > 17 and c.age_code < 65) then "18-64"
      when c.age_code > 64 then "65+"
      when c.age_code < 18 then "0-17" end,
 stp.CCG_Code, stp.CCG_Name, stp.STP_Code, stp.STP_Name, stp.Region_Code, stp.Region_Name, eth.LowerEthnicityCode, eth.LowerEthnicityName, eth.UpperEthnicity, eth.WNWEthnicity)
 AS A
 LEFT JOIN $db_output.commissioning_org_mapping AS B ON A.CCG_CODE = B.ORIGINAL_CCG_CODE and '$end_month_id' >= '$apr26_icb_swap_month_id' 

# COMMAND ----------

# DBTITLE 1,Latest Mid-Year Estimates at Lower Super Output Area (LSOA) level to get IMD values
 %sql
 create or replace temp view lsoa_imd_pop as
 select
 c.gender,
 c.age_lower,
 c.GEOGRAPHIC_SUBGROUP_CODE,
 COALESCE(DEC.IMD_Decile,'UNKNOWN') AS IMD_Decile,
 COALESCE(DEC.IMD_Quintile,'UNKNOWN') AS IMD_Quintile,
 COALESCE(DEC.IMD_Core20, 'UNKNOWN') AS IMD_Core20,
 c.POPULATION_COUNT
 FROM $reference_data.ons_population_v2 c
 INNER JOIN (SELECT MAX(YEAR_OF_COUNT) AS MAX_YEAR FROM $reference_data.ons_population_v2) AS c1 on c.YEAR_OF_COUNT = c1.MAX_YEAR
 INNER JOIN (SELECT YEAR_OF_COUNT, MAX(DSS_SYSTEM_CREATED_DATE) AS MAX_CREATED_DATE FROM $reference_data.ons_population_v2 group by YEAR_OF_COUNT) AS c2 on c1.MAX_YEAR = c2.YEAR_OF_COUNT AND c.DSS_SYSTEM_CREATED_DATE = c2.MAX_CREATED_DATE
 LEFT JOIN $reference_data.english_indices_of_dep_v02 r on c.GEOGRAPHIC_SUBGROUP_CODE = r.LSOA_CODE_2011 AND c.GEOGRAPHIC_GROUP_CODE = "E01" AND r.IMD_YEAR = '2019'
 LEFT JOIN $db_output.imd_desc DEC on r.DECI_IMD = DEC.IMD_Number and '$end_month_id' >= DEC.FirstMonth and (DEC.LastMonth is null or '$end_month_id' <= DEC.LastMonth)
 WHERE c.GEOGRAPHIC_GROUP_CODE= "E01" 

# COMMAND ----------

# DBTITLE 1,Latest LSOA to CCG mappings based on postcode
 %sql
 create or replace temporary view ons_lsoa_to_ccg as
 select distinct LSOA11, CCG 
  
 from $reference_data.postcode 
 where LEFT(LSOA11, 3) = "E01"
 --pick records that were valid for 25-26
 and (RECORD_END_DATE >= '2026-03-31' OR RECORD_END_DATE IS NULL)    
 and RECORD_START_DATE <= '2026-03-31'
 order by LSOA11

# COMMAND ----------

# DBTITLE 1,Sub-National and National IMD Population - Uses Latest Mid-Year Estimates
 %sql
 INSERT OVERWRITE TABLE $db_output.imd_pop
 SELECT 
 AGE_GROUP, 
 COALESCE(B.CCG_CODE, A.CCG_CODE) AS CCG_CODE,
 COALESCE(B.CCG_NAME, A.CCG_NAME) AS CCG_NAME,
 COALESCE(B.STP_CODE, A.STP_CODE) AS STP_CODE,
 COALESCE(B.STP_NAME, A.STP_NAME) AS STP_NAME,
 COALESCE(B.REGION_CODE, A.REGION_CODE) AS REGION_CODE,
 COALESCE(B.REGION_NAME, A.REGION_NAME) AS REGION_NAME,
 a.IMD_Decile,
 a.IMD_Quintile,
 a.IMD_Core20,
 A.POPULATION_COUNT * COALESCE(B.POPULATION_FACTOR, 1) AS POPULATION_COUNT
 FROM
 (SELECT
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end as Age_Group,
 COALESCE(stp.CCG_Code, 'UNKNOWN') as CCG_Code,
 COALESCE(stp.CCG_Name, 'UNKNOWN') as CCG_Name,
 COALESCE(stp.STP_Code, 'UNKNOWN') as STP_Code,
 COALESCE(stp.STP_Name, 'UNKNOWN') as STP_Name,
 COALESCE(stp.Region_Code, 'UNKNOWN') as Region_Code,
 COALESCE(stp.Region_Name, 'UNKNOWN') as Region_Name,     
 p.IMD_Decile,
 p.IMD_Quintile,
 p.IMD_Core20,
 SUM(p.POPULATION_COUNT) as POPULATION_COUNT
 from lsoa_imd_pop p
 left join ons_lsoa_to_ccg ccg on p.GEOGRAPHIC_SUBGROUP_CODE = ccg.LSOA11
 left join $db_output.bbrb_stp_mapping stp on ccg.CCG = stp.CCG_CODE  ---map ccg to stp/region level
 group by case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end,
 COALESCE(stp.CCG_Code, 'UNKNOWN'), COALESCE(stp.CCG_Name, 'UNKNOWN'), COALESCE(stp.STP_Code, 'UNKNOWN'), COALESCE(stp.STP_Name, 'UNKNOWN'), COALESCE(stp.Region_Code, 'UNKNOWN'), COALESCE(stp.Region_Name, 'UNKNOWN'), p.IMD_Decile, p.IMD_Quintile, p.IMD_Core20)
 AS A
 LEFT JOIN $db_output.commissioning_org_mapping AS B ON A.CCG_CODE = B.ORIGINAL_CCG_CODE and '$end_month_id' >= '$apr26_icb_swap_month_id' 

# COMMAND ----------

# DBTITLE 1,Sub-National Population (CCG, STP and Region) - Uses Latest Mid-Year Estimates
 %sql
 INSERT OVERWRITE TABLE $db_output.commissioner_pop
 SELECT
 AGE_GROUP, 
 COALESCE(B.CCG_CODE, A.CCG_CODE) AS CCG_CODE,
 COALESCE(B.CCG_NAME, A.CCG_NAME) AS CCG_NAME,
 COALESCE(B.STP_CODE, A.STP_CODE) AS STP_CODE,
 COALESCE(B.STP_NAME, A.STP_NAME) AS STP_NAME,
 COALESCE(B.REGION_CODE, A.REGION_CODE) AS REGION_CODE,
 COALESCE(B.REGION_NAME, A.REGION_NAME) AS REGION_NAME,
 A.POPULATION_COUNT * COALESCE(B.POPULATION_FACTOR, 1) AS POPULATION_COUNT
 FROM
 (select 
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end as Age_Group,
 COALESCE(stp.CCG_Code, 'UNKNOWN') as CCG_Code,
 COALESCE(stp.CCG_Name, 'UNKNOWN') as CCG_Name,
 COALESCE(stp.STP_Code, 'UNKNOWN') as STP_Code,
 COALESCE(stp.STP_Name, 'UNKNOWN') as STP_Name,
 COALESCE(stp.Region_Code, 'UNKNOWN') as Region_Code,
 COALESCE(stp.Region_Name, 'UNKNOWN') as Region_Name,
 SUM(p.POPULATION_COUNT) as POPULATION_COUNT 
  
 from $reference_data.ons_population_v2 p
 left join $reference_data.ons_chd_geo_equivalents ons on p.GEOGRAPHIC_SUBGROUP_CODE = ons.GEOGRAPHY_CODE and left(ons.GEOGRAPHY_CODE, 3) = "E38" and YEAR_OF_CHANGE in (2022, 2023) and (DATE_OF_TERMINATION is null or DATE_OF_TERMINATION between '2024-04-01' and '2026-03-31') --Sets ONS mappings to the 25-26 mapping so this can be left until the population data is available
 left join $db_output.bbrb_stp_mapping stp on ons.DH_GEOGRAPHY_CODE = stp.CCG_CODE ---map ccg to stp/region level
 where year_of_count = (select max(year_of_count) from $reference_data.ons_population_v2 where GEOGRAPHIC_GROUP_CODE = 'E38') ---looks at latest data rather than depending on what month is being ran
 and GEOGRAPHIC_GROUP_CODE = 'E38' ---ccg-level population
 group by 
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end,
 stp.CCG_Code, stp.CCG_Name, stp.STP_Code, stp.STP_Name, stp.Region_Code, stp.Region_Name)
 AS A
 LEFT JOIN $db_output.commissioning_org_mapping AS B ON A.CCG_CODE = B.ORIGINAL_CCG_CODE and '$end_month_id' >= '$apr26_icb_swap_month_id' 

# COMMAND ----------

# DBTITLE 1,National Population - Uses Latest Mid-Year Estimates
 %sql
 INSERT OVERWRITE TABLE $db_output.eng_pop
 SELECT 
 case when (age_lower > 17 and age_lower < 65) then "18-64"
      when age_lower > 64 then "65+"
      when age_lower < 18 then "0-17" end as AGE_GROUP,
 SUM(POPULATION_COUNT) as POPULATION_COUNT
 from $reference_data.ons_population_v2 where year_of_count = (select max(year_of_count) from $reference_data.ons_population_v2 where GEOGRAPHIC_GROUP_CODE = 'E38') and GEOGRAPHIC_GROUP_CODE = 'E38' and trim(RECORD_TYPE) = 'E'
 group by case when (age_lower > 17 and age_lower < 65) then "18-64"
      when age_lower > 64 then "65+"
      when age_lower < 18 then "0-17" end

# COMMAND ----------

# DBTITLE 1,Age and Gender Standardisation Population - Ethnicity
 %sql
 INSERT OVERWRITE TABLE $db_output.age_gender_std_eth_pop
 SELECT
 DER_GENDER, 
 DER_GENDER_DESC,
 AGE,
 AGE_GROUP_IPS,
 AGE_GROUP_OAPS,
 AGE_GROUP_MHA,
 AGE_GROUP_CYP,
 AGE_GROUP_HIGHER_LEVEL,
 AGE_GROUP, 
 COALESCE(B.CCG_CODE, A.CCG_CODE) AS CCG_CODE,
 COALESCE(B.CCG_NAME, A.CCG_NAME) AS CCG_NAME,
 COALESCE(B.STP_CODE, A.STP_CODE) AS STP_CODE,
 COALESCE(B.STP_NAME, A.STP_NAME) AS STP_NAME,
 COALESCE(B.REGION_CODE, A.REGION_CODE) AS REGION_CODE,
 COALESCE(B.REGION_NAME, A.REGION_NAME) AS REGION_NAME,
 LOWERETHNICITYCODE,
 LOWERETHNICITYNAME,
 UPPERETHNICITY,
 WNW_ETHNICITY,
 A.POPULATION_COUNT * COALESCE(B.POPULATION_FACTOR, 1) AS POPULATION_COUNT
 FROM
 (select
 gen.Der_Gender,
 gen.Der_Gender_Desc,
 c.age_code as age,
 a.Age_Group_IPS, 
 a.Age_Group_OAPs,
 a.Age_Group_MHA,
 a.Age_Group_CYP,
 a.Age_Group_Higher_Level,
 case when (c.age_code > 17 and c.age_code < 65) then "18-64"
      when c.age_code > 64 then "65+"
      when c.age_code < 18 then "0-17" end as Age_Group,
 COALESCE(stp.CCG_Code, 'UNKNOWN') as CCG_Code,
 COALESCE(stp.CCG_Name, 'UNKNOWN') as CCG_Name,
 COALESCE(stp.STP_Code, 'UNKNOWN') as STP_Code,
 COALESCE(stp.STP_Name, 'UNKNOWN') as STP_Name,
 COALESCE(stp.Region_Code, 'UNKNOWN') as Region_Code,
 COALESCE(stp.Region_Name, 'UNKNOWN') as Region_Name,
 eth.LowerEthnicityCode,
 eth.LowerEthnicityName,
 eth.UpperEthnicity,
 eth.WNWEthnicity as WNW_Ethnicity,
 sum(observation) as POPULATION_COUNT
 from $reference_data.ons_2021_census c
 left join (SELECT *
 FROM $reference_data.ONS_CHD_GEO_EQUIVALENTS AS od
 WHERE DATE_OF_OPERATION = (SELECT MAX(DATE_OF_OPERATION) FROM $reference_data.ONS_CHD_GEO_EQUIVALENTS AS od2 WHERE od.GEOGRAPHY_CODE = od2.GEOGRAPHY_CODE AND od2.DATE_OF_OPERATION < '2026-03-31')
 ) od on c.area_type_code = od.GEOGRAPHY_CODE and area_type_group_code = "E38"
 inner join $db_output.bbrb_stp_mapping stp on od.DH_GEOGRAPHY_CODE = stp.CCG_CODE ---map ccg to stp/region level
 inner join $db_output.ethnicity_desc eth on c.ethnic_group_code = eth.Census21EthnicityCode
 inner join $db_output.gender_desc gen on c.sex_code = gen.Der_Gender and '$end_month_id' >= gen.FirstMonth and (gen.LastMonth is null or '$end_month_id' <= gen.LastMonth)
 inner join $db_output.age_band_desc a on c.age_code = a.AgeRepPeriodEnd and '$end_month_id' >= a.FirstMonth and (a.LastMonth is null or '$end_month_id' <= a.LastMonth)
 where area_type_group_code = "E38" ---Sub ICB grouping only
 and ethnic_group_code != -8 ---exclude does not apply ethnicity
 and ons_date = (select max(ons_date) from $reference_data.ons_2021_census where area_type_group_code = "E38")
 group by 
 gen.Der_Gender,
 gen.Der_Gender_Desc,
 c.age_code,
 a.Age_Group_IPS, 
 a.Age_Group_OAPs,
 a.Age_Group_MHA,
 a.Age_Group_CYP,
 a.Age_Group_Higher_Level,
 case when (c.age_code > 17 and c.age_code < 65) then "18-64"
      when c.age_code > 64 then "65+"
      when c.age_code < 18 then "0-17" end,
 stp.CCG_Code, stp.CCG_Name, stp.STP_Code, stp.STP_Name, stp.Region_Code, stp.Region_Name, eth.LowerEthnicityCode, eth.LowerEthnicityName, eth.UpperEthnicity, eth.WNWEthnicity)
 AS A 
 LEFT JOIN $db_output.commissioning_org_mapping AS B ON A.CCG_CODE = B.ORIGINAL_CCG_CODE and '$end_month_id' >= '$apr26_icb_swap_month_id' 

# COMMAND ----------

# DBTITLE 1,Age and Gender Standardisation Population - IMD
 %sql
 INSERT OVERWRITE TABLE $db_output.age_gender_std_imd_pop
 SELECT
 DER_GENDER, 
 DER_GENDER_DESC,
 AGE,
 AGE_GROUP_IPS,
 AGE_GROUP_OAPS,
 AGE_GROUP_MHA,
 AGE_GROUP_CYP,
 AGE_GROUP_HIGHER_LEVEL,
 AGE_GROUP, 
 COALESCE(B.CCG_CODE, A.CCG_CODE) AS CCG_CODE,
 COALESCE(B.CCG_NAME, A.CCG_NAME) AS CCG_NAME,
 COALESCE(B.STP_CODE, A.STP_CODE) AS STP_CODE,
 COALESCE(B.STP_NAME, A.STP_NAME) AS STP_NAME,
 COALESCE(B.REGION_CODE, A.REGION_CODE) AS REGION_CODE,
 COALESCE(B.REGION_NAME, A.REGION_NAME) AS REGION_NAME,
 IMD_DECILE,
 IMD_QUINTILE,
 IMD_CORE20,
 A.POPULATION_COUNT * COALESCE(B.POPULATION_FACTOR, 1) AS POPULATION_COUNT
 FROM
 (SELECT
 gen.Der_Gender,
 gen.Der_Gender_Desc,
 p.age_lower as age,
 a.Age_Group_IPS, 
 a.Age_Group_OAPs,
 a.Age_Group_MHA,
 a.Age_Group_CYP,
 a.Age_Group_Higher_Level,
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end as Age_Group,
 COALESCE(stp.CCG_Code, 'UNKNOWN') as CCG_Code,
 COALESCE(stp.CCG_Name, 'UNKNOWN') as CCG_Name,
 COALESCE(stp.STP_Code, 'UNKNOWN') as STP_Code,
 COALESCE(stp.STP_Name, 'UNKNOWN') as STP_Name,
 COALESCE(stp.Region_Code, 'UNKNOWN') as Region_Code,
 COALESCE(stp.Region_Name, 'UNKNOWN') as Region_Name,     
 p.IMD_Decile,
 p.IMD_Quintile,
 p.IMD_Core20,
 SUM(p.POPULATION_COUNT) as POPULATION_COUNT
 from lsoa_imd_pop p
 inner join ons_lsoa_to_ccg ccg on p.GEOGRAPHIC_SUBGROUP_CODE = ccg.LSOA11
 inner join $db_output.bbrb_stp_mapping stp on ccg.CCG = stp.CCG_CODE ---map ccg to stp/region level
 inner join $db_output.gender_desc gen
   on case when p.GENDER = "M" then 1
      when p.GENDER = "F" then 2
      end = gen.Der_Gender
    and '$end_month_id' >= gen.FirstMonth and (gen.LastMonth is null or '$end_month_id' <= gen.LastMonth)
 inner join $db_output.age_band_desc a on p.AGE_LOWER = a.AgeRepPeriodEnd and '$end_month_id' >= a.FirstMonth and (a.LastMonth is null or '$end_month_id' <= a.LastMonth)
 group by 
 gen.Der_Gender,
 gen.Der_Gender_Desc,
 p.age_lower,
 a.Age_Group_IPS, 
 a.Age_Group_OAPs,
 a.Age_Group_MHA,
 a.Age_Group_CYP,
 a.Age_Group_Higher_Level,
 case when (p.age_lower > 17 and p.age_lower < 65) then "18-64"
      when p.age_lower > 64 then "65+"
      when p.age_lower < 18 then "0-17" end,
 COALESCE(stp.CCG_Code, 'UNKNOWN'), COALESCE(stp.CCG_Name, 'UNKNOWN'), COALESCE(stp.STP_Code, 'UNKNOWN'), COALESCE(stp.STP_Name, 'UNKNOWN'), COALESCE(stp.Region_Code, 'UNKNOWN'), COALESCE(stp.Region_Name, 'UNKNOWN'), p.IMD_Decile, p.IMD_Quintile, p.IMD_Core20) AS A
 LEFT JOIN $db_output.commissioning_org_mapping AS B ON A.CCG_CODE = B.ORIGINAL_CCG_CODE and '$end_month_id' >= '$apr26_icb_swap_month_id' 