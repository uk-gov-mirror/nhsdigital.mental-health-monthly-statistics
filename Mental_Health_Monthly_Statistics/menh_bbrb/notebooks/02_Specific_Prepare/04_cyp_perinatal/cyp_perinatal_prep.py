# Databricks notebook source
 %sql
 CREATE OR REPLACE TEMPORARY VIEW Ref AS
 SELECT
     r.UniqMonthID,
     r.OrgIDProv,
     CASE 
       WHEN r.OrgIDProv in ('DFC','S9X2N','F9R5H') THEN CONCAT(r.OrgIDProv, r.LocalPatientID)
       ELSE r.Person_ID
       END AS Person_ID,
     r.RecordNumber,
     r.UniqServReqID,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          else r.IC_Rec_CCG end as Der_OrgComm,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          else r.IC_Rec_CCG_Mapped end as Der_OrgComm_Mapped,
     r.LADistrictAuth,
     r.AgeServReferRecDate,
     r.AgeRepPeriodEnd,
     r.NHSDEthnicity,
     mpi.LowerEthnicity,
     mpi.LowerEthnicity_Desc,
     mpi.UpperEthnicity,
     mpi.WNW_Ethnicity,
     mpi.Gender,
     mpi.GenderIDCode,
     mpi.Der_Gender, 
     mpi.Der_Gender_Desc,
     ab.Age_Group_CYP as Age_Band,
     mpi.IMD_Decile,
     mpi.IMD_Quintile,
     mpi.IMD_Core20
  
 FROM $db_output.nhse_pre_proc_referral r
 LEFT JOIN $db_output.mhs001mpi_12_months_data mpi on r.Person_ID = mpi.Person_ID and r.RecordNumber = mpi.RecordNumber
 LEFT JOIN $db_output.age_band_desc ab on r.AgeServReferRecDate = ab.AgeRepPeriodEnd and '$end_month_id' >= ab.FirstMonth and (ab.LastMonth is null or '$end_month_id' <= ab.LastMonth)
  
 WHERE r.AgeServReferRecDate BETWEEN 0 AND 17 AND 
 r.UniqMonthID BETWEEN '$end_month_id' -11 AND '$end_month_id' 
 AND (r.LADistrictAuth LIKE 'E%' OR r.LADistrictAuth IS NULL OR r.LADistrictAuth = '')

