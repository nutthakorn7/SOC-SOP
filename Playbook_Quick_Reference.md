# 🛡️ SOC Playbook Quick Reference Card

> **Print this page** — A single-page reference for all 50 incident response playbooks.
>
> **พิมพ์หน้านี้** — สรุป Playbook ทั้ง 50 ในหน้าเดียว สำหรับแปะโต๊ะ Analyst

---

## 📧 Email & Social Engineering

| PB | Name / ชื่อ | Severity | Key Action |
|:---:|:---|:---:|:---|
| **01** | Phishing / ฟิชชิ่ง | P2–P1 | Isolate mailbox → Block sender → Check click logs |
| **17** | BEC / อีเมลหลอกธุรกิจ | P1 | Freeze financial transactions → Verify sender identity |
| **42** | Email Account Takeover | P1 | Reset creds → Revoke OAuth → Audit inbox rules |
| **48** | Deepfake Social Engineering | P1 | Verify via callback → Freeze actions → Preserve media |

## 🦠 Malware & Ransomware

| PB | Name / ชื่อ | Severity | Key Action |
|:---:|:---|:---:|:---|
| **02** | Ransomware / แรนซัมแวร์ | P1 | Isolate → Do NOT pay → Check backups → Preserve evidence |
| **03** | Malware Infection / มัลแวร์ | P2–P1 | Isolate endpoint → Collect artifacts → EDR scan |
| **10** | Exploit / ช่องโหว่ | P2–P1 | Patch → Block IP → Check lateral movement |
| **11** | Suspicious Script | P2 | Kill process → Capture script → Check parent process |
| **38** | Wiper Attack | P1 | Isolate immediately → Check integrity → Activate DR |
| **39** | Living Off The Land | P2 | Audit LOLBin usage → Check scheduled tasks → Monitor |
| **46** | Rootkit / Bootkit | P1 | Offline scan → Rebuild if confirmed → Check firmware |

## 🔑 Identity & Access

| PB | Name / ชื่อ | Severity | Key Action |
|:---:|:---|:---:|:---|
| **04** | Brute Force / เดารหัส | P3–P2 | Lock account → Check source IP → Enable MFA |
| **05** | Account Compromise | P2–P1 | Reset password → Revoke sessions → Check actions |
| **06** | Impossible Travel | P3–P2 | Verify with user → Check VPN → Review access logs |
| **07** | Privilege Escalation | P1 | Revoke elevated perms → Audit group changes |
| **14** | Insider Threat / ภัยจากภายใน | P1 | Preserve evidence → Legal/HR → Monitor covertly |
| **15** | Rogue Admin | P1 | Disable account → Rotate secrets → Full audit |
| **26** | MFA Bypass / Token Theft | P1 | Revoke tokens → Force re-enrollment → Check phish kit |
| **36** | Credential Dumping | P1 | Reset all exposed creds → Check LSASS/SAM/DCSync |

## 🌐 Network & Web

| PB | Name / ชื่อ | Severity | Key Action |
|:---:|:---|:---:|:---|
| **09** | DDoS Attack | P2–P1 | Activate WAF/CDN → Rate limit → ISP mitigation |
| **12** | Lateral Movement | P1 | Segment network → Disable compromised accounts |
| **13** | C2 Communication | P1 | Block C2 domains/IPs → Isolate beaconing hosts |
| **18** | Web Attack | P2 | WAF block → Review logs → Patch vulnerability |
| **22** | API Abuse | P2 | Rate limit → Rotate API keys → Review access patterns |
| **24** | DNS Tunneling | P1 | Block DNS → Isolate host → Analyze payload |
| **25** | Zero-Day Exploit | P1 | Virtual patch → Isolate → Monitor for exploitation |
| **34** | Network Discovery | P3 | Identify scanner → Block if unauthorized → Review ACLs |
| **37** | SQL Injection | P1 | WAF block → Patch code → Check data exposure |
| **44** | Watering Hole | P1 | Block site → Scan visitors → Check exploit payload |
| **43** | Drive-By Download | P2 | Block URL → Scan affected endpoints → Patch browser |
| **50** | Unauthorized Scanning | P3 | Identify source → Block → Report if external |

