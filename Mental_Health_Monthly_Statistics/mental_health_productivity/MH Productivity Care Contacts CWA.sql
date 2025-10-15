-- Databricks notebook source
 %py
 import pandas as pd
 import numpy as np
 from datetime import datetime
 import calendar
 from dateutil.relativedelta import relativedelta

-- COMMAND ----------

 %py
 #initialise widgets
 dbutils.widgets.text("latestmonth_startdate", "2025-05-01") #start date of the latest month
 dbutils.widgets.text("db_output", "personal_db") #output database


 #get widgets as python variables
 rp_startdate = dbutils.widgets.get("latestmonth_startdate")
 db_output  = dbutils.widgets.get("db_output")

-- COMMAND ----------

 %py
 date_format = '%Y-%m-%d'
 rp_currentyear = datetime.strptime(rp_startdate, date_format)
 rp_lastyear = rp_currentyear - relativedelta(years=1)

 lastyear_rp = rp_lastyear.strftime(date_format)
 currentyear_rp = rp_currentyear.strftime(date_format)

 print (currentyear_rp, lastyear_rp) 
 rp_year = rp_currentyear.year
 rp_month = rp_currentyear.month
 print(rp_year, rp_month)


-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW ServiceTeamType AS
----MHS102 All
SELECT
s.UniqMonthID,
s.OrgIDProv,
s.Person_ID,
s.UniqServReqID,
COALESCE(s.UniqCareProfTeamID, s.UniqOtherCareProfTeamLocalID) as UniqCareProfTeamID,
s.ServTeamTypeRefToMH,
s.ServTeamIntAgeGroup,
s.ReferClosureDate,
s.ReferClosureTime,
s.ReferClosReason,
s.ReferRejectionDate,
s.ReferRejectionTime,
s.ReferRejectReason,
s.RecordNumber,
s.RecordStartDate,
s.RecordEndDate
from mhsds_database.mhs102otherservicetype s
UNION ALL
----MHS101 v6
SELECT
r.UniqMonthID,
r.OrgIDProv,
r.Person_ID,
r.UniqServReqID,
r.UniqCareProfTeamLocalID as UniqCareProfTeamID, 
 r.ServTeamType as ServTeamTypeRefToMH,
r.ServTeamIntAgeGroup,
r.ServDischDate as ReferClosureDate,
r.ServDischTime as ReferClosureTime,
r.ReferClosReason,
r.ReferRejectionDate,
r.ReferRejectionTime,
r.ReferRejectReason,
r.RecordNumber,
r.RecordStartDate,
r.RecordEndDate
from mhsds_database.mhs101referral r
where UniqMonthID > 1488


-- COMMAND ----------

-- DBTITLE 1,Create a table with cost
 %py

 columns = ['TeamType', 'Cost']
 data = [
 ('A01' ,251.62506972),
 ('A02' ,338.34250847),
 ('A05' ,262.84917212),
 ('A06' ,279.94415525),
 ('A07' ,267.60271239),
 ('A08' ,312.54377912),
 ('A09' ,291.20148363),
 ('A10' ,289.37598783),
 ('A11' ,356.15362751),
 ('A12' ,344.62430292),
 ('A13' ,311.86254908),
 ('A14' ,300.1429598),
 ('A15' ,222.26026312),
 ('A16' ,291.99167627),
 ('A17' ,237.57722884),
 ('A18' ,302.61301023),
 ('A19' ,152.83411186),
 ('A20' ,1266.19115751),
 ('A21' ,375.72422246),
 ('A22' ,813.23108783),
 ('A23' ,574.58304116),
 ('A24' ,240.87411481),
 ('A25' ,669.06628531),
 ('B01' ,500.33420703),
 ('B02' ,438.50578816),
 ('C01' ,459.29763981),
 ('C02' ,312.81598071),
 ('C04' ,369.29353733),
 ('C05' ,386.70818211),
 ('C06' ,401.97711088),
 ('C07' ,641.6263303),
 ('C08' ,309.32668871),
 ('C10' ,319.53809374),
 ('D01' ,187.1472596),
 ('D02' ,379.24351136),
 ('D03' ,240.71772895),
 ('D04' ,917.04191615),
 ('D05' ,216.92550739),
 ('D06' ,322.66659194),
 ('D07' ,433.30289383),
 ('D08' ,389.54572606),
 ('E01' ,370.90843941),
 ('E02' ,366.83717264),
 ('E03' ,554.31813597),
 ('E04' ,280.22251091),
 ('F01' ,329.89695887),
 ('F02' ,335.60286777),
 ('F03' ,916.64859311),
 ('F04' ,526.82634172),
 ('F05' ,211.21486209),
 ('F06' ,158.10891513),
 ('F07' ,0.13548885),
 ('Z01' ,275.46985874),
 ('Z02' ,334.4485302)
 ]

 df = spark.createDataFrame(data).toDF(*columns)

 df.createOrReplaceTempView("TeamType_Cost")