# COMMAND ----------

 %sql

 CREATE OR REPLACE TEMPORARY VIEW GP_PRACTICE_CCG AS

 SELECT GP.UniqMonthID,
     GP.Person_ID,
     GP.OrgIDCCGGPPractice,
     GP.OrgIDSubICBLocGP,
     COALESCE(mp.TargetOrganisationID, mp2.TargetOrganisationID) as OrgIDSubICBLocGP_Mapped,
     GP.RecordNumber
 FROM $db_source.MHS002GP GP
     INNER JOIN 
                 (
                 SELECT UniqMonthID,
                         Person_ID, 
                         MAX(RecordNumber) as RecordNumber
                     FROM $db_source.MHS002GP
                     WHERE GMPReg NOT IN ('V81999','V81998','V81997') AND EndDateGMPRegistration is NULL
                 GROUP BY UniqMonthID, Person_ID
                 ) max_GP  
                 ON GP.Person_ID = max_GP.Person_ID 
                 AND GP.RecordNumber = max_GP.RecordNumber
                 AND GP.UniqMonthID = max_GP.UniqMonthID

 LEFT JOIN (select distinct uniqmonthid, reportingperiodenddate from $db_source.mhs000header) h ON GP.UniqMonthID = h.UniqMonthID
 LEFT JOIN $db_output.OrgIDSubICBLocGP_Mapping mp ON GP.GMPReg = mp.OrganisationID ---new Apr26 GP Codes
 LEFT JOIN $db_output.OrgIDSubICBLocGP_Mapping_preApr26 mp2 ON GP.GMPReg = mp2.OrganisationID 
                                 and (mp2.GP_EndDate is null OR mp2.GP_EndDate >= h.reportingperiodenddate)
                                 and (mp2.SubICB_EndDate is null OR mp2.SubICB_EndDate >= h.reportingperiodenddate)
 WHERE GP.GMPReg NOT IN ('V81999','V81998','V81997') AND GP.EndDateGMPRegistration is NULL

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW Ref_filtF01 AS -- Need to recreate nhse_pre_proc_referral as missing ServTeamType variable
 SELECT
     r.UniqMonthID,
     r.OrgIDProv,
     CASE 
       WHEN r.OrgIDProv in ('DFC','S9X2N','F9R5H') THEN CONCAT(r.OrgIDProv, r.LocalPatientID)
       ELSE r.Person_ID
       END AS Person_ID,
     r.RecordNumber,
     r.UniqServReqID,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          WHEN m.UniqMonthID <= 1467 and gp.OrgIDCCGGPPractice is not null then gp.OrgIDCCGGPPractice
          WHEN m.UniqMonthID > 1467 and gp.OrgIDSubICBLocGP is not null then gp.OrgIDSubICBLocGP
          WHEN m.UniqMonthID <= 1467 then m.OrgIDCCGRes
          WHEN m.UniqMonthID > 1467 then m.OrgIDSubICBLocResidence
          ELSE 'ERROR' END as Der_OrgComm,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          WHEN m.UniqMonthID <= 1467 and gp.OrgIDCCGGPPractice is not null then gp.OrgIDCCGGPPractice
          WHEN m.UniqMonthID > 1467 and gp.OrgIDSubICBLocGP_Mapped is not null then gp.OrgIDSubICBLocGP_Mapped
          WHEN m.UniqMonthID <= 1467 then m.OrgIDCCGRes
          WHEN m.UniqMonthID > 1467 then m.OrgIDSubICBLocResidence_Mapped
          ELSE 'ERROR' END as Der_OrgComm_Mapped,
     m.LADistrictAuth,
     r.AgeServReferRecDate,
     m.AgeRepPeriodEnd,
     m.NHSDEthnicity,
     mpi.LowerEthnicity,
     mpi.LowerEthnicity_Desc,
     mpi.UpperEthnicity,
     mpi.WNW_Ethnicity,
     mpi.Gender,
     mpi.GenderIDCode,
     mpi.Der_Gender, 
     mpi.Der_Gender_Desc,
     ab.Age_Group_CYP as Age_Band,
     mpi.IMD_Decile,
     mpi.IMD_Quintile,
     mpi.IMD_Core20
 FROM $db_source.mhs101referral r
 INNER JOIN (
   SELECT m.Person_ID, m.UniqMonthID, m.RecordNumber, m.OrgIDCCGRes, m.OrgIDSubICBLocResidence, m.LADistrictAuth, m.AgeRepPeriodEnd, m.NHSDEthnicity,
          mp.CCG as OrgIDSubICBLocResidence_Mapped
   FROM $db_source.mhs001mpi m 
   LEFT JOIN $db_output.OrgIDSubICBLocResidence_Mapping mp ON regexp_replace(m.Postcode, '\\s+', '') = regexp_replace(mp.PCDS, '\\s+', '')
 ) m
 ON r.RecordNumber = m.RecordNumber
 LEFT JOIN GP_Practice_CCG gp
 ON r.Person_ID = gp.Person_ID
 AND m.UniqMonthID = gp.UniqMonthID
 LEFT JOIN $db_output.mhs001mpi_12_months_data mpi on r.Person_ID = mpi.Person_ID and r.RecordNumber = mpi.RecordNumber
 LEFT JOIN $db_output.age_band_desc ab on r.AgeServReferRecDate = ab.AgeRepPeriodEnd and '$end_month_id' >= ab.FirstMonth and (ab.LastMonth is null or '$end_month_id' <= ab.LastMonth)
 INNER JOIN $db_output.ServiceTeamType s
 ON s.RecordNumber = r.RecordNumber
 AND s.UniqServReqID = r.UniqServReqID
 AND s.ServTeamTypeRefToMH in ('F01') --Education based services only 
 and s.uniqmonthid between '$end_month_id'-11 AND '$end_month_id'
  
 WHERE r.AgeServReferRecDate BETWEEN 0 AND 17 AND 
 r.UniqMonthID BETWEEN '$end_month_id' -11 AND '$end_month_id' 
 AND (m.LADistrictAuth LIKE 'E%' OR m.LADistrictAuth IS NULL OR m.LADistrictAuth = '')

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW Comb AS
 SELECT
     CASE 
       WHEN c.OrgIDProv in ('DFC','S9X2N','F9R5H') THEN CONCAT(m.OrgIDProv, m.LocalPatientID)
       ELSE c.Person_ID
       END AS Person_ID,
     c.RecordNumber,
     c.UniqServReqID,
     c.CareContDate AS Der_ContactDate,
     c.AgeCareContDate
  
 FROM $db_source.MHS201CareContact c
 LEFT JOIN $db_source.MHS001MPI m ON c.RecordNumber = m.RecordNumber
  
 WHERE 
   (
     ( c.AttendStatus IN ('5', '6') and ((c.ConsMechanismMH NOT IN ('05', '06') and c.UniqMonthID < '1459') or (c.ConsMechanismMH IN ('01', '02', '04', '11') and c.UniqMonthID >= '1459')))   
 -------/*** ConsMediumUsed' will change to 'ConsMechanismMH', code '06' will change to '09' from Oct 2021 data /*** updated to v5 AM ***/
     or 
     ( ((c.ConsMechanismMH IN ('05', '06') and c.UniqMonthID < '1459') or (c.ConsMechanismMH IN ('05', '09', '10', '13') and c.UniqMonthID >= '1459')) and c.OrgIdProv in ('DFC','S9X2N','F9R5H')) 
    )-------/*** ConsMediumUsed' will change to 'ConsMechanismMH', code '06' will change to '09' from Oct 2021 data V5.0 /*** updated to v5 AM ***/
 UNION ALL
  
 SELECT
     CASE 
       WHEN i.OrgIDProv in ('DFC','S9X2N','F9R5H') THEN CONCAT(m.OrgIDProv, m.LocalPatientID)
       ELSE i.Person_ID
       END AS Person_ID,
     i.RecordNumber,
     i.UniqServReqID,
     i.IndirectActDate AS Der_ContactDate,
     NULL AS AgeCareContDate
  
 FROM $db_source.MHS204IndirectActivity i
 LEFT JOIN $db_source.MHS001MPI m ON i.RecordNumber = m.RecordNumber

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW Act AS 
  
 SELECT
     r.UniqMonthID,
     r.OrgIDProv,
     r.Der_OrgComm,
     r.Der_OrgComm_Mapped,
     r.LADistrictAuth,
     r.Person_ID,
     r.RecordNumber,
     r.UniqServReqID,
     COALESCE(a.AgeCareContDate,r.AgeRepPeriodEnd) AS Der_ContAge,
     r.LowerEthnicity,
     r.LowerEthnicity_Desc,
     r.UpperEthnicity,
     r.WNW_Ethnicity,
     r.Gender,
     r.GenderIDCode,
     r.Der_Gender, 
     r.Der_Gender_Desc,         
     r.AgeRepPeriodEnd,
     r.Age_Band,
     r.IMD_Decile,
     r.IMD_Quintile,
     r.IMD_Core20,
     a.Der_ContactDate
  
 FROM Comb a
 INNER JOIN Ref r ON a.RecordNumber = r.RecordNumber AND a.UniqServReqID = r.UniqServReqID
  
 WHERE COALESCE(a.AgeCareContDate,r.AgeRepPeriodEnd) BETWEEN 0 AND 17

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW Act_filtF01 AS 
  
 SELECT
     r.UniqMonthID,
     r.OrgIDProv,
     r.Der_OrgComm,
     r.Der_OrgComm_Mapped,
     r.LADistrictAuth,
     r.Person_ID,
     r.RecordNumber,
     r.UniqServReqID,
     COALESCE(a.AgeCareContDate,r.AgeRepPeriodEnd) AS Der_ContAge,
     r.LowerEthnicity,
     r.LowerEthnicity_Desc,
     r.UpperEthnicity,
     r.WNW_Ethnicity,
     r.Gender,
     r.GenderIDCode,
     r.Der_Gender, 
     r.Der_Gender_Desc,         
     r.AgeRepPeriodEnd,
     r.Age_Band,
     r.IMD_Decile,
     r.IMD_Quintile,
     r.IMD_Core20,
     a.Der_ContactDate
  
 FROM Comb a
 INNER JOIN Ref_filtF01 r ON a.RecordNumber = r.RecordNumber AND a.UniqServReqID = r.UniqServReqID
  
 WHERE COALESCE(a.AgeCareContDate,r.AgeRepPeriodEnd) BETWEEN 0 AND 17

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW Act_cumulative AS 
  
 SELECT
     r.UniqMonthID,
     r.OrgIDProv,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          else ccg.SubICBGPRes end as Der_OrgComm,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          else ccg.SubICBGPRes_Mapped end as Der_OrgComm_Mapped,
     r.Person_ID,
     r.RecordNumber,
     r.UniqServReqID,
     a.AgeCareContDate AS Der_ContAge,
     r.ReferralRequestReceivedDate,
     r.ServDischDate,
     a.Der_ContactDate,
     DENSE_RANK() OVER (PARTITION BY r.UniqServReqID ORDER BY a.Der_ContactDate ASC, A.AgeCareContDate ASC) AS Der_ContactOrder
  
 FROM $db_source.mhs101referral r
  
 LEFT JOIN Comb a ON a.UniqServReqID = r.UniqServReqID AND a.AgeCareContDate BETWEEN 0 AND 17
  
 LEFT JOIN $db_source.mhs001mpi m 
       ON ((M.RecordEndDate is null or M.RecordEndDate >= '$rp_enddate') and m.recordstartdate < '$rp_enddate') and r.person_id = m.person_id and r.orgidprov = m.orgidprov AND M.PatMRecInRp = True
       
 LEFT JOIN $db_output.bbrb_ccg_in_year ccg on m.Person_ID = ccg.Person_ID
  
 WHERE 
 ((r.RecordEndDate is null or r.RecordEndDate >= '$rp_enddate') and r.recordstartdate < '$rp_enddate')
 AND r.AgeServReferRecDate BETWEEN 0 AND 17  
 AND (m.LADistrictAuth LIKE 'E%' OR m.LADistrictAuth IS NULL OR LADistrictAuth = '')
 AND ReferralRequestReceivedDate >= '2019-04-01'

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.Act_cumulative_master
 SELECT 
 DISTINCT 
 UniqMonthID,
 OrgIDProv,
 Der_OrgComm,
 Person_ID,
 RecordNumber,
 UniqServReqID,
 Der_ContAge,
 ReferralRequestReceivedDate,
 ServDischDate,
 Der_ContactDate,
 Der_ContactOrder,
 o.NAME AS PROVIDER_NAME,
 COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') AS CCG_Code,
 COALESCE(stp.CCG_Name, co.CCG_Name,'UNKNOWN') AS CCG_Name,
 COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') AS STP_Code,
 COALESCE(stp.STP_Name, co.STP_Name,'UNKNOWN') AS STP_Name,
 COALESCE(stp.Region_Code, co.Region_Code,'UNKNOWN') AS Region_Code,
 COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') AS Region_Name,
 DATEDIFF(Der_ContactDate, ReferralRequestReceivedDate) as TimeFromRefToFirstCont,
 DATEDIFF(DATE_ADD('$rp_enddate',1), ReferralRequestReceivedDate) as TimeFromRefToEndRP
 FROM Act_cumulative A
 LEFT JOIN $db_output.bbrb_stp_mapping stp on A.Der_OrgComm = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.commissioning_org_mapping co ON A.Der_OrgComm_Mapped = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.bbrb_org_daily_latest o on a.OrgIDProv = o.ORG_CODE

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.Act_cumulative_master_first_contact
 SELECT DISTINCT * FROM $db_output.Act_cumulative_master A
 WHERE DER_CONTACTORDER = '1' 
 AND Der_ContactDate BETWEEN '$rp_startdate_qtr' and '$rp_enddate'

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.Act_cumulative_master_still_waiting
  
 SELECT DISTINCT * FROM $db_output.Act_cumulative_master A
 WHERE DER_CONTACTORDER = '1' 
 AND DER_CONTACTDATE IS NULL 
 AND UNIQMONTHID = '$end_month_id'
 AND (SERVDISCHDATE IS NULL OR SERVDISCHDATE > '$rp_enddate')

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW Ref109 AS
  
 SELECT
     r.UniqMonthID,
     r.OrgIDProv,
     CASE 
       WHEN r.OrgIDProv in ('DFC','S9X2N','F9R5H') THEN CONCAT(r.OrgIDProv, r.LocalPatientID)
       ELSE r.Person_ID
       END AS Person_ID,
     r.RecordNumber,
     r.UniqServReqID,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          else r.IC_Rec_CCG end as Der_OrgComm,
     Case when r.OrgIDProv in ('DFC','S9X2N','F9R5H') then r.OrgIDComm
          else r.IC_Rec_CCG_Mapped end as Der_OrgComm_Mapped,
     r.LADistrictAuth,
     r.AgeServReferRecDate,    
     r.AgeRepPeriodEnd,
     r.NHSDEthnicity,
     mpi.LowerEthnicity,
     mpi.LowerEthnicity_Desc,
     mpi.UpperEthnicity,
     mpi.WNW_Ethnicity,
     mpi.Gender,
     mpi.GenderIDCode,
     mpi.Der_Gender, 
     mpi.Der_Gender_Desc,     
     ab.Age_Group_CYP as Age_Band,
     mpi.IMD_Decile,
     mpi.IMD_Quintile,
     mpi.IMD_Core20
  
 FROM $db_output.nhse_pre_proc_referral r
 LEFT JOIN $db_output.mhs001mpi_12_months_data mpi on r.Person_ID = mpi.Person_ID and r.RecordNumber = mpi.RecordNumber
 LEFT JOIN $db_output.age_band_desc ab on r.AgeServReferRecDate = ab.AgeRepPeriodEnd and '$end_month_id' >= ab.FirstMonth and (ab.LastMonth is null or '$end_month_id' <= ab.LastMonth)
  
 WHERE r.AgeServReferRecDate BETWEEN 18 AND 24 AND 
 r.UniqMonthID BETWEEN '$end_month_id' -11 AND '$end_month_id' 
 AND (r.LADistrictAuth LIKE 'E%' OR r.LADistrictAuth IS NULL OR r.LADistrictAuth = '')

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW Act109 AS 
  
 SELECT
     r.UniqMonthID,
     r.OrgIDProv,
     r.Der_OrgComm,
     r.Der_OrgComm_Mapped,
     r.LADistrictAuth,
     r.Person_ID,
     r.RecordNumber,
     r.UniqServReqID,
     r.AgeRepPeriodEnd,
     COALESCE(a.AgeCareContDate,r.AgeRepPeriodEnd) AS Der_ContAge,
     r.LowerEthnicity,
     r.LowerEthnicity_Desc,
     r.UpperEthnicity,
     r.WNW_Ethnicity,
     r.Gender,
     r.GenderIDCode,
     r.Der_Gender, 
     r.Der_Gender_Desc,     
     r.Age_Band,
     r.IMD_Decile,
     r.IMD_Quintile,
     r.IMD_Core20,
     a.Der_ContactDate
  
 FROM Comb a
 INNER JOIN Ref109 r ON a.RecordNumber = r.RecordNumber AND a.UniqServReqID = r.UniqServReqID
  
 WHERE COALESCE(a.AgeCareContDate,r.AgeRepPeriodEnd) BETWEEN 18 AND 24

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.FirstCont_Final
 SELECT
     a.UniqMonthID,
     a.OrgIDProv,
     o.NAME AS Provider_Name,
     COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') AS CCG_Code,
     COALESCE(stp.CCG_Name, co.CCG_Name,'UNKNOWN') AS CCG_Name,
     COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') AS STP_Code,
     COALESCE(stp.STP_Name, co.STP_Name,'UNKNOWN') AS STP_Name,
     COALESCE(stp.Region_Code, co.Region_Code,'UNKNOWN') AS Region_Code,
     COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') AS Region_Name,
     a.LADistrictAuth,
     a.Person_ID,
     a.RecordNumber,
     a.UniqServReqID,
     a.LowerEthnicity,
     a.LowerEthnicity_Desc,
     a.UpperEthnicity,    
     a.WNW_Ethnicity,
     a.Der_Gender,     
     a.Der_Gender_Desc,
     a.AgeRepPeriodEnd,
     a.Age_Band,
     a.IMD_Decile,
     a.IMD_Quintile,
     a.IMD_Core20,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, a.LADistrictAuth ORDER BY a.Der_ContactDate ASC) AS AccessLARN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessCCGRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN'), a.OrgIDProv ORDER BY a.Der_ContactDate ASC) AS AccessCCGProvRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, a.OrgIDProv ORDER BY a.Der_ContactDate ASC) AS AccessProvRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID ORDER BY a.Der_ContactDate ASC) AS AccessEngRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessSTPRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessRegionRN,
     'MHS95' AS Metric-- add metric id to table
  
 FROM Act as a
 LEFT JOIN $db_output.bbrb_stp_mapping stp on A.Der_OrgComm = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.commissioning_org_mapping co ON A.Der_OrgComm_Mapped = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.bbrb_org_daily_latest  o on a.OrgIDProv = o.ORG_CODE

