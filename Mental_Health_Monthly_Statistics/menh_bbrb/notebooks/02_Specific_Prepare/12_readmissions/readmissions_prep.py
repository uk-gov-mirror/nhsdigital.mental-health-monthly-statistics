# Databricks notebook source
 %md
 3-month rolling metrics, where the rp_startdate and rp_enddate is lagged by -14days for discharged referrals to allow enough time to monitor readmission rate

# COMMAND ----------

# DBTITLE 1,Get first ward stays in the rp
 %sql
 INSERT OVERWRITE TABLE $db_output.Readm_FirstWardStay
 SELECT DISTINCT 
 	i.UniqHospProvSpellID
 	,i.Person_ID
 	,i.UniqServReqID
 	,i.UniqMonthID
 	,i.RecordNumber
 	,i.ReportingPeriodStartDate
 	,i.ReportingPeriodEndDate
 	,i.OrgIDProv
 	,i.StartDateHospProvSpell
 	,i.StartTimeHospProvSpell
 	,i.DischDateHospProvSpell
 	,i.MethOfDischMHHospProvSpell
 	,i.DestOfDischHospProvSpell
 	,r.AgeRepPeriodEnd
 	,r.OrgIDCCGRes
 	,ia.UniqWardStayID AS UniqWardStayID_first 
 	,ia.StartDateWardStay AS StartDateWardStay_first 
 	,ia.StartTimeWardStay AS StartTimeWardStay_first 
 	,ia.UniqMonthID AS WS_UniqMonthID_first
     ,ia.MHAdmittedPatientClass AS HospitalBedTypeMH_first
 	
 FROM $db_output.nhse_pre_proc_inpatients i  

 LEFT JOIN $db_output.nhse_pre_proc_referral r ON i.RecordNumber = r.RecordNumber AND i.UniqServReqID = r.UniqServReqID 

 LEFT JOIN $db_output.der_nhse_pre_proc_inpatients ia ON i.UniqHospProvSpellID = ia.UniqHospProvSpellID AND i.UniqServReqID = ia.UniqServReqID and i.Person_ID = ia.Person_ID
 	AND ia.Der_FirstWardStayRecord = 1 -- get ward stay of admission 
 	
 WHERE (i.UniqMonthID BETWEEN ($end_month_id - 3) AND $end_month_id) -- include previous 4 months for the qtr - inclusive of the last 14 days in the previous rp

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.Readm_LatestWardStay
 SELECT 
 	s.UniqHospProvSpellID
 	,s.UniqServReqID
 	,s.Person_ID
 	,s.UniqMonthID
 	,i.UniqWardStayID
 	,i.RecordNumber
 	,i.StartDateWardStay
 	,i.StartTimeWardStay
 	,i.EndDateWardStay
 	,i.EndTimeWardStay
 	,i.MHAdmittedPatientClass
 	,i.MHS502UniqID
 	,ROW_NUMBER () OVER(PARTITION BY i.Person_ID, i.UniqServReqID, i.UniqHospProvSpellID, i.UniqMonthID ORDER BY COALESCE(i.EndDateWardStay,'2100-12-31') DESC, i.MHS502UniqID DESC) AS WS_Order

 FROM $db_output.Readm_FirstWardStay s

 INNER JOIN $db_output.nhse_pre_proc_inpatients i ON i.UniqHospProvSpellID = s.UniqHospProvSpellID 
 	AND i.UniqServReqID = s.UniqServReqID 
 	AND i.Person_ID = s.Person_ID
 	AND i.UniqMonthID = s.UniqMonthID

