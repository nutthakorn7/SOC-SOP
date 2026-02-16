# Playbook: Privilege Escalation

**ID**: PB-07
**Severity**: High/Critical | **Category**: Identity & Access / Endpoint
**MITRE ATT&CK**: [T1068](https://attack.mitre.org/techniques/T1068/) (Exploitation for Privilege Escalation), [T1098](https://attack.mitre.org/techniques/T1098/) (Account Manipulation), [T1078.002](https://attack.mitre.org/techniques/T1078/002/) (Domain Accounts)
**Trigger**: EDR alert ("Mimikatz detected", "LSASS access"), SIEM ("Member added to Domain Admins"), UEBA anomaly

---

## Decision Flow

```mermaid
graph TD
    Alert["🚨 Privilege Escalation Alert"] --> Method{"⚙️ Escalation Method?"}
    Method -->|Group Membership Change| Group["👥 Added to Admin Group"]
    Method -->|Exploit / Tool| Tool["🔧 Exploit Tool Detected"]
    Method -->|Configuration Change| Config["⚙️ GPO / Policy Modification"]
    Group --> Ticket{"📋 Change Request?"}
    Ticket -->|Yes, Authorized| FP["✅ False Positive"]
    Ticket -->|No| Suspicious["🔴 Unauthorized"]
    Tool --> ToolType{"Which Tool?"}
    ToolType -->|Mimikatz / LSASS Dump| Cred["🔴 Credential Theft"]
    ToolType -->|Local Exploit (CVE)| Vuln["🔴 Vulnerability Exploit"]
    ToolType -->|UAC Bypass| UAC["🟠 UAC Bypass"]
    Config --> Authorized{"Authorized Change?"}
    Authorized -->|No| Suspicious
    Suspicious --> Isolate["🔌 Isolate + Investigate"]
    Cred --> Isolate
    Vuln --> Isolate
    UAC --> Isolate
```

---

## 1. Analysis

### 1.1 Escalation Method Identification

| Method | Detection | Event IDs / Artifacts |
|:---|:---|:---|
| **Domain Admin group add** | SIEM, AD audit | 4728, 4732 (group member added) |
| **Local Admin group add** | SIEM, EDR | 4732 (local group) |
| **Mimikatz / credential dump** | EDR | LSASS access, sekurlsa::\* |
| **Token manipulation** | EDR, Sysmon | Process token changes, SeDebugPrivilege |
| **UAC bypass** | EDR, Sysmon | fodhelper.exe, eventvwr.exe abuse |
| **Kernel exploit (CVE)** | EDR, IDS | Exploit artifacts, crash dumps |
| **Sudo/SUID abuse** | Linux audit | sudo logs, SUID file execution |
| **GPO modification** | AD audit | GPO changes in SYSVOL |
| **Scheduled task as SYSTEM** | Sysmon, SIEM | 4698 (task created), SYSTEM context |

### 1.2 Investigation Checklist

| Check | How | Done |
|:---|:---|:---:|
| What process/tool performed the escalation? | EDR process timeline | ☐ |
| Was it authorized? (Change request, admin work) | ITSM / Change Management | ☐ |
| Which account gained elevated privileges? | AD audit log | ☐ |
| What did the elevated account do next? | SIEM / EDR timeline | ☐ |
| Was the source host already compromised? | EDR alerts, malware presence | ☐ |
| Was credential dumping involved? | LSASS access, process injection | ☐ |
| Were other systems accessed with elevated creds? | [PB-12 Lateral Movement](Lateral_Movement.en.md) | ☐ |

---

## 2. Containment

### 2.1 Immediate Actions

| # | Action | Tool | Done |
|:---:|:---|:---|:---:|
| 1 | **Remove** escalated privileges / group membership | AD / IdP | ☐ |
| 2 | **Disable** the suspicious account | AD / IdP | ☐ |
| 3 | **Isolate** the source host | EDR | ☐ |
| 4 | **Kill** the exploit/tool process | EDR | ☐ |
| 5 | **Block** the exploit hash across all endpoints | EDR global blacklist | ☐ |

### 2.2 If Credential Theft Confirmed

| # | Action | Done |
|:---:|:---|:---:|
| 1 | Reset passwords of ALL accounts accessed from compromised host | ☐ |
| 2 | Check for Pass-the-Hash / Pass-the-Ticket usage | ☐ |
| 3 | If Domain Admin creds dumped, plan KRBTGT reset (twice, 12h apart) | ☐ |
| 4 | Audit all lateral movement from this host → [PB-12](Lateral_Movement.en.md) | ☐ |
| 5 | Check for DCSync (Event ID 4662 with replication GUIDs) | ☐ |

---

## 3. Eradication

| # | Action | Done |
|:---:|:---|:---:|
| 1 | Remove exploit tools / malware from host | ☐ |
| 2 | Patch the vulnerability used for escalation (if CVE-based) | ☐ |
| 3 | Review GPOs for unauthorized modifications | ☐ |
| 4 | Scan for backdoors: new accounts, scheduled tasks, services | ☐ |
| 5 | Check for persistence in registry, WMI, startup | ☐ |
| 6 | Re-image host if Mimikatz/credential dump confirmed | ☐ |

---

## 4. Recovery

| # | Action | Done |
|:---:|:---|:---:|
| 1 | Restore permission baseline from documented standard | ☐ |
| 2 | Full AD audit — compare current vs baseline group memberships | ☐ |
| 3 | Enable Credential Guard on workstations | ☐ |
| 4 | Implement LAPS for local admin passwords | ☐ |
| 5 | Deploy/verify Protected Users group for sensitive accounts | ☐ |
| 6 | Monitor recovered host and accounts for 72 hours | ☐ |

---

## 5. IoC Collection

| Type | Value | Source |
|:---|:---|:---|
| Exploit tool/binary hash | | EDR |
| Escalated account name | | AD audit |
| Process used for escalation | | EDR |
| Source host | | SIEM |
| CVE exploited (if applicable) | | IDS / EDR |
| Lateral movement destinations | | SIEM |

---

## 6. Escalation Criteria

| Condition | Escalate To |
|:---|:---|
| Domain Admin credentials compromised | CISO + External IR |
| Mimikatz / credential dumping confirmed | Tier 2 + Identity team |
| Multiple hosts affected | Major Incident |
| GPO modified without authorization | CISO + AD team |
| Kernel exploit (0-day) | CISO + Vendor |
| Data accessed with elevated privileges | [PB-08](Data_Exfiltration.en.md) + Legal |

---

## Related Documents

- [IR Framework](../Framework.en.md)
- [Incident Report](../../templates/incident_report.en.md)
- [PB-05 Account Compromise](Account_Compromise.en.md)
- [PB-12 Lateral Movement](Lateral_Movement.en.md)
- [PB-15 Rogue Admin](Rogue_Admin.en.md)

## References

- [MITRE ATT&CK T1068 — Exploitation for Privilege Escalation](https://attack.mitre.org/techniques/T1068/)
- [MITRE ATT&CK T1098 — Account Manipulation](https://attack.mitre.org/techniques/T1098/)
- [Microsoft — Securing Privileged Access](https://learn.microsoft.com/en-us/security/compass/securing-privileged-access)