# COMMAND ----------

 %sql
 INSERT INTO $db_output.FirstCont_Final
 SELECT
     a.UniqMonthID,
     a.OrgIDProv,
     o.NAME AS Provider_Name,
     COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') AS CCG_Code,
     COALESCE(stp.CCG_Name, co.CCG_Name,'UNKNOWN') AS CCG_Name,
     COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') AS STP_Code,
     COALESCE(stp.STP_Name, co.STP_Name,'UNKNOWN') AS STP_Name,
     COALESCE(stp.Region_Code, co.Region_Code,'UNKNOWN') AS Region_Code,
     COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') AS Region_Name,
     a.LADistrictAuth,
     a.Person_ID,
     a.RecordNumber,
     a.UniqServReqID,
     a.LowerEthnicity,
     a.LowerEthnicity_Desc,
     a.UpperEthnicity,    
     a.WNW_Ethnicity,
     a.Der_Gender,     
     a.Der_Gender_Desc,
     a.AgeRepPeriodEnd,
     a.Age_Band,
     a.IMD_Decile,
     a.IMD_Quintile,
     a.IMD_Core20,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, a.LADistrictAuth ORDER BY a.Der_ContactDate ASC) AS AccessLARN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessCCGRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN'), a.OrgIDProv ORDER BY a.Der_ContactDate ASC) AS AccessCCGProvRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, a.OrgIDProv ORDER BY a.Der_ContactDate ASC) AS AccessProvRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID ORDER BY a.Der_ContactDate ASC) AS AccessEngRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessSTPRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessRegionRN,
     'MHS159' AS Metric-- add metric id to table
  
 FROM Act_filtF01 as a
 LEFT JOIN $db_output.bbrb_stp_mapping stp on A.Der_OrgComm = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.commissioning_org_mapping co ON A.Der_OrgComm_Mapped = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.bbrb_org_daily_latest  o on a.OrgIDProv = o.ORG_CODE

