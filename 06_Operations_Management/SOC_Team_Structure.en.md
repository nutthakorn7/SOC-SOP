# SOC Team Structure & Roles

This document defines the organizational structure, roles, and responsibilities within the Security Operations Center (SOC).

## 1. Organizational Chart

```mermaid
graph TD
    CISO[CISO / VP of Security] --> Manager[SOC Manager]
    Manager --> Lead1[Team Lead - Shift A]
    Manager --> Lead2[Team Lead - Shift B]
    Manager --> Engineer[Detection Engineer]
    Manager --> TI[Threat Intelligence Analyst]
    Lead1 --> T2A[Tier 2 Analyst]
    Lead1 --> T1A1[Tier 1 Analyst]
    Lead1 --> T1A2[Tier 1 Analyst]
    Lead2 --> T2B[Tier 2 Analyst]
    Lead2 --> T1B1[Tier 1 Analyst]
    Lead2 --> T1B2[Tier 1 Analyst]

    style CISO fill:#1a1a2e,color:#fff
    style Manager fill:#16213e,color:#fff
    style Lead1 fill:#0f3460,color:#fff
    style Lead2 fill:#0f3460,color:#fff
    style Engineer fill:#533483,color:#fff
    style TI fill:#533483,color:#fff
```

## 2. Role Definitions

### 2.1 Tier 1 — Alert Analyst (Monitoring & Triage)
-   **Headcount**: 4-6 per SOC (2-3 per shift)
-   **Responsibilities**:
    -   Monitor SIEM dashboards and alert queues in real-time.
    -   Perform initial triage: True Positive vs. False Positive classification.
    -   Escalate confirmed incidents to Tier 2 with initial context.
    -   Document actions in the ticketing system.
-   **Skills Required**: CompTIA Security+, basic networking, log analysis.
-   **KPIs**: Alert Throughput, False Positive Rate, MTTD (Mean Time To Detect).

### 2.2 Tier 2 — Incident Responder (Investigation & Containment)
-   **Headcount**: 2-4 per SOC (1-2 per shift)
-   **Responsibilities**:
    -   Deep-dive investigation on escalated incidents.
    -   Execute Playbook containment and eradication steps.
    -   Perform host & network forensics (memory, disk, packet capture).
    -   Coordinate with IT teams for isolation and remediation.
-   **Skills Required**: CySA+, GCIH, EDR/SIEM advanced queries, forensics tools.
-   **KPIs**: MTTR (Mean Time To Respond), Incident Closure Rate.

### 2.3 Tier 3 — Threat Hunter / Senior Analyst
-   **Headcount**: 1-2 per SOC
-   **Responsibilities**:
    -   Proactive threat hunting using hypothesis-driven methodologies.
    -   Advanced malware analysis and reverse engineering.
    -   Develop custom detection content (Sigma, YARA, Snort).
    -   Lead major incident investigations and Root Cause Analysis (RCA).
-   **Skills Required**: GCIA, GCFA, OSCP, advanced scripting (Python, PowerShell).
-   **KPIs**: Threats Discovered, Detection Gap Reduction, TTPs Mapped to MITRE ATT&CK.

### 2.4 Detection Engineer
-   **Headcount**: 1-2 per SOC
-   **Responsibilities**:
    -   Create and maintain detection rules (Sigma/YARA/Snort).
    -   Tune rules to reduce False Positive Rate.
    -   Manage CI/CD pipeline for rule deployment.
    -   Maintain the MITRE ATT&CK coverage dashboard.
-   **Skills Required**: Sigma, regex, SIEM query languages (SPL, KQL, Lucene).

### 2.5 Threat Intelligence Analyst
-   **Headcount**: 1 per SOC
-   **Responsibilities**:
    -   Collect, analyze, and disseminate threat intelligence (CTI).
    -   Maintain threat feeds and IOC databases.
    -   Produce Threat Advisory reports for stakeholders.
    -   Map adversary TTPs to organizational risk.
-   **Skills Required**: CTIA, OSINT techniques, TLP classification, STIX/TAXII.

### 2.6 SOC Manager
-   **Headcount**: 1 per SOC
-   **Responsibilities**:
    -   Oversee daily SOC operations and shift scheduling.
    -   Set KPIs and report metrics to CISO/Leadership.
    -   Manage staffing, training, and career development.
    -   Coordinate with external teams (IT, Legal, HR) during major incidents.
    -   Budget management for tools and licensing.
-   **Skills Required**: CISSP, CISM, leadership and communication skills.

## 3. Career Progression Path

```mermaid
graph LR
    T1[Tier 1 Analyst] -->|1-2 Years| T2[Tier 2 Responder]
    T2 -->|2-3 Years| T3[Tier 3 Hunter]
    T2 -->|2-3 Years| DE[Detection Engineer]
    T2 -->|2-3 Years| TI[Threat Intel Analyst]
    T3 -->|3-5 Years| Lead[Team Lead]
    DE -->|3-5 Years| Lead
    TI -->|3-5 Years| Lead
    Lead -->|5+ Years| MGR[SOC Manager]
    MGR -->|7+ Years| CISO[CISO]
```

## 4. Recommended Staffing Model

| SOC Volume | Tier 1 | Tier 2 | Tier 3 | Det. Engineer | TI Analyst | Manager | Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Small** (<500 alerts/day) | 2 | 1 | 0 | 1 (shared) | 0 | 1 | 5 |
| **Medium** (500-2000/day) | 4 | 2 | 1 | 1 | 1 | 1 | 10 |
| **Large** (>2000/day, 24/7) | 8 | 4 | 2 | 2 | 1 | 1 | 18 |

