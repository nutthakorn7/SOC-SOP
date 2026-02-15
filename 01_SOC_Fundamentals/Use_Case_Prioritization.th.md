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

## เอกสารที่เกี่ยวข้อง

- [แผนงานสร้าง SOC](SOC_Building_Roadmap.th.md)
- [ดัชนี Detection Rules](../07_Detection_Rules/README.th.md)
- [แผนที่ MITRE ATT&CK](../tools/mitre_attack_heatmap.html)