# COMMAND ----------

 %sql
 INSERT INTO $db_output.FirstCont_Final ---Using insert into here as inserting data into table above but for different Metric
  
 SELECT
     a.UniqMonthID,
     a.OrgIDProv,
     o.NAME AS Provider_Name,
     COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') AS CCG_Code,
     COALESCE(stp.CCG_Name, co.CCG_Name,'UNKNOWN') AS CCG_Name,
     COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') AS STP_Code,
     COALESCE(stp.STP_Name, co.STP_Name,'UNKNOWN') AS STP_Name,
     COALESCE(stp.Region_Code, co.Region_Code,'UNKNOWN') AS Region_Code,
     COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') AS Region_Name,
     a.LADistrictAuth,
     a.Person_ID,
     a.RecordNumber,
     a.UniqServReqID,
     a.LowerEthnicity,
     a.LowerEthnicity_Desc,
     a.UpperEthnicity,    
     a.WNW_Ethnicity,
     a.Der_Gender, 
     a.Der_Gender_Desc,         
     a.AgeRepPeriodEnd,
     a.Age_Band,
     a.IMD_Decile,
     a.IMD_Quintile,
     a.IMD_Core20,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, a.LADistrictAuth ORDER BY a.Der_ContactDate ASC) AS AccessLARN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessCCGRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.CCG_Code, co.CCG_Code,'UNKNOWN'), a.OrgIDProv ORDER BY a.Der_ContactDate ASC) AS AccessCCGProvRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, a.OrgIDProv ORDER BY a.Der_ContactDate ASC) AS AccessProvRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID ORDER BY a.Der_ContactDate ASC) AS AccessEngRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.STP_Code, co.STP_Code,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessSTPRN,
     ROW_NUMBER () OVER(PARTITION BY a.Person_ID, COALESCE(stp.Region_Name, co.Region_Name,'UNKNOWN') ORDER BY a.Der_ContactDate ASC) AS AccessRegionRN,
     'MHS109' AS Metric-- add metric id to table
  
 FROM Act109 as A
 LEFT JOIN $db_output.bbrb_stp_mapping stp on A.Der_OrgComm = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.commissioning_org_mapping co ON A.Der_OrgComm_Mapped = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'
 LEFT JOIN $db_output.bbrb_org_daily_latest  o on a.OrgIDProv = o.ORG_CODE