-- COMMAND ----------

 %py

 columns = ['OrgCode', 'Prov_Type']
 prov = [
 ('R1L','Core Trust'),
 ('RAT','Core Trust'),
 ('RDY','Core Trust'),
 ('RGD','Core Trust'),
 ('RHA','Core Trust'),
 ('RJ8','Core Trust'),
 ('RKL','Core Trust'),
 ('RLY','Core Trust'),
 ('RMY','Core Trust'),
 ('RNU','Core Trust'),
 ('RP7','Core Trust'),
 ('RPG','Core Trust'),
 ('RQY','Core Trust'),
 ('RRE','Core Trust'),
 ('RRP','Core Trust'),
 ('RT1','Core Trust'),
 ('RT2','Core Trust'),
 ('RT5','Core Trust'),
 ('RV3','Core Trust'),
 ('RV5','Core Trust'),
 ('RV9','Core Trust'),
 ('RVN','Core Trust'),
 ('RW1','Core Trust'),
 ('RW4','Core Trust'),
 ('RW5','Core Trust'),
 ('RWK','Core Trust'),
 ('RWR','Core Trust'),
 ('RWV','Core Trust'),
 ('RWX','Core Trust'),
 ('RX2','Core Trust'),
 ('RX3','Core Trust'),
 ('RX4','Core Trust'),
 ('RXA','Core Trust'),
 ('RXE','Core Trust'),
 ('RXG','Core Trust'),
 ('RXM','Core Trust'),
 ('RXT','Core Trust'),
 ('RXV','Core Trust'),
 ('RXX','Core Trust'),
 ('RXY','Core Trust'),
 ('RYG','Core Trust'),
 ('TAD','Core Trust'),
 ('TAF','Core Trust'),
 ('TAH','Core Trust'),
 ('TAJ','Core Trust'),
 ('G6V2S','Core Trust')
 ]

 prov_df = spark.createDataFrame(prov).toDF(*columns)

 prov_df.createOrReplaceTempView("prov_type")

-- COMMAND ----------

-- DBTITLE 1,Merged dataset with unit cost
CREATE OR REPLACE TEMP VIEW MHCARECONTACTS AS

SELECT 
c.ORGIDPROV, 
ServTeamTypeRefToMH,
case when CARECONTDATE is null then null
else month(CARECONTDATE) end as Month_id,
case 
when month(CARECONTDATE) = 1 then 'Jan'
when month(CARECONTDATE) = 2 then 'Feb'
when month(CARECONTDATE) = 3 then 'Mar'
when month(CARECONTDATE) = 4 then 'Apr'
when month(CARECONTDATE) = 5 then 'May'
when month(CARECONTDATE) = 6 then 'Jun'
when month(CARECONTDATE) = 7 then 'Jul'
when month(CARECONTDATE) = 8 then 'Aug'
when month(CARECONTDATE) = 9 then 'Sep'
when month(CARECONTDATE) = 10 then 'Oct'
when month(CARECONTDATE) = 11 then 'Nov'
when month(CARECONTDATE) = 12 then 'Dec'
else null
end as Month,
f.label as year,  
case when CARECONTDATE is null then null
else TRUNC(CARECONTDATE, 'MM') end as CC_Month,
--f.start_date,
--f.end_date,
tc.Cost,
COUNT(DISTINCT UNIQCARECONTID) as Care_contacts
FROM 
mhsds_database.mhs201carecontact c 
left join ServiceTeamType s on c.uniqservreqid = s.uniqservreqid and c.recordnumber = s.recordnumber
left join mhsds_database.mhs501hospprovspell h on c.uniqservreqid = h.uniqservreqid and c.recordnumber = h.recordnumber
left join reference_data.calendar_financial_year f on c.carecontdate between f.start_date and f.end_date
left join TeamType_Cost tc on s.ServTeamTypeRefToMH = tc.TeamType
where
attendstatus in ('5','6')
and c.carecontdate >= '2019-04-01'
and h.uniqservreqid is null
group by 
c.ORGIDPROV, 
ServTeamTypeRefToMH,
case when CARECONTDATE is null then null
else month(CARECONTDATE) end,
case 
when month(CARECONTDATE) = 1 then 'Jan'
when month(CARECONTDATE) = 2 then 'Feb'
when month(CARECONTDATE) = 3 then 'Mar'
when month(CARECONTDATE) = 4 then 'Apr'
when month(CARECONTDATE) = 5 then 'May'
when month(CARECONTDATE) = 6 then 'Jun'
when month(CARECONTDATE) = 7 then 'Jul'
when month(CARECONTDATE) = 8 then 'Aug'
when month(CARECONTDATE) = 9 then 'Sep'
when month(CARECONTDATE) = 10 then 'Oct'
when month(CARECONTDATE) = 11 then 'Nov'
when month(CARECONTDATE) = 12 then 'Dec'
else null
end,
f.label,
case when CARECONTDATE is null then null
else TRUNC(CARECONTDATE, 'MM') end,
--f.start_date,
--f.end_date,
tc.Cost