## 5. Interview Questions by Tier

### Tier 1 Candidates
| # | Question | Expected Answer |
|:---|:---|:---|
| 1 | What is the difference between a True Positive and a False Positive? | TP = real threat confirmed; FP = alert triggered but not a real threat |
| 2 | You see 50 failed logins from one IP. What do you do? | Check if it's brute force, verify the source IP, check if account locked, escalate if confirmed |
| 3 | What is TLP:RED? | Restricted to named participants only — cannot be shared |
| 4 | Walk me through triaging a phishing alert. | Check sender, links, attachments, headers, check if user clicked, check IOCs in SIEM |
| 5 | What logs would you check for a Windows lateral movement alert? | Event IDs 4624/4625 (logon), 5140 (share access), Sysmon, EDR |

### Tier 2 Candidates
| # | Question | Expected Answer |
|:---|:---|:---|
| 1 | How would you investigate a suspected C2 callback? | Analyze network traffic (beaconing), check process tree, identify parent process, isolate host |
| 2 | Explain the MITRE ATT&CK kill chain. | Recon → Weaponize → Deliver → Exploit → Install → C2 → Actions on Objectives |
| 3 | When should you isolate a host vs. just monitoring? | Isolate: confirmed malware, active C2, data exfiltration. Monitor: suspicious but unconfirmed |
| 4 | Write a Splunk query to find PowerShell encoded commands. | `index=sysmon EventCode=1 CommandLine="*-enc*" OR CommandLine="*encodedcommand*"` |
| 5 | How do you determine the blast radius of a compromised account? | Check auth logs for where account logged in, file access, email rules, AD changes |

### Tier 3 Candidates
| # | Question | Expected Answer |
|:---|:---|:---|
| 1 | Describe your threat hunting methodology. | Hypothesis → data collection → analysis → findings → detection rule creation |
| 2 | How would you detect living-off-the-land attacks? | Monitor LOLBins (certutil, mshta, rundll32), parent-child process anomalies |
| 3 | Walk through your malware analysis workflow. | Sandbox → static (strings, imports, PE) → dynamic (behavior, C2) → YARA rule |
| 4 | How do you create a Sigma rule from an investigation finding? | Identify log source, define detection logic, set level/status, test against FP |
| 5 | How would you detect DNS tunneling? | Long subdomains, high query volume to single domain, entropy analysis |

## 6. Skills Matrix & Training Plan

| Skill | T1 Required | T2 Required | T3 Required | Training Resource |
|:---|:---:|:---:|:---:|:---|
| SIEM queries (basic) | ✅ | ✅ | ✅ | Internal training |
| SIEM queries (advanced) | ❌ | ✅ | ✅ | Splunk/Elastic cert |
| Networking (TCP/IP, DNS) | ✅ | ✅ | ✅ | CompTIA Network+ |
| Log analysis | ✅ | ✅ | ✅ | SANS SEC555 |
| Incident Response | Basic | ✅ | ✅ | GCIH / CySA+ |
| Forensics | ❌ | Basic | ✅ | GCFA / SANS FOR508 |
| Malware analysis | ❌ | ❌ | ✅ | GREM / SANS FOR610 |
| Threat hunting | ❌ | ❌ | ✅ | SANS FOR508 |
| Detection engineering | ❌ | Basic | ✅ | Internal + Sigma docs |
| Scripting (Python/PS) | ❌ | Basic | ✅ | Self-study / courses |
| MITRE ATT&CK | Awareness | Working | Expert | ATT&CK training |

## 7. Salary Benchmarks (Thailand Market, 2026)

> **Note**: Ranges are approximate and vary by organization size, industry, and location.

| Role | Experience | Monthly Range (THB) | Certifications that Add Value |
|:---|:---|:---|:---|
| T1 Analyst | 0-2 years | 25,000 – 45,000 | CompTIA Security+, CySA+ |
| T2 Analyst | 2-4 years | 40,000 – 70,000 | GCIH, CySA+, OSCP |
| T3 Analyst | 4-7 years | 60,000 – 100,000 | GCFA, GREM, OSCP |
| Detection Engineer | 3-5 years | 50,000 – 90,000 | Sigma/YARA expertise |
| TI Analyst | 3-5 years | 45,000 – 80,000 | CTIA, OSINT certs |
| SOC Manager | 5-10 years | 80,000 – 150,000 | CISSP, CISM |

## Related Documents
-   [Shift Handoff Standard](Shift_Handoff.en.md)
-   [SOC Metrics & KPIs](SOC_Metrics.en.md)
-   [Analyst Onboarding Path](../10_Training_Onboarding/Analyst_Onboarding_Path.en.md)
-   [Training Checklist](../10_Training_Onboarding/Training_Checklist.en.md)
-   [SOC Assessment Checklist](SOC_Assessment_Checklist.en.md)

## References
-   [NIST SP 800-61r2 (Incident Handling Guide)](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
-   [SOC-CMM — SOC Capability Maturity Model](https://www.soc-cmm.com/)
-   [SANS SOC Survey & Analyst Reports](https://www.sans.org/white-papers/soc-survey/)
-   [MITRE ATT&CK — Threat-Informed Defense](https://attack.mitre.org/)
-   [FIRST CSIRT Services Framework](https://www.first.org/standards/frameworks/csirts/csirt_services_framework_v2.1)
