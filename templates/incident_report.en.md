# Incident Report Template

> **Instructions**: Complete all mandatory sections (★) within 24 hours of incident closure. For Critical/High severity incidents, the executive summary must be submitted to management within 4 hours of detection.

---

## Header

| Field | Value |
|:---|:---|
| **Incident ID** | #YYYYMMDD-00X |
| **Date Detected** | YYYY-MM-DD HH:MM (UTC) |
| **Date Closed** | YYYY-MM-DD HH:MM (UTC) |
| **Analyst** | [Name / Role] |
| **Severity** | ☐ Critical · ☐ High · ☐ Medium · ☐ Low |
| **Status** | ☐ Open · ☐ Investigating · ☐ Contained · ☐ Closed |
| **TLP** | ☐ RED · ☐ AMBER+STRICT · ☐ AMBER · ☐ GREEN · ☐ CLEAR |
| **Category** | [Phishing / Malware / Ransomware / Account Compromise / DDoS / Data Breach / Other] |
| **MITRE ATT&CK** | [Technique IDs, e.g., T1566.001, T1059.001] |

---

## ★ 1. Executive Summary

*2–3 sentence overview: What happened, what was the impact, and what was the outcome?*

> 

---

## ★ 2. Timeline (UTC)

| Time | Phase | Event |
|:---|:---|:---|
| YYYY-MM-DD HH:MM | **Initial Activity** | First attacker action (if known) |
| YYYY-MM-DD HH:MM | **Detection** | Alert triggered by [Rule Name / Source] |
| YYYY-MM-DD HH:MM | **Triage** | Analyst acknowledged and began investigation |
| YYYY-MM-DD HH:MM | **Escalation** | Escalated to [Tier 2 / SOC Lead / Management] |
| YYYY-MM-DD HH:MM | **Containment** | [Action taken, e.g., host isolated, account disabled] |
| YYYY-MM-DD HH:MM | **Eradication** | [Action taken, e.g., malware removed, vulnerability patched] |
| YYYY-MM-DD HH:MM | **Recovery** | System returned to production |
| YYYY-MM-DD HH:MM | **Monitoring** | Enhanced monitoring period began |
| YYYY-MM-DD HH:MM | **Closure** | Incident declared resolved |

---

## ★ 3. Impact Assessment

| Dimension | Assessment |
|:---|:---|
| **Affected Hosts** | [List hostnames/IPs] |
| **Affected Users** | [Count + list if < 10] |
| **Affected Services** | [Applications, databases, etc.] |
| **Data Loss** | ☐ None · ☐ Suspected · ☐ Confirmed (details: ____) |
| **Data Type** | ☐ PII · ☐ Financial · ☐ Credentials · ☐ IP · ☐ Other |
| **Business Impact** | [Downtime duration, revenue impact, reputational risk] |
| **Regulatory Notification Required** | ☐ Yes (PDPA 72h / Other) · ☐ No |

---

## ★ 4. Root Cause Analysis

### VERIS "4A" Framework

| Dimension | Assessment |
|:---|:---|
| **Actor** | ☐ External · ☐ Internal · ☐ Partner · ☐ Unknown |
| **Action** | ☐ Malware · ☐ Hacking · ☐ Social Engineering · ☐ Error · ☐ Misuse · ☐ Physical |
| **Asset** | ☐ Server · ☐ Workstation · ☐ User Device · ☐ Network · ☐ Cloud · ☐ Person · ☐ Data |
| **Attribute** | ☐ Confidentiality · ☐ Integrity · ☐ Availability |

### Root Cause Detail

| Question | Answer |
|:---|:---|
| **What vulnerability was exploited?** | [CVE-XXXX-XXXX or description] |
| **How did the attacker gain access?** | [Initial access vector] |
| **What controls failed?** | [Detection gap, missing patch, etc.] |
| **Was this preventable?** | ☐ Yes (how) · ☐ No (why) |

---

## ★ 5. Indicators of Compromise (IoCs)

| Type | Value | Context |
|:---|:---|:---|
| IP Address | | [C2 / Scanner / Source] |
| Domain | | [Phishing / C2 / Staging] |
| File Hash (SHA256) | | [Malware / Tool] |
| Email Address | | [Sender / Recipient] |
| URL | | [Payload / Landing page] |
| File Path | | [Dropped / Modified] |
| Process | | [Suspicious / Malicious] |
| Registry Key | | [Persistence] |

---

## ★ 6. Remediation & Follow-up Actions

| # | Action | Owner | Status | Due Date |
|:---:|:---|:---|:---:|:---|
| 1 | | | ☐ Done · ☐ Pending | |
| 2 | | | ☐ Done · ☐ Pending | |
| 3 | | | ☐ Done · ☐ Pending | |
| 4 | Update detection rules | SOC | ☐ Done · ☐ Pending | |
| 5 | Update playbook if needed | SOC | ☐ Done · ☐ Pending | |

---

## 7. Lessons Learned

| Question | Answer |
|:---|:---|
| **What went well?** | |
| **What could be improved?** | |
| **Were playbooks followed?** | ☐ Yes · ☐ Partially · ☐ No |
| **Were SLAs met?** | ☐ Yes · ☐ No (detail: ____) |
| **Training gaps identified?** | |
| **Tool/process changes needed?** | |

---

## 8. Approvals

| Role | Name | Signature | Date |
|:---|:---|:---|:---|
| Lead Analyst | | | |
| SOC Manager | | | |
| CISO (Critical only) | | | |

---

## Related Documents

- [IR Framework](../05_Incident_Response/Framework.en.md)
- [Shift Handover Template](shift_handover.en.md)
- [Change Request (RFC)](change_request_rfc.en.md)
- [PDPA Compliance](../07_Compliance_Privacy/PDPA_Compliance.en.md)

## References

- [NIST SP 800-61r2 — Incident Handling](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [VERIS Framework](http://veriscommunity.net/)
- [SANS Incident Report Template](https://www.sans.org/information-security-policy/)