# COMMAND ----------

 %sql
 OPTIMIZE $db_output.FirstCont_Final

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW perinatal_refs AS
  
 SELECT DISTINCT
 r.UniqMonthID,
 r.RecordNumber,
 r.Person_ID,
 r.ServiceRequestId,
 r.UniqServReqID,
 r.OrgIDProv,
 r.ReferralRequestReceivedDate,
 COALESCE(stp.CCG_Code, co.CCG_Code, 'UNKNOWN') AS IC_Rec_CCG,
 COALESCE(stp.CCG_Name, co.CCG_Name, 'UNKNOWN') AS CCG_NAME,
 m.LADistrictAuth,
 coalesce(eth.LowerEthnicityCode, "UNKNOWN") as LowerEthnicityCode,
 coalesce(eth.LowerEthnicityName, "UNKNOWN") as LowerEthnicityName,
 coalesce(eth.UpperEthnicity, "UNKNOWN") as UpperEthnicity,
 COALESCE(stp.STP_Code, co.STP_Code, 'UNKNOWN') AS STP_Code,
 COALESCE(stp.STP_Name, co.STP_Name, 'UNKNOWN') AS STP_Name,
 COALESCE(stp.Region_Code, co.Region_Code, 'UNKNOWN') AS Region_Code,
 COALESCE(stp.Region_Name, co.Region_Name, 'UNKNOWN') AS Region_Name
  
 FROM $db_source.MHS101Referral r
 INNER JOIN $db_output.ServiceTeamType s
 ON s.RecordNumber = r.RecordNumber
 AND s.UniqServReqID = r.UniqServReqID
 AND s.ServTeamTypeRefToMH in ('C02', 'F02') --Specialist Perinatal Services 
 and s.uniqmonthid between '$end_month_id'-11 AND '$end_month_id'
  
 INNER JOIN $db_source.MHS001MPI m
 ON m.recordnumber = r.recordnumber
 AND CASE
         WHEN '$end_month_id' >= 1477 and m.GenderIDCode in ('2','3') THEN '1' -- Gender Identity Code is female or non-binary (including trans women)
         WHEN '$end_month_id' >= 1477 and m.GenderIDCode= '1' and m.GenderSameAtBirth = 'N' THEN '1' -- Gender identity code is Male but Gender is not same as birth
         WHEN '$end_month_id' >= 1477 and m.GenderIDCode is null and m.Gender = '2' THEN '1' -- Gender identity not recorded so Female Person Stated Gender
         WHEN '$end_month_id' < 1477 and m.GenderIDCode = '2' THEN '1'
         WHEN '$end_month_id' < 1477 and (m.GenderIDCode is null or m.GenderIDCode not IN ('1','2','3','4','X','Z')) and m.Gender = '2' THEN '1' 
         ELSE '0' 
         END = '1' -- updated added new gender field jan 2022
 AND (m.LADistrictAuth IS NULL OR m.LADistrictAuth LIKE ('E%') or ladistrictauth = '')
 and m.uniqmonthid between '$end_month_id'-11 AND '$end_month_id'
  
 LEFT JOIN $db_output.ethnicity_desc eth on m.NHSDEthnicity = eth.LowerEthnicityCode and '$end_month_id' >= eth.FirstMonth and (eth.LastMonth is null or '$end_month_id' <= eth.LastMonth)
  
 LEFT JOIN $db_output.bbrb_ccg_in_year ccg on m.Person_ID = ccg.Person_ID

 LEFT JOIN $db_output.bbrb_stp_mapping stp on ccg.SubICBGPRes = stp.CCG_Code and '$end_month_id' < '$apr26_icb_swap_month_id'

 LEFT JOIN $db_output.commissioning_org_mapping co ON ccg.SubICBGPRes_Mapped = co.CCG_Code and '$end_month_id' >= '$apr26_icb_swap_month_id'
  
 WHERE r.UniqMonthID BETWEEN '$end_month_id'-11 AND '$end_month_id'

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW conts12 AS
 ---Prior October 2021
 SELECT
 r.UniqMonthID,
 r.Person_ID,
 r.RecordNumber,
 r.LADistrictAuth,
 r.LowerEthnicityCode,
 r.LowerEthnicityName,
 r.OrgIDProv,
 r.IC_Rec_CCG,
 r.UniqServReqID,
 c.UniqCareContID,
 c.CareContDate AS Der_ContactDate,
 r.STP_Code,
 r.Region_Code
  
 FROM perinatal_refs r
 INNER JOIN $db_source.MHS201CareContact c 
 ON r.RecordNumber = c.RecordNumber 
 AND r.UniqServReqID = c.UniqServReqID 
 AND c.AttendStatus IN ('5','6') AND c.ConsMechanismMH IN ('01', '03') and c.UniqMonthid < '1459'
  
 UNION ALL
 ---After October 2021 (dataset version change)
  
 SELECT
 r.UniqMonthID,
 r.Person_ID,
 r.RecordNumber,
 r.LADistrictAuth,
 r.LowerEthnicityCode,
 r.LowerEthnicityName,
 r.OrgIDProv,
 r.IC_Rec_CCG,
 r.UniqServReqID,
 c.UniqCareContID,
 c.CareContDate AS Der_ContactDate,
 r.STP_Code,
 r.Region_Code
  
 FROM perinatal_refs r
 INNER JOIN $db_source.MHS201CareContact c 
 ON r.RecordNumber = c.RecordNumber 
 AND r.UniqServReqID = c.UniqServReqID 
 AND c.AttendStatus IN ('5','6') AND c.ConsMechanismMH IN ('01', '11') and c.UniqMonthid >= '1459'

