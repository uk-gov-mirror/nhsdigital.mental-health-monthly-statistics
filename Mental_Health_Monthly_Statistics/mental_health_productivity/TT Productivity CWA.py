# Databricks notebook source
 %sql

 select distinct Unique_MonthID, ReportingPeriodStartDate
 from iapt_database.ids000header

# COMMAND ----------

 %py
 import pandas as pd
 import numpy as np
 from datetime import datetime
 import calendar
 from dateutil.relativedelta import relativedelta

# COMMAND ----------

 %py
 #initialise widgets
 dbutils.widgets.text("latestmonth_startdate", "2025-05-01") #start date of the latest month
 dbutils.widgets.text("monthid", "1502") #start date of the latest month
 dbutils.widgets.text("db_output", "personal_db") #output database


 #get widgets as python variables
 rp_startdate = dbutils.widgets.get("latestmonth_startdate")
 db_output  = dbutils.widgets.get("db_output")
 monthid  = dbutils.widgets.get("monthid")

# COMMAND ----------

 %sql --COMBINED VERSION 1.5 and 2 data

 -- Month by month counts of contacts by AppType (Assessment/Treatment) by Hight / Low Intensity 
 -- Report by organisation and exclude non-NHS orgs (Use org_type_daily to find Trusts)
 -- All months from Apr 2019 (v1.5 to Aug 2020, v2.0/v2.1 to Sept 2024)

 -- Months included are specified via Unique_MonthID in line 102 (v1.5 data) and line 58 (v2.0/v2.1 data)

 -- Output in format used by Productivity team in Finance to produce TT productivity estimates

 CREATE OR REPLACE TEMP VIEW TT_CC AS

 select OrgID_Provider, Organisation_Name, Month_year
 , StartOfMonth
 , AppType
 , Attended as AttendedCC
 , case when AppType in ('02','03','05') or AttTreatHIonly = 0 then cast(AttTreatHIonly as string) else '-' end as AttTreatmentHIonly
 , case when AppType in ('02','03','05') or AttTreatLIonly = 0 then cast(AttTreatLIonly as string) else '-' end as AttTreatmentLIonly
 , case when AppType in ('02','03','05') or AttTreatMixed = 0 then cast(AttTreatMixed as string) else '-' end as AttTreatmentMixed
 , case when AppType in ('02','03','05') or AttTreatOtherTType = 0 then cast(AttTreatOtherTType as string) else '-' end as AttTreatOtherTType

 from(
 --VERSION 2 data

 select cc.Unique_monthID, orgid_provider, od.Name as Organisation_Name
 , case when month(max(CareContDate)) < 10 then concat('0',right(month(max(CareContDate)),1),'/',right(year(max(CareContDate)),4))
  else concat(right(month(max(CareContDate)),2),'/',right(year(max(CareContDate)),4)) end as Month_year
 ,TRUNC( max(CareContDate) , 'MM' ) as StartOfMonth
 , AppType
 , count(distinct case when (AttendOrDNAcode in (5,6) or PlannedCareContIndicator = 'N') then UniqueID_IDS201 end) as Attended
 , count(distinct case when (AttendOrDNAcode in (5,6) or PlannedCareContIndicator = 'N') and AppType in ('02','03','05') then UniqueID_IDS201 end) as AttTreatAll
 , count(distinct case when (AttendOrDNAcode in (5,6) or PlannedCareContIndicator = 'N') and AppType in ('02','03','05') and ca.HIflag = 1
 and ca.LIflag = 0 then UniqueID_IDS201 end) as AttTreatHIonly
 , count(distinct case when (AttendOrDNAcode in (5,6) or PlannedCareContIndicator = 'N') and AppType in ('02','03','05') and ca.LIflag = 1
 and ca.HIflag = 0 then UniqueID_IDS201 end) as AttTreatLIonly
 , count(distinct case when (AttendOrDNAcode in (5,6) or PlannedCareContIndicator = 'N') and AppType in ('02','03','05') and ca.LIflag = 1
 and ca.HIflag = 1 then UniqueID_IDS201 end) as AttTreatMixed
 , count(distinct case when (AttendOrDNAcode in (5,6) or PlannedCareContIndicator = 'N') and AppType in ('02','03','05')
 and ((ca.ESflag = 1 and ca.LIflag = 0 and ca.HIflag = 0)
 or (ca.notHILIESflag = 1 and ca.ESflag = 0 and ca.LIflag = 0 and ca.HIflag = 0) or ca.PathwayID is null)
  then UniqueID_IDS201 end) as AttTreatOtherTType
 from iapt_database.ids201carecontact cc

 left join (
 select Unique_CareContactID, pathwayID
 ,max(case when CodeProcAndProcStatus in ('1127281000000100', '1129471000000105', '842901000000108', '286711000000107', '314034001', '449030000', '933221000000107', '1026131000000100', '304891004', '228557008', '443730003') then 1 else 0 end) as HIflag
 ,max(case when CodeProcAndProcStatus in ('748051000000105', '748101000000105', '748041000000107', '748091000000102', '748061000000108', '702545008', '1026111000000108', '975131000000104') then 1 else 0 end) as LIflag
 ,max(case when CodeProcAndProcStatus in ('1098051000000103') then 1 else 0 end) as ESflag
 ,max(case when CodeProcAndProcStatus not in ('1127281000000100', '1129471000000105', '842901000000108', '286711000000107', '314034001', '449030000', '933221000000107', '1026131000000100', '304891004', '228557008', '443730003','748051000000105', '748101000000105', '748041000000107', '748091000000102', '748061000000108', '702545008', '1026111000000108', '975131000000104','1098051000000103') or CodeProcAndProcStatus is null then 1 else 0 end) as notHILIESflag
 from  iapt_database.ids202careactivity ca
 group by Unique_CareContactID, pathwayID
 ) ca on cc.Unique_CareContactID = ca.Unique_CareContactID and cc.pathwayID = ca.pathwayID

 left join (
 select *
 ,row_number() over(partition by org_code order by case when org_is_current = 1 then 0 else 1 end asc, case when business_end_date is null then 0 else 1 end asc
                                                   ,business_end_date desc, business_start_date desc) as rank
 from reference_data.org_daily 
 )od on od.org_code = cc.OrgID_Provider and rank = 1
 left join reference_data.org_type_daily ot on ot.org_type_code = od.org_type_code

 where cc.Unique_monthID between 1446 and '$monthid'
 --and ot.description like '%TRUST%'
 --and oph.ODS_Organisation_Type like '%TRUST%'
 group by cc.Unique_monthID, orgid_provider, od.Name, AppType

 UNION ALL --Version 1.5 data

 select cc.Unique_monthID, ORGCODEPROVIDER as orgid_provider, od.Name as Organisation_Name
 , case when month(max(APPOINTMENT)) < 10 then concat('0',right(month(max(APPOINTMENT)),1),'/',right(year(max(APPOINTMENT)),4))
  else concat(right(month(max(APPOINTMENT)),2),'/',right(year(max(APPOINTMENT)),4)) end as Month_year
 ,TRUNC( max(APPOINTMENT) , 'MM' ) as StartOfMonth
 , AppType
 , count(distinct case when ATTENDANCE in (5,6) then cc.APPOINTMENT_ID end) as Attended
 , count(distinct case when ATTENDANCE in (5,6) and AppType in ('02','03','05') then cc.APPOINTMENT_ID end) as AttTreatAll
 , count(distinct case when ATTENDANCE in (5,6) and AppType in ('02','03','05') and ca.HIflag = 1 and ca.LIflag = 0 then cc.APPOINTMENT_ID end) as AttTreatHIonly
 , count(distinct case when ATTENDANCE in (5,6) and AppType in ('02','03','05') and ca.LIflag = 1 and ca.HIflag = 0 then cc.APPOINTMENT_ID end) as AttTreatLIonly
 , count(distinct case when ATTENDANCE in (5,6) and AppType in ('02','03','05') and ca.LIflag = 1 and ca.HIflag = 1 then cc.APPOINTMENT_ID end) as AttTreatMixed
 , count(distinct case when ATTENDANCE in (5,6) and AppType in ('02','03','05') and ((ca.ESflag = 1 and ca.LIflag = 0 and ca.HIflag = 0) 
           or (ca.notHILIESflag = 1 and ca.ESflag = 0 and ca.LIflag = 0 and ca.HIflag = 0) or ca.PathwayID is null) then cc.APPOINTMENT_ID end) as AttTreatOtherTType
 from iapt_database.rep_appointment cc

 left join (
 select APPOINTMENT_ID, PathwayID
 ,case when THERTYPE1 in ('40','41','42','43','44','45','46','47','48','50','51') or THERTYPE2 in ('40','41','42','43','44','45','46','47','48','50','51') 
    or THERTYPE3 in ('40','41','42','43','44','45','46','47','48','50','51') or THERTYPE4 in ('40','41','42','43','44','45','46','47','48','50','51') 
    then 1 else 0 end as HIflag
 ,case when THERTYPE1 in ('20','21','22','23','24','25','26','27','28') or THERTYPE2 in ('20','21','22','23','24','25','26','27','28') 
    or THERTYPE3 in ('20','21','22','23','24','25','26','27','28') or THERTYPE4 in ('20','21','22','23','24','25','26','27','28') then 1 else 0 end as LIflag
 ,case when THERTYPE1 in ('29','49') or THERTYPE2 in ('29','49') or THERTYPE3 in ('29','49') or THERTYPE4 in ('29','49') then 1 else 0 end as ESflag
 ,case when (THERTYPE1 not in ('20','21','22','23','24','25','26','27','28','29','40','41','42','43','44','45','46','47','48','49','50','51') or THERTYPE1 is null) 
   and (THERTYPE2 not in ('20','21','22','23','24','25','26','27','28','29','40','41','42','43','44','45','46','47','48','49','50','51') or THERTYPE2 is null)
   and (THERTYPE3 not in ('20','21','22','23','24','25','26','27','28','29','40','41','42','43','44','45','46','47','48','49','50','51') or THERTYPE3 is null)
   and (THERTYPE4 not in ('20','21','22','23','24','25','26','27','28','29','40','41','42','43','44','45','46','47','48','49','50','51') or THERTYPE4 is null) 
   then 1 else 0 end as notHILIESflag
 from iapt_database.rep_appointment appt
 ) ca on cc.APPOINTMENT_ID = ca.APPOINTMENT_ID and cc.pathwayID = ca.pathwayID

 left join (
 select *
 ,row_number() over(partition by org_code order by case when org_is_current = 1 then 0 else 1 end asc, case when business_end_date is null then 0 else 1 end asc
                                                   ,business_end_date desc, business_start_date desc) as rank
 from reference_data.org_daily 
 )od on od.org_code = cc.ORGCODEPROVIDER and rank = 1
 left join reference_data.org_type_daily ot on ot.org_type_code = od.org_type_code

 where cc.Unique_monthID between 1429 and 1445
 --and ot.description like '%TRUST%'
 --and oph.ODS_Organisation_Type like '%TRUST%'
 group by cc.Unique_monthID, orgid_provider, od.Name, AppType

 )_

 order by Unique_monthID
 , case when Organisation_Name = 'All Non-NHS providers' then 1
  when Organisation_Name = 'All NHS providers' then 2
  else 3 end, orgid_provider, AppType


