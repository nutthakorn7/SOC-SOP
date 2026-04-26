# ลำดับความสำคัญ Detection Use Case — ตรวจจับอะไรก่อน

> **รหัสเอกสาร:** UC-001  
> **เวอร์ชัน:** 1.0  
> **อัปเดตล่าสุด:** 2026-02-15  
> **เงื่อนไข:** ติดตั้ง SIEM แล้ว, มี log source ≥3

---

## ปัญหา

มี detection rules นับพัน deploy ทีเดียวไม่ได้ คู่มือนี้บอกว่า **ตรวจจับอะไรก่อน** ตามข้อมูลภัยจริง

---

## MITRE ATT&CK Top 10 (เทคนิคที่พบบ่อยสุด)

| ลำดับ | เทคนิค | คืออะไร | ความถี่ |
|:---:|:---|:---|:---:|
| 1 | Phishing (T1566) | Email อันตราย | 🔴🔴🔴 |
| 2 | Valid Accounts (T1078) | Credential ถูกขโมย | 🔴🔴🔴 |
| 3 | PowerShell/Script (T1059) | ใช้ script โจมตี | 🔴🔴 |
| 4 | Brute Force (T1110) | เดารหัสผ่าน | 🔴🔴 |
| 5 | Ransomware (T1486) | เข้ารหัสไฟล์เรียกค่าไถ่ | 🔴🔴 |

---

## เฟส 1: พื้นฐาน (เดือน 1–3) — 10 Rules แรก

| # | Use Case | Playbook | ความสำคัญ |
|:---:|:---|:---|:---:|
| 1 | Failed login > 10 ครั้ง/5 นาที | PB-04 | 🔴 |
| 2 | Login จากสถานที่เป็นไปไม่ได้ | PB-06 | 🔴 |
| 3 | Office เปิด PowerShell | PB-01 | 🔴 |
| 4 | Malware execute สำเร็จ | PB-03 | 🔴 |
| 5 | ไฟล์ถูกเปลี่ยนชื่อจำนวนมาก (ransomware) | PB-02 | 🔴 |
| 6 | สร้าง admin account ใหม่ | PB-07 | 🟡 |
| 7 | ลบ Security log | PB-20 | 🟡 |
| 8 | Login นอกเวลาทำงาน | PB-05 | 🟡 |
| 9 | สร้าง email forwarding rule | PB-17 | 🟡 |
| 10 | เชื่อมต่อ IP อันตราย | PB-13 | 🟡 |

---

## เฟส 2: ขยาย (เดือน 4–6) — เพิ่ม 10 Rules

| # | Use Case | Playbook |
|:---:|:---|:---|
| 11 | Lateral movement (admin share) | PB-12 |
| 12 | ติดตั้ง service ใหม่ (persistence) | PB-11 |
| 13 | Encoded PowerShell | PB-11 |
| 14 | DNS ไปโดเมนน่าสงสัย | PB-24 |
| 15 | Upload ข้อมูลขนาดใหญ่ | PB-08 |
| 16 | Cloud privilege escalation | PB-16 |
| 17–20 | Scheduled task, process injection, USB, MFA fail | PB-11–26 |

---

## เฟส 3: ขั้นสูง (เดือน 7–12) — เพิ่ม 10 Rules

| # | Use Case | Playbook |
|:---:|:---|:---|
| 21 | Beaconing (C2 callback) | PB-13 |
| 22 | DNS tunneling | PB-24 |
| 23 | Cloud storage เป็น public | PB-27 |
| 24 | Shadow IT | PB-29 |
| 25–30 | Kerberoasting, DCSync, AiTM, DLL sideload, WMI, OT/ICS | PB-15–30 |

---

## เฟส 4: Threat Hunting (ปีที่ 2+)

| สมมติฐาน | ความถี่ |
|:---|:---:|
| มี service account ถูกยึดไหม? | รายเดือน |
| มีใคร beacon ไป C2? | รายสัปดาห์ |
| ข้อมูลสำคัญรั่วไหลไหม? | รายสัปดาห์ |
| มี web shell ซ่อนอยู่ไหม? | รายเดือน |

---

## สูตรให้คะแนนลำดับ

```
คะแนน = (ความเป็นไปได้ × 3) + (ผลกระทบ × 3) + (ข้อมูลพร้อม × 2) + (ความง่าย × 2)

ช่วง: 10–50 → เริ่มจากคะแนนสูงสุด
```

---

## ตาราง Coverage

| Tactic | เฟส 1 | เฟส 2 | เฟส 3 | เฟส 4 |
|:---|:---:|:---:|:---:|:---:|
| Initial Access | ✅ | ✅ | ✅ | ✅ |
| Execution | ✅ | ✅ | ✅ | ✅ |
| Persistence | ⚠️ | ✅ | ✅ | ✅ |
| Lateral Movement | ❌ | ✅ | ✅ | ✅ |
| Exfiltration | ❌ | ⚠️ | ✅ | ✅ |
| Impact | ✅ | ✅ | ✅ | ✅ |

