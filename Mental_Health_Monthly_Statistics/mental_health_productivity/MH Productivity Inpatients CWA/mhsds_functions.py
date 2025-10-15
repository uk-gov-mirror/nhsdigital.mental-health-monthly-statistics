# Databricks notebook source
from dataclasses import dataclass, field
import pyspark.sql.types as T
import pyspark.sql.functions as F
import json
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from pyspark.sql.column import Column
from functools import reduce
from pyspark.sql import DataFrame as df

# COMMAND ----------

# DBTITLE 1,Common Functions
def timenow():
  return datetime.now().strftime("%Y%m%d %X")
 
def str2dt(date: str) -> T.DateType():
  """  This function converts a string into a datetime in the 
  format datetime(YYYY, M, D, H, M)
  
  Example:
  str2dt("2021-09-01")
  >> datetime.datetime(2021, 9, 1, 0, 0)
  """
  date_format = '%Y-%m-%d'
  date_conv = datetime.strptime(date, date_format)
  
  return date_conv
 
def dt2str(date: T.DateType()) -> str:
  """
  This function converts a datetime to a string in the 
  format "YYYY-MM-DD"
  
  Example:
  dt2str(datetime(2022, 1, 1, 0, 0))
  >> "2022-01-01"
  """ 
  date_format = '%Y-%m-%d'
  date_conv = date.strftime(date_format)
  
  return date_conv
 
def first_day(date: T.DateType()) -> T.DateType():
  """  This function gets the first day of the month
  for any given date
  
  Example:
  get_first_day(datetime(2021, 1, 15, 0, 0))
  >> datetime(2021, 1, 1, 0, 0)
  """
  first_day = date.replace(day=1) ##first day
  
  return first_day
 
def last_day(date: T.DateType()) -> T.DateType():
  """  This function gets the last day of the month
  for any given date
  
  Example:
  get_last_day(datetime(2021, 1, 15, 0, 0))
  >> datetime(2021, 1, 31, 0, 0)
  """
  last_day_params = calendar.monthrange(date.year, date.month)[1]
  last_day = date.replace(day=last_day_params) ##last day
  
  return last_day
 
def add_months(date: T.DateType(), rp_length_num: int) -> T.DateType():
  """ This functions adds required amount of 
  months from a given date  
  
  Example:
  add_months(datetime(2021, 1, 15, 0, 0), 3)
  >> datetime(2020, 10, 15, 0, 0)
  """
  new_month = date + relativedelta(months=rp_length_num) ##minus rp_length_num months
  
  return new_month
 
def minus_months(date: T.DateType(), rp_length_num: int) -> T.DateType():
  """ This functions minuses required amount of 
  months from a given date  
  
  Example:
  minus_months(datetime(2021, 1, 15, 0, 0), 3)
  >> datetime(2020, 10, 15, 0, 0)
  """
  new_month = date - relativedelta(months=rp_length_num) ##minus rp_length_num months
  
  return new_month
 
def is_numeric(s):
    try:
        float(s)
        return 1
    except ValueError:
        return 0
    except TypeError:
        return 0
spark.udf.register("is_numeric", is_numeric)
 
def parent_breakdown(whole_breakdown: str) -> str:
  return whole_breakdown.split(";")[0]

def child_breakdown(whole_breakdown: str) -> str:
  return whole_breakdown.split(";")[-1]

def get_pyspark_column_name(col_expr: Column) -> str:
  s = col_expr._jc.toString()
  if s.startswith("`") and s.endswith("`"):
      return s[1:-1]
  
  return s

def get_unique_pyspark_column_list(col_list: list) -> list:
  seen_exprs = set()
  unique_columns = []
  for col in col_list:
      expr_str = str(col._jc.toString())  # low-level Spark column string
      if expr_str not in seen_exprs:
          seen_exprs.add(expr_str)
          unique_columns.append(col)
  
  return unique_columns

# COMMAND ----------

# DBTITLE 1,Parameter Functions
def get_rp_enddate(rp_startdate: str) -> str:
  """ This function gets the end of the month from
  the reporting period start date
  
  Example:
  get_rp_enddate("2021-10-01")
  >> "2021-10-31"
  """
  rp_startdate_dt = str2dt(rp_startdate)
  rp_enddate_dt = last_day(rp_startdate_dt)
  rp_enddate = dt2str(rp_enddate_dt)
  
  return rp_enddate  
 
def get_pub_month(rp_startdate: str, status: str) -> str:
  """ This function gets the Publication year and month
  in the format YYYYMM from the reporting period start date 
  and submission window
  
  Example:
  get_pub_month("2021-10-01", "Performance")
  >> "202201"
  """ 
  pub_month = str2dt(rp_startdate)
  
  if status == "Provisional":
    pub_month = add_months(pub_month, 2)
  elif status in ["Performance", "Final", "Adhoc"]:
    pub_month = add_months(pub_month, 3)
  else:
    return ValueError("Invalid submission window name inputted")
 
  pub_month = dt2str(pub_month)
  pub_month = pub_month[0:4] + pub_month[5:7]
  return pub_month
 
