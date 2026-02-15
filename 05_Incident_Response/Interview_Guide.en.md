# SOC Analyst Interview Guide

> **Document ID:** HR-001  
> **Version:** 1.0  
> **Last Updated:** 2026-02-15  
> **Audience:** SOC Managers, HR, Hiring Teams

---

## How to Use This Guide

Select questions based on the **tier level** you're hiring for. Include a mix of technical, scenario-based, and behavioral questions. Score each answer 1–5.

---

## Tier 1 — Junior SOC Analyst

### Technical Questions

**Q1: What is the difference between an IDS and an IPS?**
> **Good answer:** IDS (Intrusion Detection System) monitors and alerts. IPS (Intrusion Prevention System) monitors AND blocks. IDS is passive, IPS is inline.

**Q2: A user reports they clicked a suspicious link in an email. Walk me through your first 5 steps.**
> **Good answer:**
> 1. Don't panic — get details (email sender, URL, time clicked)
> 2. Check email headers — is the sender spoofed?
> 3. Check URL reputation (VirusTotal, URLhaus)
> 4. Check EDR — did anything execute on the user's machine?
> 5. If malicious → isolate endpoint, escalate to T2, block sender/URL

**Q3: What is a false positive? Give an example.**
> **Good answer:** An alert that fires but is not actually malicious. Example: vulnerability scanner triggering IDS alerts, or admin using PowerShell legitimately triggering a "suspicious script" alert.

**Q4: What common ports should a SOC analyst know?**
> **Good answer:** 80/443 (HTTP/HTTPS), 22 (SSH), 3389 (RDP), 53 (DNS), 25/587 (SMTP), 445 (SMB), 389/636 (LDAP), 88 (Kerberos)

**Q5: You see 500 failed login attempts from one IP in 5 minutes. What do you do?**
> **Good answer:** This is likely brute force (T1110). Check if any login succeeded after the failures. If external IP → block at firewall. If login succeeded → treat as account compromise, escalate. Check if other accounts targeted (password spray).

### Hands-On Test (15 min)
Give the candidate a sample SIEM alert (screenshot or mock) and ask:
1. What is the severity?
2. What would you investigate next?
3. Would you escalate? To whom?

---

## Tier 2 — Senior SOC Analyst

### Technical Questions

**Q1: Explain the MITRE ATT&CK framework. How do you use it in your daily work?**
> **Good answer:** Matrix of adversary tactics and techniques. Use it to: map alerts to techniques, identify coverage gaps, communicate with threat intel teams, prioritize detection rules.

**Q2: What's the difference between EDR and SIEM? When do you use each?**
> **Good answer:** SIEM aggregates logs from many sources, correlates events, provides broad visibility. EDR focuses on endpoints — process execution, file changes, network connections. Use SIEM for cross-source correlation, EDR for deep endpoint investigation and response (isolation, kill process).

**Q3: You're investigating a compromised Windows server. What artifacts do you look for?**
> **Good answer should include:**
> - Event logs (4624/4625/4688/1102)
> - Sysmon logs (process creation, network connections)
> - Scheduled tasks, services, registry run keys (persistence)
> - PowerShell history / transcript logs
> - Browser history, recent files
> - Memory dump (if available)
> - Prefetch files, shimcache, amcache

**Q4: What is Kerberoasting and how do you detect it?**
> **Good answer:** Attacker requests TGS tickets for service accounts with SPNs, then cracks the ticket offline to get the service account password. Detect via: Event ID 4769 with encryption type 0x17 (RC4), anomalous TGS volume from single account.

**Q5: Design a detection rule for lateral movement via PsExec.**
> **Good answer should cover:**
> - New service installed (Event ID 7045, service name "PSEXESVC")
> - Named pipe creation (\\pipe\psexesvc)
> - Remote process creation via admin share (\\target\ADMIN$)
> - Network connection to port 445 followed by service creation

### Scenario Test (30 min)
Present a multi-stage attack scenario (phishing → execution → lateral movement) with simulated SIEM data. Ask the candidate to:
1. Build a timeline
2. Identify IOCs
3. Determine the blast radius
4. Recommend containment steps

---

## SOC Lead / Manager

### Leadership Questions

**Q1: How do you measure SOC effectiveness?**
> **Good answer:** MTTD (Mean Time to Detect), MTTR (Mean Time to Respond), alert-to-ticket ratio, false positive rate, SLA compliance, coverage against MITRE ATT&CK, analyst satisfaction/retention.

**Q2: Your team has 50% false positive rate. How do you reduce it?**
> **Good answer:** 
> 1. Analyze top 10 noisiest rules
> 2. Work with detection engineering to tune thresholds/whitelists
> 3. Implement tiered alerting (info vs warning vs critical)
> 4. Establish a feedback loop — analysts flag FP → engineering tunes
> 5. Track FP rate per rule, set improvement targets

**Q3: How do you prevent analyst burnout in a 24/7 SOC?**
> **Good answer:** Fair shift rotation, limit consecutive night shifts, automate repetitive tasks (SOAR), meaningful work (not just clicking "close"), training/certification opportunities, recognition, career path visibility.

**Q4: You have a budget to add one tool. How do you decide what to buy?**
> **Good answer:** 
> 1. Assess current capability gaps (MITRE ATT&CK coverage)
> 2. Interview analysts — what slows them down most?
> 3. Evaluate: does this reduce MTTD, MTTR, or FP rate?
> 4. Consider: build (open-source) vs buy (vendor)
> 5. POC with top 2 vendors, test against real scenarios
> 6. Calculate ROI (hours saved × analyst cost)

---

## Behavioral Questions (All Tiers)

| Question | What You're Assessing |
|:---|:---|
| Tell me about a time you handled a stressful incident | Composure under pressure |
| Describe a time you escalated something and were wrong | Humility, learning from mistakes |
| How do you stay current on new threats? | Continuous learning |
| What's the most interesting security incident you've worked on? | Passion, depth of experience |
| How do you handle disagreements with colleagues about severity? | Communication, teamwork |

---

## Scoring Matrix

| Criteria | Weight | Score (1-5) |
|:---|:---:|:---:|
| Technical knowledge | 30% | ___ |
| Hands-on/scenario performance | 25% | ___ |
| Communication skills | 15% | ___ |
| Problem-solving approach | 15% | ___ |
| Cultural fit / teamwork | 10% | ___ |
| Learning mindset | 5% | ___ |
| **Weighted Total** | **100%** | **___** |

**Hiring threshold:** ≥ 3.5 weighted average

---

## Related Documents

- [SOC Team Structure](../06_Operations_Management/SOC_Team_Structure.en.md)
- [SOC Building Roadmap](../01_SOC_Fundamentals/SOC_Building_Roadmap.en.md)
- [Tier 1 Runbook](Tier1_Runbook.en.md)
