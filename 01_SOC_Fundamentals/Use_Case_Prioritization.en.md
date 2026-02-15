# Detection Use Case Prioritization — What to Detect First

> **Document ID:** UC-001  
> **Version:** 1.0  
> **Last Updated:** 2026-02-15  
> **Prerequisite:** SIEM installed, at least 3 log sources onboarded

---

## The Problem

There are thousands of possible detection rules. You can't deploy them all at once. This guide tells you **what to detect first** based on real-world threat data and your available log sources.

---

## The Framework: MITRE ATT&CK Top 10

Based on industry data (Mandiant M-Trends, Verizon DBIR, CrowdStrike threat reports), these are the most commonly used attack techniques:

| Rank | Technique | ID | What It Is | How Common |
|:---:|:---|:---|:---|:---:|
| 1 | Phishing | T1566 | Malicious email (link/attachment) | 🔴🔴🔴 |
| 2 | Valid Accounts | T1078 | Stolen/compromised credentials | 🔴🔴🔴 |
| 3 | Command & Scripting | T1059 | PowerShell, cmd, bash abuse | 🔴🔴 |
| 4 | Brute Force | T1110 | Password guessing/spraying | 🔴🔴 |
| 5 | Data Encrypted (Ransomware) | T1486 | File encryption for ransom | 🔴🔴 |
| 6 | Remote Services | T1021 | RDP, SSH, SMB lateral movement | 🔴🔴 |
| 7 | Ingress Tool Transfer | T1105 | Download malware/tools | 🔴 |
| 8 | Web Application Exploit | T1190 | SQLi, RCE against web apps | 🔴 |
| 9 | Process Injection | T1055 | Living-off-the-land techniques | 🔴 |
| 10 | Account Manipulation | T1098 | Persistence via account changes | 🔴 |

---

## Phase 1: Foundational Use Cases (Month 1–3)

**Goal:** Catch the most common and most impactful attacks.

### Deploy These 10 Rules First

| # | Use Case | Log Source | Sigma Rule | Playbook | Priority |
|:---:|:---|:---|:---|:---|:---:|
| 1 | Multiple failed logins (brute force) | AD / Azure AD | `win_multiple_failed_logins` | PB-04 | 🔴 P1 |
| 2 | Login from impossible location | Azure AD | `cloud_impossible_travel` | PB-06 | 🔴 P1 |
| 3 | Office app spawns PowerShell | EDR / Sysmon | `proc_office_spawn_powershell` | PB-01 | 🔴 P1 |
| 4 | Malware executed on endpoint | EDR | `proc_temp_folder_execution` | PB-03 | 🔴 P1 |
| 5 | Bulk file rename (ransomware) | EDR / Sysmon | `file_bulk_renaming_ransomware` | PB-02 | 🔴 P1 |
| 6 | New admin account created | AD | `win_new_admin_account` | PB-07 | 🟡 P2 |
| 7 | Security log cleared | Windows | `win_security_log_cleared` | PB-20 | 🟡 P2 |
| 8 | Login outside business hours | AD / Azure AD | `cloud_unusual_login` | PB-05 | 🟡 P2 |
| 9 | Suspicious email forwarding rule | M365 | `cloud_email_inbox_rule` | PB-17 | 🟡 P2 |
| 10 | Connection to known-bad IP | Firewall / Proxy | (custom rule) | PB-13 | 🟡 P2 |

### Metrics to Track
- How many alerts per day? (Target: < 50 for 1 analyst)
- False positive rate? (Accept < 60% in Phase 1, tune to < 40%)
- Mean time from alert to triage? (Target: < 30 min)

---

## Phase 2: Extended Coverage (Month 4–6)

**Goal:** Catch lateral movement, persistence, and cloud-specific threats.

### Add These 10 Rules

| # | Use Case | Log Source | Playbook | Priority |
|:---:|:---|:---|:---|:---:|
| 11 | Admin share access (lateral movement) | Sysmon/EDR | PB-12 | 🟡 P2 |
| 12 | Service installed (persistence) | Windows | PB-11 | 🟡 P2 |
| 13 | Encoded PowerShell execution | Sysmon | PB-11 | 🟡 P2 |
| 14 | DNS to suspicious TLD | DNS logs | PB-24 | 🟡 P2 |
| 15 | Large data upload (exfiltration) | Proxy / DLP | PB-08 | 🟡 P2 |
| 16 | Cloud IAM privilege escalation | CloudTrail / Azure | PB-16 | 🟡 P2 |
| 17 | Scheduled task created remotely | Sysmon | PB-12 | 🟢 P3 |
| 18 | Process injection (lsass.exe access) | Sysmon | PB-11 | 🟢 P3 |
| 19 | USB mass storage connected | EDR | PB-14 | 🟢 P3 |
| 20 | Failed MFA attempts (>5) | Azure AD | PB-26 | 🟢 P3 |