# COMMAND ----------

 %sql
 CREATE OR REPLACE TEMPORARY VIEW contYTD AS
  
 SELECT
 c.UniqMonthID,
 c.Person_ID,
 c.RecordNumber,
 c.LADistrictAuth,
 c.OrgIDProv,
 c.IC_Rec_CCG,
 c.UniqServReqID,
 c.UniqCareContID,
 c.STP_Code,
 c.Region_Code,
 ROW_NUMBER () OVER(PARTITION BY c.Person_ID, c.LADistrictAuth ORDER BY c.UniqMonthID ASC, c.Der_ContactDate ASC, c.UniqCareContID ASC) AS FYAccessLARN,
 ROW_NUMBER () OVER(PARTITION BY c.Person_ID, c.IC_Rec_CCG ORDER BY c.UniqMonthID ASC, c.Der_ContactDate ASC, c.UniqCareContID ASC) AS FYAccessCCGRN,
 ROW_NUMBER () OVER(PARTITION BY c.Person_ID, c.OrgIDProv ORDER BY c.UniqMonthID ASC, c.Der_ContactDate ASC, c.UniqCareContID ASC) AS FYAccessProvRN,
 ROW_NUMBER () OVER(PARTITION BY c.Person_ID ORDER BY c.UniqMonthID ASC, c.Der_ContactDate ASC, c.UniqCareContID ASC) AS FYAccessEngRN,
 ROW_NUMBER () OVER(PARTITION BY c.Person_ID, c.STP_Code ORDER BY c.UniqMonthID ASC, c.Der_ContactDate ASC, c.UniqCareContID ASC) AS FYAccessSTPRN,
 ROW_NUMBER () OVER(PARTITION BY c.Person_ID, c.Region_Code ORDER BY c.UniqMonthID ASC, c.Der_ContactDate ASC, c.UniqCareContID ASC) AS FYAccessRegionRN
  
 FROM Conts12 c
  
 WHERE c.UniqMonthID BETWEEN '$end_month_id'-11 AND '$end_month_id'