---

## Prioritization Matrix

### Risk-Based Scoring

| ปัจจัย | น้ำหนัก | 1 (ต่ำ) | 2 (กลาง) | 3 (สูง) |
|:---|:---:|:---|:---|:---|
| **Threat Likelihood** | 30% | ไม่ค่อยพบ | พบบ้าง | พบบ่อย |
| **Business Impact** | 30% | ผลกระทบต่ำ | กระทบบริการ | กระทบรายได้/ชื่อเสียง |
| **Data Availability** | 20% | ไม่มี log | มีบาง log | มีครบ |
| **Detection Feasibility** | 20% | ยากมาก | ทำได้แต่ซับซ้อน | ทำได้ง่าย |

### คำนวณ Priority Score

```
Score = (Likelihood × 0.3) + (Impact × 0.3) + (Data × 0.2) + (Feasibility × 0.2)

Priority:
  2.5–3.0 = P1 (ดำเนินการภายใน 1 สัปดาห์)
  2.0–2.4 = P2 (ภายใน 1 เดือน)
  1.5–1.9 = P3 (ภายใน 1 ไตรมาส)
  1.0–1.4 = P4 (Backlog)
```

## Use Case Development Template

| ฟิลด์ | คำอธิบาย |
|:---|:---|
| **UC ID** | UC-YYYY-NNN |
| **ชื่อ** | [ชื่อ Use Case] |
| **MITRE Technique** | [TID — ชื่อ] |
| **Log Sources ที่ต้องใช้** | [ระบุ] |
| **Detection Logic** | [Sigma rule / query] |
| **False Positive Cases** | [ระบุ FP ที่คาดว่าจะเกิด] |
| **Response Playbook** | [ลิงก์ไปยัง playbook] |
| **Priority** | [P1/P2/P3/P4] |

## Coverage Dashboard

| MITRE Tactic | Techniques ทั้งหมด | ครอบคลุม | Gap |
|:---|:---:|:---:|:---:|
| Initial Access | 9 | [X] | [X] |
| Execution | 12 | [X] | [X] |
| Persistence | 19 | [X] | [X] |
| Privilege Escalation | 13 | [X] | [X] |
| Defense Evasion | 42 | [X] | [X] |
| Credential Access | 17 | [X] | [X] |
| Lateral Movement | 9 | [X] | [X] |
| Exfiltration | 9 | [X] | [X] |
| Impact | 13 | [X] | [X] |

## Use Case Scoring Model

### Risk-based Prioritization

| Factor | Weight | Score (1-5) | คำอธิบาย |
|:---|:---|:---|:---|
| Business Impact | 30% | 1-5 | ผลกระทบต่อธุรกิจ |
| Threat Likelihood | 25% | 1-5 | โอกาสเกิดภัย |
| Detection Capability | 20% | 1-5 | ความสามารถตรวจจับ |
| Data Availability | 15% | 1-5 | มี log source หรือไม่ |
| Effort to Implement | 10% | 1-5 | ความยากในการสร้าง |

### Use Case Lifecycle

```mermaid
flowchart LR
    A[เสนอ] --> B[ประเมิน]
    B --> C[พัฒนา]
    C --> D[ทดสอบ]
    D --> E[นำขึ้นใช้งาน]
    E --> F[ติดตามผล]
    F --> G[ปรับแต่ง]
    G --> F
```

### Use Case Quick-Start Templates

| Use Case | Log Source | Rule Logic | Priority |
|:---|:---|:---|:---|
| Brute Force | AD/LDAP | > 10 failed/5min | High |
| Privilege Escalation | Windows Event | 4672 + 4688 | Critical |
| Data Exfiltration | Proxy/DLP | Upload > threshold | High |
| Suspicious DNS | DNS logs | Entropy > 3.5 | Medium |
| Malware Detection | EDR | Known hash/behavior | Critical |

### Use Case Retirement Criteria
- False positive rate > 60% หลัง tuning
- Log source ถูกยกเลิกใช้งาน
- ซ้ำซ้อนกับ rule อื่น
- ไม่เคย trigger ใน 6 เดือน

### Quick Wins Identification

| Criteria | Description |
|:---|:---|
| High impact + Low effort | นำขึ้นใช้งานก่อน |
| Existing log source | No new onboarding |
| Known TTP coverage | MITRE mapped |
| Template available | Pre-built rule |

## เอกสารที่เกี่ยวข้อง

- [แผนงานสร้าง SOC](SOC_Building_Roadmap.th.md)
- [ดัชนี Detection Rules](../08_Detection_Engineering/README.th.md)
- [แผนที่ MITRE ATT&CK](../tools/mitre_attack_heatmap.html)