# COMMAND ----------

 %sql

 select distinct month_year, startofMonth from TT_CC

# COMMAND ----------

 %py

 columns = ['AppType', 'Cost', 'Cost_LI', 'Cost_HI']
 data = [
 ('01',185.54739033,0.0,0.0),
 ('02',165.87930294,71.8360894502663,215.508268350799),
 ('03',158.39644554,92.2756681333834,276.82700440015),
 ('04' ,108.29967014,0.0,0.0),
 ('05' ,134.79784972,66.0440263207639,198.132078962292),
 ('06' ,130.24576504,0.0,0.0),
 ('10' ,129.36922463,0.0,0.0),
 ('98' ,160.65999706,0.0,0.0),
 ]

 df = spark.createDataFrame(data).toDF(*columns)

 df.createOrReplaceTempView("App_Cost")

# COMMAND ----------

 %sql

 select * from App_Cost

# COMMAND ----------

# DBTITLE 1,CWA calculation
 %sql

 CREATE OR REPLACE TEMP VIEW TT_CWA_AppType AS

 Select a.*,
 case when (UnitCost_LI + UnitCost_HI) = 0 then (AttendedCC * UnitCost)
 else (((AttTreatmentMixed + AttTreatOtherTType) * UnitCost) + (AttTreatmentHIonly * UnitCost_HI) + (AttTreatmentLIonly * UnitCost_LI ))
 end as CWA
 from
 (
 select a.*,
 Case when b.Cost is null then 162.72017621309
 else b.Cost end as UnitCost,
 Case when b.Cost is null then 0
 else b.Cost_LI end as UnitCost_LI,
 Case when b.Cost is null then 0
 else b.Cost_HI end as UnitCost_HI
 from TT_CC a
 left join App_Cost b on a.AppType = b.AppType
 ) a

