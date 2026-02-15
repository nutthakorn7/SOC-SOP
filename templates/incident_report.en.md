# Incident Report Template

**Incident ID**: #YYYYMMDD-00X
**Date**: YYYY-MM-DD
**Analyst**: [Name]
**Severity**: [Low/Medium/High/Critical]
**TLP**: [RED/AMBER/GREEN/CLEAR]
**Status**: [Open/Closed]

## 1. Executive Summary
*Briefly describe what happened, the impact, and the resolution.*

## 2. Timeline (UTC)
-   **Detection**: [Time] - Alert triggered for [Rule Name].
-   **Analysis**: [Time] - Analyst verified malicious activity.
-   **Containment**: [Time] - Host isolated / User disabled.
-   **Eradication**: [Time] - Malicious files removed.
-   **Recovery**: [Time] - System returned to production.

## 3. Impact Assessment
-   **Affected Assets**: [List of Hostnames/Users]
-   **Data Loss**: [Yes/No - Details]
-   **Business Impact**: [Downtime duration, reputational risk]

## 4. Root Cause Analysis (VERIS "4A" Framework)
-   **Actor**: [External / Internal / Partner]
-   **Action**: [Malware / Hacking / Social / Error / Misuse]
-   **Asset**: [Server / User Dev / Person / Data]
-   **Attribute**: [Confidentiality / Integrity / Availability]
-   **Vulnerability**: [CVE-XXXX-XXXX if applicable]

## 5. Remediation & Lessons Learned
-   [ ] Action 1: Patch vulnerability X.
-   [ ] Action 2: Update detection rule Y to prevent recurrence.

## Related Documents
-   [Incident Response Framework](../05_Incident_Response/Framework.en.md)
-   [Shift Handover Template](shift_handover.en.md)
-   [Change Request (RFC)](change_request_rfc.en.md)

## References
-   [NIST SP 800-61 — Computer Security Incident Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
-   [SANS Incident Report Template](https://www.sans.org/information-security-policy/)
