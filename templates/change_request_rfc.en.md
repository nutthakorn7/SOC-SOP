# Request for Change (RFC)

> **Instructions**: Complete all sections before submitting to the Change Advisory Board (CAB). Emergency changes may skip CAB but require SOC Manager + CISO verbal approval and retrospective review within 48 hours.

---

## Header

| Field | Value |
|:---|:---|
| **RFC ID** | #RFC-YYYYMMDD-XX |
| **Requester** | [Name / Role] |
| **Date Submitted** | YYYY-MM-DD |
| **Target Date** | YYYY-MM-DD |
| **Change Type** | ☐ Standard · ☐ Normal · ☐ Emergency |
| **Priority** | ☐ Critical · ☐ High · ☐ Medium · ☐ Low |
| **Environment** | ☐ Production · ☐ Staging · ☐ Development |

---

## 1. Description of Change

*What exactly is being changed? Be specific about components, versions, and configurations.*

| Aspect | Details |
|:---|:---|
| **Component** | [SIEM / EDR / SOAR / Network / Other] |
| **Change Summary** | [e.g., Deploy new detection rule 'Detect Mimikatz T1003'] |
| **Scope** | [Which systems/tenants/regions affected] |
| **Version** | From: [current] → To: [target] |

---

## 2. Justification

*Why is this change necessary? What risk does it mitigate?*

| Question | Answer |
|:---|:---|
| **Business Need** | |
| **Risk Mitigated** | |
| **Consequences of NOT Changing** | |
| **Regulatory Requirement?** | ☐ Yes (specify) · ☐ No |

---

## 3. Impact Analysis

| Dimension | Assessment |
|:---|:---|
| **Affected Components** | [List all systems] |
| **Affected Teams** | [SOC / IT Ops / Network / Users] |
| **Risk of Failure** | ☐ Low · ☐ Medium · ☐ High |
| **Downtime Required** | ☐ Yes (duration: ____) · ☐ No |
| **Performance Impact** | ☐ None · ☐ Temporary degradation · ☐ Significant |
| **False Positive Risk** | ☐ Low · ☐ Medium · ☐ High (for detection rules) |
| **User Notification Needed** | ☐ Yes · ☐ No |

---

## 4. Implementation Plan

| # | Step | Responsible | Duration | Checkpoint |
|:---:|:---|:---|:---|:---|
| 1 | Pre-change backup/snapshot | | | ☐ |
| 2 | [Implementation step] | | | ☐ |
| 3 | [Implementation step] | | | ☐ |
| 4 | Post-change validation | | | ☐ |
| 5 | Monitoring period | | | ☐ |

**Maintenance Window**: YYYY-MM-DD HH:MM – HH:MM (UTC)

---

## 5. Testing & Validation

| Test | Expected Result | Actual Result | Pass? |
|:---|:---|:---|:---:|
| Functional test | | | ☐ |
| Performance test | | | ☐ |
| Alert validation (if detection rule) | | | ☐ |
| No regression on existing rules | | | ☐ |

---

## 6. Rollback Plan

*Step-by-step instructions to revert the change if it fails.*

| # | Rollback Step | Responsible | Duration |
|:---:|:---|:---|:---|
| 1 | | | |
| 2 | | | |
| 3 | Verify rollback successful | | |

**Rollback Trigger**: [What conditions trigger a rollback?]
**Maximum Acceptable Downtime**: [Duration]

---

## 7. Communication Plan

| When | Who | Channel | Message |
|:---|:---|:---|:---|
| Before change | [Affected teams] | [Email/Chat] | Planned change notification |
| During change | [SOC team] | [Chat] | Status updates |
| After change | [All stakeholders] | [Email] | Completion confirmation |
| If failed | [Management] | [Phone + Email] | Rollback notification |

---

## 8. Approval (CAB)

| Role | Name | Decision | Date |
|:---|:---|:---:|:---|
| SOC Manager | | ☐ Approved · ☐ Rejected | |
| IT Operations | | ☐ Approved · ☐ Rejected | |
| Security Lead | | ☐ Approved · ☐ Rejected | |
| CISO (Critical only) | | ☐ Approved · ☐ Rejected | |

**CAB Decision**: ☐ Approved · ☐ Approved with Conditions · ☐ Deferred · ☐ Rejected

**Conditions (if any)**:
> 

---

## 9. Post-Implementation Review

| Metric | Value |
|:---|:---|
| **Change Successful?** | ☐ Yes · ☐ Partial · ☐ No (rolled back) |
| **Actual Implementation Time** | |
| **Issues Encountered** | |
| **Lessons Learned** | |
| **Follow-up Actions** | |

---

## Related Documents

- [Deployment Procedures](../02_Platform_Operations/Deployment_Procedures.en.md)
- [Incident Report Template](incident_report.en.md)
- [Change Management SOP](../06_Operations_Management/Change_Management.en.md)
- [SOC Assessment Checklist](../06_Operations_Management/SOC_Assessment_Checklist.en.md)

## References

- [ITIL Change Management](https://www.axelos.com/certifications/itil-service-management)
- [NIST SP 800-128 — Configuration Management](https://csrc.nist.gov/publications/detail/sp/800-128/final)