# COMMAND ----------

# DBTITLE 1,Adding Provider Type
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



# COMMAND ----------

# DBTITLE 1,CWA output 
 %sql
 CREATE OR REPLACE TEMP VIEW TT_CWA_All AS
 select a.*,
 CASE WHEN b.OrgCode is null and Organisation_Name like '%TRUST' then 'Other Trusts'
      WHEN b.OrgCode is null and Organisation_Name not like '%TRUST' then 'Non-NHS providers'
      else b.Prov_Type end as Prov_Type
 from TT_CWA_AppType a
 left join prov_type b on a.OrgID_Provider = b.OrgCode;

 select * from TT_CWA_All

# COMMAND ----------

# DBTITLE 1,CWA data for YTD current
 %sql

 select 'Current_YTD', Prov_Type, OrgID_Provider, Organisation_Name, sum(CWA) as CWA

 from TT_CWA_All a
 left join reference_data.calendar_financial_year f on f.start_date <= '$latestmonth_startdate' and f.end_date >= '$latestmonth_startdate'
 where StartOfMonth >= f.start_date
 and StartOfMonth <= '$latestmonth_startdate'

 group by Prov_Type, OrgID_Provider, Organisation_Name

# COMMAND ----------

# DBTITLE 1,CWA data for current rolling quarter (run this only if current month is on or after June, i.e. for months between June - March)
 %sql

 select 'Current_Rolling_Quarter',Prov_Type, OrgID_Provider, Organisation_Name, sum(CWA) as CWA

 from TT_CWA_All
 where StartOfMonth  >= DATEADD(MONTH, -2, '$latestmonth_startdate')
 and StartOfMonth <= '$latestmonth_startdate'
 group by Prov_Type, OrgID_Provider, Organisation_Name

