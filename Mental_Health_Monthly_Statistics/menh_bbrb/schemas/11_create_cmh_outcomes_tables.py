# Databricks notebook source

 %sql
 DROP TABLE IF EXISTS $db_output.CMHProms_ReferralsPrep;
 CREATE TABLE IF NOT EXISTS $db_output.CMHProms_ReferralsPrep
 (
 Person_ID string,
 UniqServReqID string,
 RecordNumber bigint,
 Der_FY string,
 UniqMonthID bigint,
 ReportingPeriodStartDate date,
 ReportingPeriodEndDate date,
 OrgIDProv string,
 OpenStatus string,
 AgeServReferRecDate bigint,
 Gender string,
 ReferralRequestReceivedDate date,
 ServDischDate date,
 ReferRejectionDate date,
 ServTeamTypeRefToMH string,
 PrimReasonReferralMH string,
 UniqCareProfTeamID string,
 LADistrictAuth string,
 Ref_Dup bigint
 ) USING DELTA

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.CMHProms_Inpatients;
 CREATE TABLE IF NOT EXISTS $db_output.CMHProms_Inpatients
 (
 Person_ID string,
 UniqServReqID string,
 Der_HospSpellCount BIGINT
 )
 USING DELTA

# COMMAND ----------


 %sql
 DROP TABLE IF EXISTS $db_output.CMHProms_Referrals;
 CREATE TABLE IF NOT EXISTS $db_output.CMHProms_Referrals
 (
 Person_ID string,
 UniqServReqID string,
 RecordNumber bigint,
 Der_FY string,
 UniqMonthID bigint,
 ReportingPeriodStartDate date,
 ReportingPeriodEndDate date,
 OrgIDProv string,
 OpenStatus string,
 Provider_Name string,
 SubICB_Code string,
 SubICB_Name string,
 ICB_Code string,
 ICB_Name string,
 Region_Code string,
 Region_Name string,
 AgeServReferRecDate bigint,
 Gender string,
 ReferralRequestReceivedDate date,
 ServDischDate date,
 ReferRejectionDate date,
 PrimReasonReferralMH string,
 ServTeamTypeRefToMH string,
 Ref_Dup bigint
 ) USING DELTA

# COMMAND ----------


 %sql
 DROP TABLE IF EXISTS $db_output.CMHProms_Contacts;
 CREATE TABLE IF NOT EXISTS $db_output.CMHProms_Contacts
 (
 Person_ID string,
 UniqServReqID string,
 UniqMonthID bigint,
 ReportingPeriodEndDate date,
 RecordNumber bigint,
 Der_ContactDate date,
 Der_ContactOrder bigint,
 Der_DirectContact bigint,
 ContactCount bigint
 ) USING DELTA

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.CMHProms_AllAssessments;
 CREATE TABLE IF NOT EXISTS $db_output.CMHProms_AllAssessments
 (
 Person_ID string,
 UniqServReqID string,
 RecordNumber bigint,
 UniqMonthID bigint,
 ReportingPeriodEndDate date,
 OrgIDProv string,
 Der_AssUniqID string,
 Der_AssTable string,
 Der_AssToolCompDate date,
 CodedAssToolType string,
 Der_PreferredTermSNOMED string,
 Der_AssessmentToolName string,
 Der_AssessmentCategory string,
 PersScore string,
 Der_ValidScore string,
 Der_AssOrderAsc bigint
 ) USING DELTA

# COMMAND ----------


 %sql
 DROP TABLE IF EXISTS $db_output.CMHProms_PairedAssessments;
 CREATE TABLE IF NOT EXISTS $db_output.CMHProms_PairedAssessments
 (
 Person_ID string,
 UniqServReqID string,
 RecordNumber bigint,
 Der_FY string,
 UniqMonthID bigint,
 ReportingPeriodStartDate date,
 OrgIDProv string,
 Age int,
 Gender string,
 ReferralRequestReceivedDate date,
 ServDischDate date,
 Der_AssUniqID string,
 Der_PreferredTermSNOMED string,
 Der_AssessmentToolName string,
 Der_AssessmentToolCategory string,
 Der_AssToolCompDate date,
 Der_AssOrderAsc bigint,
 SecondContact date,
 ContactCount bigint
 ) USING DELTA

# COMMAND ----------


 %sql
 DROP TABLE IF EXISTS $db_output.CMHProms_Master;
 CREATE TABLE IF NOT EXISTS $db_output.CMHProms_Master
 (
 Person_ID string,
 UniqServReqID string,
 RecordNumber bigint,
 ServTeamTypeRefTo string,
 PrimReasonReferralMH string,
 Der_FY string,
 UniqMonthID bigint,
 ReportingPeriodStartDate date,
 ReportingPeriodEndDate date,
 OpenStatus string,
 OrgIDProv string,
 Provider_Name string,
 Region_Code string,
 Region_Name string,
 CCG_Code string, --SubICB_Code
 CCG_Name string, --SubICB_Name
 STP_Code string, --ICB_Code
 STP_Name string, --ICB_Name
 Age int,
 Gender string,
 ReferralRequestReceivedDate date,
 ServDischDate date,
 Der_AssessmentToolName string,
 Der_PreferredTermSNOMED string,
 SecondContact date,
 ContactCount bigint,
 Der_AssOrderAsc bigint,
 Ref_Dup bigint
 ) USING DELTA