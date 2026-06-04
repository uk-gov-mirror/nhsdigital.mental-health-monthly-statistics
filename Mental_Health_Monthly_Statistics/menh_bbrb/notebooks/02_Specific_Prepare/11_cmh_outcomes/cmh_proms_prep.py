# Databricks notebook source
 %run ../../mhsds_functions

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.CMHProms_ReferralsPrep
 SELECT 
 Person_ID
 ,UniqServReqID
 ,RecordNumber
 ,Der_FY
 ,UniqMonthID
 ,ReportingPeriodStartDate
 ,ReportingPeriodEndDate
 ,OrgIDProv
 ,CASE WHEN ServDischDate BETWEEN ReportingPeriodStartDate and ReportingPeriodEndDate THEN "Closed" ELSE "Open" END AS OpenStatus
 ,AgeServReferRecDate
 ,CASE WHEN Gender = '1' THEN 'M' WHEN Gender = '2' THEN 'F' ELSE NULL END as Gender
 ,ReferralRequestReceivedDate
 ,ServDischDate
 ,ReferRejectionDate
 ,ServTeamTypeRefToMH
 ,PrimReasonReferralMH
 ,UniqCareProfTeamID
 ,LADistrictAuth
 ,ROW_NUMBER()OVER(PARTITION BY Person_ID, UniqServReqID ORDER BY RecordNumber DESC) AS Ref_Dup --- flag to remove duplicated referral/team records when joining to outcomes 

 FROM  $db_output.nhse_pre_proc_referral 

 WHERE 
 (UniqMonthID BETWEEN $start_month_id AND $end_month_id)
 AND 
 (AgeServReferRecDate >= 18) --Age at referral was 18 and over
 AND (ReferralRequestReceivedDate >= '2019-04-01')
 AND (ReferRejectionDate IS NULL)
 AND (LADistrictAuth LIKE 'E%' OR LADistrictAuth IS NULL OR LADistrictAuth = "") ---to limit to those people whose commissioner is an English organisation 
 AND (ServTeamTypeRefToMH  IN ('A06','A09','A08','A05','A16','A13','A12') )-- specific CMH service types - excluding EIP
 AND (PrimReasonReferralMH <> '08' OR PrimReasonReferralMH IS NULL) -- exclude referrals for organic brain disorder
 AND (ReportingPeriodStartDate BETWEEN '$rp_startdate_qtr' AND '$rp_enddate')
 AND (ServDischDate BETWEEN ReportingPeriodStartDate AND ReportingPeriodEndDate)
     

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.CMHProms_Inpatients
 SELECT Person_ID, UniqServReqID, COUNT(Der_HospSpellRecordOrder) AS Der_HospSpellCount
 FROM $db_output.Der_NHSE_Pre_Proc_Inpatients  ---using this table as it has Der_HospSpellRecordOrder deriavtion
 WHERE StartDateHospProvSpell <= '$rp_enddate' 
 GROUP BY Person_ID, UniqServReqID

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.CMHProms_Referrals

 SELECT 
 DISTINCT ---selecting distinct as same referral could have been referred to different servteamtype/careprofteamid in month
  r.Person_ID
 ,r.UniqServReqID
 ,r.RecordNumber
 ,r.Der_FY
 ,r.UniqMonthID
 ,r.ReportingPeriodStartDate
 ,r.ReportingPeriodEndDate
 ,r.OrgIDProv
 ,CASE WHEN r.ServDischDate BETWEEN r.ReportingPeriodStartDate and r.ReportingPeriodEndDate THEN "Closed" ELSE "Open" END AS OpenStatus
 ,COALESCE(o.NAME,'UNKNOWN') AS Provider_Name
 ,COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') AS SubICB_Code
 ,COALESCE(stp.CCG_Name, co.CCG_Name,'UNKNOWN') AS SubICB_Name
 ,COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') AS ICB_Code
 ,COALESCE(stp.STP_Name, co.STP_Name,'UNKNOWN') AS ICB_Name
 ,COALESCE(stp.Region_Code, co.Region_Code,'UNKNOWN') AS Region_Code
 ,COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') AS Region_Name
 ,r.AgeServReferRecDate
 ,CASE WHEN r.Gender = '1' THEN 'M' WHEN r.Gender = '2' THEN 'F' ELSE NULL END as Gender
 ,r.ReferralRequestReceivedDate
 ,r.ServDischDate
 ,r.ReferRejectionDate
 ,r.PrimReasonReferralMH
 ,r.ServTeamTypeRefToMH
 ,r.Ref_Dup

 FROM $db_output.CMHProms_ReferralsPrep r 
  
 LEFT JOIN $db_output.CMHProms_Inpatients i ON i.Person_ID = r.Person_ID AND i.UniqServReqID = r.UniqServReqID ---to identify referrals to inpatient services (and subsequently remove) 
  
 LEFT JOIN $db_output.bbrb_org_daily_latest o ON r.OrgIDProv = o.ORG_CODE ---provider reference data
 LEFT JOIN $db_output.bbrb_ccg_in_quarter ccg on r.Person_ID = ccg.Person_ID
 LEFT JOIN $db_output.bbrb_stp_mapping stp on ccg.SubICBGPRes = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.commissioning_org_mapping co ON ccg.SubICBGPRes_Mapped = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'

 WHERE (i.Der_HospSpellCount IS NULL) ---to exclude referrals with an associated hospital spell 


# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.CMHProms_Contacts
 SELECT distinct
 r.Person_ID
 ,r.UniqServReqID
 ,r.UniqMonthID
 ,r.ReportingPeriodEndDate
 ,r.RecordNumber 
 ,a.Der_ContactDate
 ,a.Der_ContactOrder
 ,a.Der_DirectContact
 ,ROW_NUMBER() OVER(PARTITION BY r.Person_ID, r.UniqServReqID ORDER BY a.Der_ContactDate ASC) AS ContactCount
 FROM $db_output.CMHProms_Referrals r  --discharged referrals in the rp
 INNER JOIN $db_output.Der_NHSE_Pre_Proc_Activity a --direct activity only
 ON r.Person_ID = a.Person_ID AND a.UniqServReqID = r.UniqServReqID -- get all contacts associated with the referral
 WHERE a.Der_DirectContact = 1
 and r.Ref_Dup =1 --join to latest referral record only

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.CMHProms_AllAssessments

 SELECT DISTINCT
 r.Person_ID
 ,r.UniqServReqID
 ,r.RecordNumber
 ,r.UniqMonthID
 ,r.ReportingPeriodEndDate
 ,r.OrgIDProv
 ,a.Der_AssUniqID
 ,a.Der_AssTable
 ,a.Der_AssToolCompDate
 ,a.CodedAssToolType
 ,a.Der_PreferredTermSNOMED
 ,a.Der_AssessmentToolName
 ,a.Der_AssessmentCategory
 ,a.PersScore
 ,a.Der_ValidScore
 ,a.Der_AssOrderAsc

 FROM $db_output.CMHProms_Referrals r

 INNER JOIN $db_output.nhse_pre_proc_assessments_unique_valid_outcomes a ON r.Person_ID = a.Person_ID AND r.UniqServReqID = a.UniqServReqID 

 LEFT JOIN $db_output.cmh_proms_ass mh ON a.CodedAssToolType = mh.Active_Concept_ID_SNOMED
 WHERE mh.Assessment_Tool_Name IS NOT NULL and mh.Preferred_Term_SNOMED IS NOT NULL 

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.CMHProms_PairedAssessments
 SELECT DISTINCT
 r.Person_ID
 ,r.UniqServReqID
 ,r.RecordNumber
 ,r.Der_FY
 ,r.UniqMonthID
 ,r.ReportingPeriodStartDate
 ,r.OrgIDProv 
 ,r.AgeServReferRecDate AS Age
 ,r.Gender
 ,r.ReferralRequestReceivedDate
 ,r.ServDischDate
 ,a1.Der_AssUniqID
 ,a1.Der_PreferredTermSNOMED 
 ,a1.Der_AssessmentToolName  
 ,a1.Der_AssessmentCategory
 ,a1.Der_AssToolCompDate
 ,a1.Der_AssOrderAsc
 ,c.Der_ContactDate as SecondContact
 ,c.ContactCount

 FROM $db_output.CMHProms_Referrals r  
 LEFT JOIN $db_output.CMHProms_Contacts c ON r.Person_ID = c.Person_ID AND r.UniqServReqID = c.UniqServReqID AND c.ContactCount =2 --only bringing second contact through

 LEFT JOIN $db_output.CMHProms_AllAssessments a1
     ON r.Person_ID = a1.Person_ID 
     AND r.UniqServReqID = a1.UniqServReqID 
     AND a1.Der_ValidScore = 'Y'


# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.CMHProms_Master

 SELECT DISTINCT
 	r.Person_ID
 	,r.UniqServReqID
 	,r.RecordNumber
 	,r.ServTeamTypeRefToMH
 	,r.PrimReasonReferralMH
 	,r.Der_FY
 	,r.UniqMonthID
 	,r.ReportingPeriodStartDate 
 	,r.ReportingPeriodEndDate
 	,r.OpenStatus
 	,r.OrgIDProv 
 	,r.Provider_Name
 	,r.Region_Code 
 	,r.Region_Name
 	,r.SubICB_Code as CCG_Code
 	,r.SubICB_Name as CCG_Name
 	,r.ICB_Code as STP_Code
 	,r.ICB_Name as STP_Name
 	,r.AgeServReferRecDate AS Age
 	,r.Gender
 	,r.ReferralRequestReceivedDate
 	,r.ServDischDate
 	,p.Der_AssessmentToolName
 	,p.Der_PreferredTermSNOMED
 	,p.SecondContact
 	,p.ContactCount
 	,p.Der_AssOrderAsc
 	,r.Ref_Dup

 FROM $db_output.CMHProms_Referrals r

 LEFT JOIN $db_output.CMHProms_PairedAssessments p ON r.RecordNumber = p.RecordNumber AND r.UniqServReqID = p.UniqServReqID 

 WHERE (r.UniqMonthID BETWEEN ($end_month_id -2)AND $end_month_id)
 and Ref_Dup = 1