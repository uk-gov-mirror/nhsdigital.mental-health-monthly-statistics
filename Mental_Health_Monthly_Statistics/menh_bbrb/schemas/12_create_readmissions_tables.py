# Databricks notebook source
 %sql
 DROP TABLE IF EXISTS $db_output.Readm_FirstWardStay;
 CREATE TABLE IF NOT EXISTS $db_output.Readm_FirstWardStay 
 (
 UniqHospProvSpellID         STRING,
 Person_ID                   STRING,
 UniqServReqID               STRING,
 UniqMonthID                 BIGINT,
 RecordNumber                BIGINT,
 ReportingPeriodStartDate    DATE,
 ReportingPeriodEndDate      DATE,
 OrgIDProv                   STRING,
 StartDateHospProvSpell      DATE,
 StartTimeHospProvSpell      DATE,
 DischDateHospProvSpell      DATE,
 MethOfDischMHHospProvSpell  STRING,
 DestOfDischHospProvSpell    STRING,
 AgeRepPeriodEnd             BIGINT,
 OrgIDCCGRes                 STRING,
 UniqWardStayID_first        STRING,
 StartDateWardStay_first     DATE,
 StartTimeWardStay_first     DATE,
 WS_UniqMonthID_first        BIGINT,
 HospitalBedTypeMH_first     STRING

 ) USING DELTA

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.Readm_LatestWardStay;
 CREATE TABLE IF NOT EXISTS $db_output.Readm_LatestWardStay 
 (
 UniqHospProvSpellID         STRING,
 UniqServReqID               STRING,
 Person_ID                   STRING,
 UniqMonthID                 BIGINT,
 UniqWardStayID              STRING,
 RecordNumber                BIGINT,
 StartDateWardStay           DATE,
 StartTimeWardStay           DATE,
 EndDateWardStay             DATE,
 EndTimeWardStay             DATE,
 MHAdmittedPatientClass      STRING,
 MHS502UniqID                STRING,
 WS_Order                    INT
 ) USING DELTA

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.Readm_AllSpells;
 CREATE TABLE IF NOT EXISTS $db_output.Readm_AllSpells 
 (
 Person_ID                       STRING,
 UniqMonthID                     BIGINT, 
 UniqHospProvSpellID             STRING,
 UniqServReqID                   STRING,
 RecordNumber                    BIGINT,
 OrgIDProv                       STRING,
 Provider_Name                   STRING,
 StartDateHospProvSpell          DATE,
 DischDateHospProvSpell          DATE,
 AgeRepPeriodEnd                 BIGINT,    
 CCG_Code                        STRING,
 CCG_Name                        STRING,
 Region_Code                     STRING,
 Region_Name                     STRING,
 STP_Code                        STRING,
 STP_Name                        STRING,
 MethOfDischMHHospProvSpell      STRING,
 DestOfDischHospProvSpell        STRING,
 Der_MethOfDischAccepted_Flag    INT,
 Der_DestOfDischNotHospital_Flag INT,
 UniqWardStayID_first            STRING,
 StartDateWardStay_first         DATE, 
 WS_UniqMonthID_first            BIGINT,
 HospitalBedTypeMH_first         STRING, 
 Acute_Bed_FirstCategory         STRING,
 UniqWardStayID_last             STRING, 
 StartDateWardStay_last          DATE,
 WS_UniqMonthID_last             BIGINT,
 HospitalBedTypeMH_last          STRING,
 Acute_Bed_LastCategory          STRING,
 Der_Admission                   INT,
 Der_Discharge                   INT
 ) USING DELTA

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.Readm_ReadmittedSpells;
 CREATE TABLE $db_output.Readm_ReadmittedSpells 
 (
 Person_ID               STRING,
 RecordNumber            BIGINT,
 Index_HS                STRING,
 Index_StartDate         DATE,
 Index_DischDate         DATE,
 UniqHospProvSpellID     STRING,
 StartDateHospProvSpell  DATE,
 TimetoReadm             BIGINT,
 FirstReAdm              INT,
 LastDisch               INT
 ) USING DELTA

# COMMAND ----------

 %sql
 DROP TABLE IF EXISTS $db_output.Readm_Master;
 CREATE TABLE IF NOT EXISTS $db_output.Readm_Master 
 (
 UniqHospProvSpellID             STRING,
 RecordNumber                    BIGINT,
 UniqServReqID                   STRING,
 Person_ID                       STRING,
 ReportingPeriodStartDate        DATE,
 ReportingPeriodEndDate          DATE,
 AgeRepPeriodEnd                 BIGINT,
 OrgIDProv                       STRING,
 Provider_Name                   STRING,
 CCG_Code                        STRING,
 CCG_Name                        STRING,
 Region_Code                     STRING,
 Region_Name                     STRING,
 STP_Code                        STRING,
 STP_Name                        STRING,
 HospitalBedTypeMH_last          STRING,
 Acute_Bed_LastCategory          STRING,
 Der_Discharge                   INT,
 Index_DischDate                 DATE,
 ReadmissionDate                 DATE,
 Der_MethOfDischAccepted_Flag    INT,
 Der_DestOfDischNotHospital_Flag INT,
 Der_DischEligibleForReAdm_Flag  INT,
 TimetoReadm                     BIGINT
 ) USING DELTA