# COMMAND ----------

 %md
 ## Previous year's data

# COMMAND ----------

# DBTITLE 1,CWA data for YTD previous
 %sql

 select 'Previous_YTD', Prov_Type, OrgID_Provider, Organisation_Name, sum(CWA) as CWA

 from TT_CWA_All a
 left join reference_data.calendar_financial_year f on f.start_date <= DATEADD(MONTH, -12, '$latestmonth_startdate') and f.end_date >= DATEADD(MONTH, -12, '$latestmonth_startdate')
 where StartOfMonth >= f.start_date
 and StartOfMonth <= DATEADD(MONTH, -12, '$latestmonth_startdate')

 group by Prov_Type, OrgID_Provider, Organisation_Name

# COMMAND ----------

# DBTITLE 1,CWA data for previous rolling quarter (run this only if current month is on or after June, i.e. for months between June - March)
 %sql

 select 'Previous_Rolling_Qtr', Prov_Type, OrgID_Provider, Organisation_Name, sum(CWA) as CWA

 from TT_CWA_All
 where StartOfMonth  >= DATEADD(MONTH, -14, '$latestmonth_startdate')
 and StartOfMonth <= DATEADD(MONTH, -12, '$latestmonth_startdate')

 group by Prov_Type, OrgID_Provider, Organisation_Name