### New Log Sources to Add
- DNS resolver logs
- Cloud audit logs (CloudTrail/Azure Activity)
- Proxy/web gateway logs
- DLP if available

---

## Phase 3: Advanced Detection (Month 7–12)

**Goal:** Catch sophisticated, targeted attacks and insider threats.

### Add These 10 Rules

| # | Use Case | Log Source | Playbook | Priority |
|:---:|:---|:---|:---|:---:|
| 21 | Beaconing detection (regular intervals) | Proxy/NDR | PB-13 | 🟢 P3 |
| 22 | DNS tunneling (high-volume/long domains) | DNS | PB-24 | 🟢 P3 |
| 23 | S3/Blob made public | CloudTrail/Azure | PB-27 | 🟢 P3 |
| 24 | Shadow IT / unauthorized SaaS | Proxy/CASB | PB-29 | 🟢 P3 |
| 25 | Kerberoasting (SPN request anomaly) | AD | PB-15 | 🟢 P3 |
| 26 | DCSync (replication request) | AD | PB-15 | 🟢 P3 |
| 27 | Token/cookie theft (AiTM) | Azure AD | PB-26 | 🟢 P3 |
| 28 | DLL side-loading | EDR/Sysmon | PB-11 | ⚪ P4 |
| 29 | WMI remote execution | Sysmon | PB-12 | ⚪ P4 |
| 30 | OT/ICS protocol anomaly | OT network | PB-30 | ⚪ P4 |

---

## Phase 4: Threat Hunting (Year 2+)

Move from **alert-driven** to **hypothesis-driven** detection:

| Hunt Hypothesis | Data Needed | Frequency |
|:---|:---|:---:|
| "Are there compromised service accounts?" | AD auth logs, UEBA | Monthly |
| "Is anyone beaconing to C2?" | Proxy + DNS statistical analysis | Weekly |
| "Are VPN credentials shared or stolen?" | VPN logs + geolocation | Monthly |
| "Is sensitive data leaving the network?" | DLP + proxy + cloud storage | Weekly |
| "Are there dormant admin accounts?" | AD account audit | Monthly |
| "Are there unknown web shells on servers?" | Filesystem scan + YARA | Monthly |

---

## Use Case Template

When creating a new detection use case:

```markdown
## UC-[###]: [Use Case Name]

### Objective
What are we trying to detect?

### MITRE ATT&CK
- Technique: T[####]
- Tactic: [Initial Access / Execution / Persistence / ...]

### Data Sources Required
- [ ] Source 1 (event IDs or log types)
- [ ] Source 2

### Detection Logic
```
IF [condition]
AND [condition]
WITHIN [timeframe]
THEN alert_level = [low/medium/high/critical]
```

### Playbook
Reference: PB-[##]

### False Positive Scenarios
- [Expected benign behavior that may trigger this]
- [How to filter/whitelist]

### Tuning Notes
- Threshold: [initial value]
- Whitelist: [IPs/users/hosts to exclude]
- Review after: [2 weeks of baseline data]
```

---

## Coverage Heat Map

Track your detection coverage across MITRE tactics:

| Tactic | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|:---|:---:|:---:|:---:|:---:|
| Initial Access | ✅ | ✅ | ✅ | ✅ |
| Execution | ✅ | ✅ | ✅ | ✅ |
| Persistence | ⚠️ | ✅ | ✅ | ✅ |
| Privilege Escalation | ⚠️ | ✅ | ✅ | ✅ |
| Defense Evasion | ❌ | ⚠️ | ✅ | ✅ |
| Credential Access | ⚠️ | ⚠️ | ✅ | ✅ |
| Discovery | ❌ | ⚠️ | ⚠️ | ✅ |
| Lateral Movement | ❌ | ✅ | ✅ | ✅ |
| Collection | ❌ | ⚠️ | ✅ | ✅ |
| Exfiltration | ❌ | ⚠️ | ✅ | ✅ |
| Impact | ✅ | ✅ | ✅ | ✅ |

✅ = Covered | ⚠️ = Partial | ❌ = Not yet

---

## Prioritization Scoring Formula

If you need to prioritize beyond this guide, score each use case:

```
Score = (Likelihood × 3) + (Impact × 3) + (Data Readiness × 2) + (Effort × 2)

Likelihood:     1 (rare) to 5 (happens weekly)
Impact:         1 (low) to 5 (business-critical)
Data Readiness: 1 (no data source) to 5 (data already in SIEM)
Effort:         1 (weeks to build) to 5 (deploy in hours)

Score range: 10-50 → Start with highest scoring use cases
```

---

## Related Documents

- [SOC Building Roadmap](SOC_Building_Roadmap.en.md)
- [Detection Rules Index](../07_Detection_Rules/README.md)
- [Log Source Onboarding](../06_Operations_Management/Log_Source_Onboarding.en.md)
- [MITRE ATT&CK Heatmap](../tools/mitre_attack_heatmap.html)