-- COMMAND ----------

select * from MHCARECONTACTS

-- COMMAND ----------

 %sql

 CREATE OR REPLACE TEMP VIEW ORG_DAILY AS

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

-- COMMAND ----------

-- DBTITLE 1,Extract Current YTD data with TeamType breakdown
 %sql
 DROP TABLE IF EXISTS $db_output.MHCARECONTACTS_costs_YTD_cur;

 CREATE TABLE $db_output.MHCARECONTACTS_costs_YTD_cur as
 Select b.*, (Care_contacts * Unit_Cost_updated) as Total_Cost
 from
 (select a.*,
 Case when a.Cost is null then 302.0741875
     else a.Cost end as Unit_Cost_updated

 from MHCARECONTACTS a
 left join reference_data.calendar_financial_year f on f.start_date <= '$latestmonth_startdate' and f.end_date >= '$latestmonth_startdate'
 where CC_Month >= f.start_date
 and CC_Month <= '$latestmonth_startdate') b;

 Select 
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end as Prov_Type,
      a.ORGIDPROV,
      c.NAME,
      a.ServTeamTypeRefToMH,
      a.Month,
      a.year,
      a.Care_contacts,
      a.Unit_Cost_updated as Unit_Cost,
      a.Total_Cost
      
 from $db_output.MHCARECONTACTS_costs_YTD_cur a
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE


-- COMMAND ----------

-- DBTITLE 1,Extract previous years YTD data with TeamType breakdown
 %sql
 DROP TABLE IF EXISTS $db_output.MHCARECONTACTS_costs_YTD_prev;

 CREATE TABLE $db_output.MHCARECONTACTS_costs_YTD_prev as

 Select b.*, (Care_contacts * Unit_Cost_updated) as Total_Cost
 from
 (select a.*,
 Case when a.Cost is null then 302.0741875
     else a.Cost end as Unit_Cost_updated
 from MHCARECONTACTS a
 left join reference_data.calendar_financial_year f on f.start_date <= DATEADD(MONTH, -12, '$latestmonth_startdate') and f.end_date >= DATEADD(MONTH, -12, '$latestmonth_startdate')
 where CC_Month >= f.start_date
 and CC_Month <= DATEADD(MONTH, -12, '$latestmonth_startdate')) b;

 Select 
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end as Prov_Type,
      a.ORGIDPROV,
      c.NAME,
      a.ServTeamTypeRefToMH,
      a.Month,
      a.year,
      a.Care_contacts,
      a.Unit_Cost_updated as Unit_Cost,
      a.Total_Cost

 from $db_output.MHCARECONTACTS_costs_YTD_prev a
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE


-- COMMAND ----------

 %md
 ## CWA Output files

-- COMMAND ----------

-- DBTITLE 1,YTD Current year CWA output
 %sql

 Select year,  
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end as Prov_Type,
      ORGIDPROV,
      c.NAME,
      sum(Total_Cost)

 from $db_output.MHCARECONTACTS_costs_YTD_cur a
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE

 group by  year,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end,
      ORGIDPROV,
      c.NAME

-- COMMAND ----------