# COMMAND ----------

 %sql
 INSERT OVERWRITE TABLE $db_output.Perinatal_M_Master
  
 SELECT DISTINCT
 r.UniqMonthID,
 r.Person_ID,
 r.UniqServReqID,
 r.OrgIDProv,
 o.NAME as Provider_Name,
 COALESCE(r.IC_Rec_CCG, "UNKNOWN") as CCG_Code,
 COALESCE(co.CCG_Name, "UNKNOWN") as CCG_Name, --Changed to pull out latest CCG Name
 r.STP_Code,
 COALESCE(co.STP_Name, "UNKNOWN") as STP_Name,
 r.REGION_CODE as Region_Code,
 COALESCE(co.Region_Name, "UNKNOWN") as Region_Name,
 COALESCE(r.LADistrictAuth,'Unknown') AS LACode,
 r.LowerEthnicityCode,
 r.LowerEthnicityName,
 r.UpperEthnicity,
 CASE WHEN c1.Contacts >0 THEN 1 ELSE NULL END AS AttContacts,
 CASE WHEN c1.Contacts = 0 THEN 1 ELSE NULL END AS NotAttContacts,
 c2.FYAccessLARN, 
 c2.FYAccessProvRN,
 c2.FYAccessCCGRN,
 c2.FYAccessSTPRN,
 c2.FYAccessRegionRN,
 c2.FYAccessEngRN
  
 FROM perinatal_refs r    
  
 LEFT JOIN 
        (
        SELECT
        c.UniqMonthID,
        c.RecordNumber,
        c.UniqServReqID,
        COUNT(c.UniqCareContID) AS Contacts
        FROM Conts12 c
        GROUP BY c.UniqMonthID, c.RecordNumber, c.UniqServReqID
        ) c1 ON r.RecordNumber = c1.RecordNumber AND r.UniqServReqID = c1.UniqServReqID
  
 LEFT JOIN ContYTD c2 
        ON r.RecordNumber = c2.RecordNumber
        AND r.UniqServReqID = c2.UniqServReqID
        AND (c2.FYAccessProvRN = 1 
             OR c2.FYAccessCCGRN = 1
             OR c2.FYAccessSTPRN = 1
             OR c2.FYAccessRegionRN = 1)   
    
 LEFT JOIN $db_output.bbrb_org_daily_latest o
       ON r.OrgIDProv = o.ORG_CODE 
    
 LEFT JOIN $db_output.commissioning_org_mapping co ON r.IC_Rec_CCG = co.CCG_Code

# COMMAND ----------

 %sql
 OPTIMIZE $db_output.Perinatal_M_Master