def get_qtr_startdate(rp_startdate: str) -> str:
  """  This functions gets the ReportingPeriodStartDate of a
  Quarterly Reporting Period
  
  Example:
  get_qtr_startdate("2020-03-01")
  >> "2020-01-01"
  """
  rp_startdate_dt = str2dt(rp_startdate) ##to datetime
  rp_qtr_startdate_dt = minus_months(rp_startdate_dt, 2) ##minus 2 months
  rp_qtr_startdate = dt2str(rp_qtr_startdate_dt) ##to string
  
  qtr_start_dt = str2dt(rp_qtr_startdate)
  start_date_dt = datetime(1900, 4, 1)
  time_diff = relativedelta(qtr_start_dt, start_date_dt)
  qtr_monthid_start = int(time_diff.years * 12 + time_diff.months + 1)
  
  return rp_qtr_startdate, qtr_monthid_start
 
def get_12m_startdate(rp_startdate: str) -> str:
  """  This functions gets the ReportingPeriodStartDate of a
  12-month Reporting Period
  
  Example:
  get_12m_startdate("2020-03-01")
  >> "2019-04-01"
  """
  rp_startdate_dt = str2dt(rp_startdate) ##to datetime
  rp_12m_startdate_dt = minus_months(rp_startdate_dt, 11) ##minus 11 months
  rp_12m_startdate = dt2str(rp_12m_startdate_dt) ##to string
  
  return rp_12m_startdate
 
def get_month_ids(rp_startdate: str) -> int:
  """  This function gets the end_month_id and start_month_id 
  parameters from the rp_startdate. This assumes a reporting 
  period of 12 months maximum
  
  Example:
  get_month_ids("2021-09-01")
  >> 1458, 1447
  """
  rp_startdate_dt = str2dt(rp_startdate)
  start_date_dt = datetime(1900, 4, 1)
  time_diff = relativedelta(rp_startdate_dt, start_date_dt)
  end_month_id = int(time_diff.years * 12 + time_diff.months + 1)
    
  return end_month_id
 
def get_financial_yr_start(rp_startdate: str) -> str:
    """ This function returns the date of the start
    of the financial year using the start of the
    reporting period
    
    Example:
    get_financial_yr_start("2022-05-01")
    >> "2022-04-01"
    """
    rp_startdate_dt = str2dt(rp_startdate)
    if rp_startdate_dt.month > 3:
      financial_year_start = datetime(rp_startdate_dt.year,4,1)
    else:
      financial_year_start = datetime(rp_startdate_dt.year-1,4,1)
     
    finan_start_dt1 = dt2str(financial_year_start)
    finan_start_dt = str2dt(finan_start_dt1)
    start_date_dt = datetime(1900, 4, 1)
    time_diff = relativedelta(finan_start_dt, start_date_dt)
    finan_monthid_start = int(time_diff.years * 12 + time_diff.months + 1)
          
    return dt2str(financial_year_start), finan_monthid_start
  
def get_year_of_count(rp_startdate):
  '''
  This function returns the year_of_count which should be used to extract data from reference_data.ONS_POPULATION_V2.  
  If the financial_yr_start is greater than the existing max(current_year) in reference_data.ONS_POPULATION_V2 then use
  current_year = max(current_year).
  '''
  current_year = get_financial_yr_start(rp_startdate)[0:4]
  max_year_of_count = spark.sql(f"select max(year_of_count) AS year_of_count from reference_data.ONS_POPULATION_V2 where GEOGRAPHIC_GROUP_CODE = 'E38'")
  max_year_of_count_value = max_year_of_count.first()["year_of_count"]
  year_of_count = current_year
  if (year_of_count > max_year_of_count_value):
    year_of_count = max_year_of_count_value
 
  return year_of_count  

# COMMAND ----------

# DBTITLE 1,Parameter Data Class
@dataclass
class MHRunParameters:
  db_output: str
  db_source: str
  rp_startdate: str
  rp_enddate: str = field(init=False) 
  month_id_end: int = field(init=False)
  month_id_start: int = field(init=False)  
  rp_start: str = field(init=False)
  rp_enddate: str = field(init=False)   
  
     
  def __post_init__(self):
    self.rp_enddate = get_rp_enddate(self.rp_startdate)
    self.month_id_end = get_month_ids(self.rp_startdate)
    self.rp_start, self.month_id_start = get_financial_yr_start(self.rp_startdate)
 
      
  def as_dict(self):
    json_dump = json.dumps(self, sort_keys=False, default=lambda o: o.__dict__)
    return json.loads(json_dump)
  
  def run_pub():
    return None

# COMMAND ----------

@dataclass
class MHRunParameters2:
  db_output: str
  db_source: str
  rp_startdate: str
  rp_enddate: str = field(init=False) 
  month_id_end: int = field(init=False)
  month_id_start: int = field(init=False)  
  rp_start: str = field(init=False)
  rp_enddate: str = field(init=False)   
  
     
  def __post_init__(self):
    self.rp_enddate = get_rp_enddate(self.rp_startdate)
    self.month_id_end = get_month_ids(self.rp_startdate)
    self.rp_start, self.month_id_start = get_qtr_startdate(self.rp_startdate)
   
      
  def as_dict(self):
    json_dump = json.dumps(self, sort_keys=False, default=lambda o: o.__dict__)
    return json.loads(json_dump)
  
  def run_pub():
    return None