# COMMAND ----------

 %sql
 -- All spells discharged in the RP
 -- Gets details for the first ward stay and latest ward stay

 INSERT OVERWRITE TABLE $db_output.Readm_AllSpells

 SELECT 
 a.Person_ID 
 ,a.UniqMonthID
 ,a.UniqHospProvSpellID
 ,a.UniqServReqID
 ,a.RecordNumber
 ,a.OrgIDProv
 ,e.NAME AS Provider_Name
 ,a.StartDateHospProvSpell
 ,a.DischDateHospProvSpell
 ,c.AgeRepPeriodEnd
 ,COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') AS CCG_Code
 ,COALESCE(stp.CCG_Name, co.CCG_Name,'UNKNOWN') AS CCG_Name
 ,COALESCE(stp.Region_Code, co.Region_Code,'UNKNOWN') AS Region_Code
 ,COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') AS Region_Name
 ,COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') AS STP_Code
 ,COALESCE(stp.STP_Name, co.STP_Name,'UNKNOWN') AS STP_Name
 ,a.MethOfDischMHHospProvSpell
 ,a.DestOfDischHospProvSpell
 ,CASE 
     WHEN(a.MethOfDischMHHospProvSpell NOT IN ('4','6','7','8') OR a.MethOfDischMHHospProvSpell IS NULL) THEN 1 
     ELSE 0 END AS Der_MethOfDischAccepted_Flag -- readmissions denom flag 
 ,CASE 
     WHEN(a.DestOfDischHospProvSpell NOT IN ('48','49','50','53','84','87','79') OR a.DestOfDischHospProvSpell IS NULL) THEN 1 
     ELSE 0 END AS Der_DestOfDischNotHospital_Flag -- readmissions denom flag 
 -- WS at admission
 ,a.UniqWardStayID_first 
 ,a.StartDateWardStay_first 
 ,a.WS_UniqMonthID_first
 ,a.HospitalBedTypeMH_first 
 ,CASE WHEN (a.UniqMonthID > 1488 AND a.HospitalBedTypeMH_first = '200') OR (a.UniqMonthID <= 1488 AND a.HospitalBedTypeMH_first = '10') THEN 'Adult Acute'
     WHEN (a.UniqMonthID > 1488 AND a.HospitalBedTypeMH_first = '201') OR (a.UniqMonthID <= 1488 AND a.HospitalBedTypeMH_first = '11') THEN 'Older Adult Acute'
     WHEN (a.UniqMonthID > 1488 AND a.HospitalBedTypeMH_first = '202') OR (a.UniqMonthID <= 1488 AND a.HospitalBedTypeMH_first = '12') THEN 'PICU'
     ELSE 'Invalid' END AS Acute_Bed_FirstCategory
 -- Latest WS
 ,z.UniqWardStayID AS UniqWardStayID_last
 ,z.StartDateWardStay AS StartDateWardStay_last
 ,z.UniqMonthID AS WS_UniqMonthID_last
 ,z.MHAdmittedPatientClass AS HospitalBedTypeMH_last
 ,CASE WHEN (z.UniqMonthID > 1488 AND z.MHAdmittedPatientClass = '200') OR (z.UniqMonthID <= 1488 AND z.MHAdmittedPatientClass = '10') THEN 'Adult Acute'
     WHEN (z.UniqMonthID > 1488 AND z.MHAdmittedPatientClass = '201') OR (z.UniqMonthID <= 1488 AND z.MHAdmittedPatientClass = '11') THEN 'Older Adult Acute'
     WHEN (z.UniqMonthID > 1488 AND z.MHAdmittedPatientClass = '202') OR (z.UniqMonthID <= 1488 AND z.MHAdmittedPatientClass = '12') THEN 'PICU'
     ELSE 'Invalid' END AS Acute_Bed_LastCategory

 -- Derivations 
 ,CASE WHEN a.StartDateHospProvSpell BETWEEN DATE_ADD('$rp_startdate_qtr',-15) AND '$rp_enddate' THEN 1 ELSE 0 END AS Der_Admission 
 ,CASE WHEN a.DischDateHospProvSpell BETWEEN DATE_ADD('$rp_startdate_qtr',-15) AND DATE_ADD('$rp_enddate',-15) THEN 1 ELSE 0 END AS Der_Discharge

 FROM $db_output.Readm_FirstWardStay a

 INNER JOIN $db_output.Readm_LatestWardStay z ON a.UniqHospProvSpellID = z.UniqHospProvSpellID 
 AND a.UniqServReqID = z.UniqServReqID 
 AND a.Person_ID = z.Person_ID
 AND a.UniqMonthID = z.UniqMonthID
 AND z.WS_Order = 1 

 LEFT JOIN $db_source.MHS001MPI c ON a.RecordNumber = c.RecordNumber AND a.Person_ID = c.Person_ID
 LEFT JOIN $db_output.bbrb_org_daily_latest E ON A.ORGIDPROV = E.ORG_CODE 
 LEFT JOIN $db_output.bbrb_ccg_in_4month ccg ON C.Person_ID = ccg.Person_ID
 LEFT JOIN $db_output.bbrb_stp_mapping stp on ccg.SubICBGPRes = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.commissioning_org_mapping co ON ccg.SubICBGPRes_Mapped = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'