## ☁️ Cloud & Infrastructure

| PB | Name / ชื่อ | Severity | Key Action |
|:---:|:---|:---:|:---|
| **16** | Cloud IAM Anomaly | P2 | Review permissions → Revoke excess → Audit API calls |
| **23** | Cryptomining | P2 | Terminate instances → Rotate keys → Check billing |
| **28** | Cloud Storage Exposure | P2–P1 | Make private → Check access logs → Notify if data leaked |
| **30** | Shadow IT | P3 | Inventory → Risk assess → Block or onboard |
| **19** | AWS EC2 Compromise | P1 | Isolate instance → Snapshot EBS → Rotate keys |
| **20** | AWS S3 Compromise | P1 | Block public access → Check CloudTrail → Rotate creds |
| **33** | Azure AD Compromise | P1 | Revoke sessions → Reset creds → Check Conditional Access |
| **41** | VPN Abuse | P2 | Disable VPN account → Check source → Review tunnel logs |
| **45** | Cloud Cryptojacking | P2 | Kill compute → Revoke API keys → Alert billing |

## 📦 Data & Supply Chain

| PB | Name / ชื่อ | Severity | Key Action |
|:---:|:---|:---:|:---|
| **08** | Data Exfiltration / ข้อมูลรั่ว | P1 | Block channel → Assess scope → PDPA notification |
| **27** | Log Clearing / ลบ Log | P1 | Restore from backup → Preserve remaining → Investigate |
| **21** | Supply Chain Attack | P1 | Isolate affected software → Check signatures → Vendor contact |
| **35** | Data Collection / Staging | P2 | Monitor staging area → Block exfil channels |
| **49** | Typosquatting | P3 | Report domain → Block in DNS → Alert users |

## 📱 Physical & Mobile

| PB | Name / ชื่อ | Severity | Key Action |
|:---:|:---|:---:|:---|
| **32** | Lost/Stolen Device / อุปกรณ์หาย | P2 | Remote wipe → Disable accounts → Report |
| **29** | Mobile Compromise | P2 | Factory reset → Re-enroll MDM → Change passwords |
| **31** | OT/ICS Incident | P1 | Isolate OT segment → Manual override → Vendor contact |
| **40** | USB Removable Media | P3–P2 | Scan device → Check autorun → DLP review |
| **47** | SIM Swap | P1 | Contact carrier → Reset accounts → Enable app-based MFA |

---

## ⚡ Escalation Quick Guide

| Severity | Response Time | Notify | Example |
|:---:|:---:|:---|:---|
| **P1 — Critical** | 15 min | SOC Manager + CISO + Legal | Ransomware, Active breach, Data leak |
| **P2 — High** | 30 min | SOC Manager + Team Lead | Malware, Account compromise |
| **P3 — Medium** | 2 hours | Tier 2 Analyst | Brute force, Scanning, Policy violation |
| **P4 — Low** | 8 hours | Tier 1 Analyst | False positive, Info request |

## 📞 Key Contacts (Fill In)

| Role | Name | Phone | Email |
|:---|:---|:---|:---|
| SOC Manager | __________ | __________ | __________ |
| CISO | __________ | __________ | __________ |
| Legal Counsel | __________ | __________ | __________ |
| PR/Comms | __________ | __________ | __________ |
| IT Infra Lead | __________ | __________ | __________ |
| Cloud Admin | __________ | __________ | __________ |
| HR Contact | __________ | __________ | __________ |

---

> 📖 **Full Documentation**: [SOC SOP Repository](https://nutthakorn7.github.io/SOC-SOP/)
>
> 🔄 **Last Updated**: 2026-02-17 | **Version**: 2.10