-- DBTITLE 1,YTD Previous year CWA output
 %sql

 Select year,  
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end as Prov_Type,
      ORGIDPROV,
      c.NAME,
      sum(Total_Cost)

 from $db_output.MHCARECONTACTS_costs_YTD_prev a
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE

 group by  year,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end,
      ORGIDPROV,
      c.NAME

-- COMMAND ----------

-- DBTITLE 1,Rolling Quarter - Current Year
 %sql

 Select 'Rolling_qtr_current_year',year,  
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end as Prov_Type,
      ORGIDPROV,
      c.NAME,
      sum(Total_Cost)

 from $db_output.MHCARECONTACTS_costs_YTD_cur a
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE

 where CC_Month  >= DATEADD(MONTH, -2, '$latestmonth_startdate')
 and CC_Month <= '$latestmonth_startdate'


 group by  year,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end,
      ORGIDPROV,
      c.NAME

-- COMMAND ----------

-- DBTITLE 1,Rolling Quarter - Previous Year
 %sql

 Select 'Rolling_qtr_prev_year',year,  
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end as Prov_Type,
      ORGIDPROV,
      c.NAME,
      sum(Total_Cost)

 from $db_output.MHCARECONTACTS_costs_YTD_prev a
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE

 where CC_Month  >= DATEADD(MONTH, -14, '$latestmonth_startdate')
 and CC_Month <= DATEADD(MONTH, -12, '$latestmonth_startdate')


 group by  year,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end,
      ORGIDPROV,
      c.NAME

-- COMMAND ----------

 %md
 TESTING AREA FOR NEW TEMPLATE


-- COMMAND ----------

 %sql
 Select '$latestmonth_startdate' AS YTD_end,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end AS Provider_Type,
 ORGIDPROV AS Provider_Code,
 Name AS Provider_NAme,
 ServTeamTypeRefToMH,
 sum(Care_Contacts) AS Care_Contacts,
 Unit_Cost_Updated  AS Unit_Cost,
 sum(Care_contacts) * Unit_Cost_updated AS CWA
 from
 (
 select a.*,b.OrgCode,b.Prov_Type,c.Name,
 Case when a.Cost is null then 302.0741875
     else a.Cost end as Unit_Cost_updated
 from MHCARECONTACTS a
 --left join reference_data.calendar_financial_year f on f.start_date <= '$latestmonth_startdate' and f.end_date >= '$latestmonth_startdate'
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE
 where 
 CC_Month >= add_months(trunc(add_months('$latestmonth_startdate',-3),'year'),3)
 and CC_Month <= '$latestmonth_startdate'
 ) b 

 GROUP BY 

 '$latestmonth_startdate' ,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end ,
 ORGIDPROV ,
 Name ,
 ServTeamTypeRefToMH,
 Unit_Cost_Updated  


 UNION ALL

 SELECT
 add_months('$latestmonth_startdate',-12) AS YTD_end,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end AS Provider_Type,
 ORGIDPROV ,
 Name ,
 ServTeamTypeRefToMH,
 sum(Care_Contacts) ,
 Unit_Cost_Updated  ,
 (sum(Care_contacts) * Unit_Cost_updated) 
 from
 (

 select a.*,b.OrgCode,b.Prov_Type,c.Name,
 Case when a.Cost is null then 302.0741875
     else a.Cost end as Unit_Cost_updated

 from MHCARECONTACTS a
 --left join reference_data.calendar_financial_year f on f.start_date <= '$latestmonth_startdate' and f.end_date >= '$latestmonth_startdate'
 left join prov_type b on a.ORGIDPROV = b.OrgCode
 left join ORG_DAILY c on a.ORGIDPROV = c.ORG_CODE
 where 
 CC_Month >= add_months(add_months(trunc(add_months('$latestmonth_startdate',-3),'year'),3),-12)
 and CC_Month <= add_months('$latestmonth_startdate',-12)


 ) b 

 GROUP BY 
 add_months('$latestmonth_startdate',-12) ,
 CASE WHEN b.OrgCode is null and NAME like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and NAME not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end ,
 ORGIDPROV ,
 Name ,
 ServTeamTypeRefToMH,
 Unit_Cost_Updated  


-- COMMAND ----------

 %sql
 /** TEST FOR DATES TO BE DELETED **/
 SELECT '$latestmonth_startdate',add_months(trunc(add_months('$latestmonth_startdate',-3),'year'),3),add_months(add_months(trunc(add_months('$latestmonth_startdate',-3),'year'),3),-12),add_months('$latestmonth_startdate',-12)