# COMMAND ----------

 %sql
 -- Discharged spells with a subsequent admission after the discharge date.
 -- Excludes discharges where the patient died, discharged themselves or were transferred to another hospital

 INSERT OVERWRITE TABLE $db_output.Readm_ReadmittedSpells

 SELECT 
 	s.Person_ID
 	,s.RecordNumber
 	,s.UniqHospProvSpellID AS Index_HS
 	,s.StartDateHospProvSpell AS Index_StartDate
 	,s.DischDateHospProvSpell AS Index_DischDate
 	,a.UniqHospProvSpellID
 	,a.StartDateHospProvSpell 
 	,DATEDIFF(a.StartDateHospProvSpell, s.DischDateHospProvSpell) AS TimetoReadm 
 	,ROW_NUMBER()OVER(PARTITION BY s.Person_ID, s.UniqHospProvSpellID ORDER BY a.StartDateHospProvSpell ASC) AS FirstReAdm -- earliest readmission per index
 	,ROW_NUMBER()OVER(PARTITION BY a.Person_ID, a.UniqHospProvSpellID ORDER BY s.DischDateHospProvSpell DESC) AS LastDisch -- most recent discharge per (re)admission 

 FROM $db_output.Readm_AllSpells s 

 INNER JOIN $db_output.Readm_AllSpells a ON s.Person_ID = a.Person_ID
 	AND a.StartDateHospProvSpell >= s.DischDateHospProvSpell
 	AND a.Der_Admission = 1 
 	AND a.UniqHospProvSpellID <> s.UniqHospProvSpellID 

 WHERE s.Der_Discharge = 1 
 AND s.Der_MethOfDischAccepted_Flag = 1 
 AND s.Der_DestOfDischNotHospital_Flag = 1 

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.Readm_Master
 SELECT 
 s.UniqHospProvSpellID
 ,s.RecordNumber
 ,s.UniqServReqID
 ,s.Person_ID
 ,'$rp_startdate_qtr' AS ReportingPeriodStartDate
 ,'$rp_enddate' AS ReportingPeriodEndDate
 ,s.AgeRepPeriodEnd
 ,s.OrgIDProv
 ,s.Provider_Name
 ,s.CCG_Code
 ,s.CCG_Name
 ,s.Region_Code
 ,s.Region_Name
 ,s.STP_Code
 ,s.STP_Name
 ,s.HospitalBedTypeMH_last
 ,s.Acute_Bed_LastCategory
 ,s.Der_Discharge
 ,ra.Index_DischDate
 ,ra.StartDateHospProvSpell AS ReadmissionDate
 ,s.Der_MethOfDischAccepted_Flag
 ,s.Der_DestOfDischNotHospital_Flag
 ,CASE WHEN s.Der_MethOfDischAccepted_Flag = 1 AND s.Der_DestOfDischNotHospital_Flag = 1 THEN 1 ELSE 0 END Der_DischEligibleForReAdm_Flag
 ,ra.TimetoReadm --- time from discharge to next (unplanned) admission 

 FROM $db_output.Readm_AllSpells s 

 LEFT JOIN $db_output.Readm_ReadmittedSpells ra ON s.UniqHospProvSpellID = ra.Index_HS AND s.Person_ID = ra.Person_ID AND ra.FirstReAdm = 1 AND ra.LastDisch = 1 ANd s.Der_Discharge = 1 

 WHERE 
 s.Der_Discharge = 1 
 AND 
 (Acute_Bed_LastCategory <> "Invalid")

# COMMAND ----------

 %sql
 OPTIMIZE $db_output.Readm_Master