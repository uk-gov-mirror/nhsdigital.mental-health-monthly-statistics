# Databricks notebook source
#dbutils.widgets.removeAll()

# COMMAND ----------

import pandas as pd
import numpy as np
from datetime import datetime

# COMMAND ----------

#initialise widgets
dbutils.widgets.text("db_output", "personal_db") #output database
dbutils.widgets.text("db_source", "mhsds_database") #mhsds database
dbutils.widgets.text("latestmonth_startdate", "2025-05-01") #start date of the latest month


#get widgets as python variables
db_output  = dbutils.widgets.get("db_output")
db_source = dbutils.widgets.get("db_source")
rp_startdate = dbutils.widgets.get("latestmonth_startdate")

# COMMAND ----------

# DBTITLE 1,Import MHSDS Functions
 %run ./mhsds_functions

# COMMAND ----------

# DBTITLE 1,Set up parameters for YTD run
mh_run_params = MHRunParameters(db_output, db_source, rp_startdate)
params = mh_run_params.as_dict()
params

# COMMAND ----------

Return_Value = dbutils.notebook.run("./AllOutputsV6_CWA", 0, params)
print(Return_Value)

# COMMAND ----------

# DBTITLE 1,CWA YTD output1
 %sql
 CREATE OR REPLACE TABLE $db_output.CWA_YTD_Output USING DELTA AS

 select * from $db_output.cwa_output;

 select * from $db_output.CWA_YTD_Output

# COMMAND ----------

# DBTITLE 1,CWA Final Formatted output for YTD
 %sql

 CREATE OR REPLACE TABLE $db_output.MH_Inpatient_CWA_YTD USING DELTA AS

 select 'YTD' as Output_Type, a.* from $db_output.MH_Inpatient_CWA a;

 select * from $db_output.MH_Inpatient_CWA_YTD
 order by ProviderType, ProviderCode

# COMMAND ----------

 %md
 ## Rolling Quarterly data 

# COMMAND ----------

# DBTITLE 1,Set up parameters for rolling quarter data run
mh_run_params = MHRunParameters2(db_output, db_source, rp_startdate)
params2 = mh_run_params.as_dict()
params2

# COMMAND ----------

rp_date = datetime.strptime(rp_startdate, "%Y-%m-%d")
if rp_date.month >= 6 or rp_date.month <= 3:
  dbutils.notebook.run("./AllOutputsV6_CWA", 0, params2)
  


# COMMAND ----------

# DBTITLE 1,CWA rolling quarterly output1
 %sql
 CREATE OR REPLACE TABLE $db_output.CWA_Quarter_Output USING DELTA AS

 select * from $db_output.cwa_output;

 select * from $db_output.CWA_Quarter_Output

# COMMAND ----------

# DBTITLE 1,CWA Final Formatted output for rolling quarter
 %sql

 CREATE OR REPLACE TABLE $db_output.MH_Inpatient_CWA_Quarter USING DELTA AS

 select 'Rolling_qtr' as Output_Type, a.* from $db_output.MH_Inpatient_CWA a;

 select * from $db_output.MH_Inpatient_CWA_Quarter
 order by ProviderType, ProviderCode

# COMMAND ----------

 %sql
 select *
 FROM $db_output.MH_Inpatient_CWA
 ORDER BY 1