# Playbook: Impossible Travel

**ID**: PB-06
**ระดับความรุนแรง**: ปานกลาง/สูง | **หมวดหมู่**: Identity & Access
**MITRE ATT&CK**: [T1078](https://attack.mitre.org/techniques/T1078/) (Valid Accounts)
**ทริกเกอร์**: SIEM/IdP alert (Login จากสองสถานที่ห่างไกลในเวลาสั้น)

## 1. การวิเคราะห์

### 1.1 สาเหตุ False Positive

| สาเหตุ | วิธีตรวจสอบ | เสร็จ |
|:---|:---|:---:|
| VPN องค์กร (exit node ต่างที่) | VPN logs | ☐ |
| Cloud proxy / CDN | Proxy logs | ☐ |
| ผู้ใช้เดินทางจริง (สนามบิน→ต่างประเทศ) | สอบถามผู้ใช้ | ☐ |
| Mobile network handoff | ISP analysis | ☐ |
| Shared account | IAM audit | ☐ |

### 1.2 รายการตรวจสอบ (หากไม่ใช่ FP)

| รายการ | วิธีตรวจสอบ | เสร็จ |
|:---|:---|:---:|
| IP ทั้งสองอยู่ที่ไหน? | GeoIP | ☐ |
| เป็นไปได้ทางกายภาพ? |(ระยะทาง / เวลา) | คำนวณ | ☐ |
| กิจกรรมหลัง login ที่ location ใหม่ | SIEM / Cloud audit | ☐ |
| ดาวน์โหลดข้อมูล? | File audit | ☐ |
| สร้าง inbox rules? | Exchange audit | ☐ |
| เปลี่ยน MFA? | IdP audit | ☐ |

## 2. การควบคุม

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **ยกเลิก session** ที่ location ผิดปกติ | ☐ |
| 2 | **รีเซ็ตรหัสผ่าน** | ☐ |
| 3 | **ติดต่อผู้ใช้** ยืนยันตัวตน | ☐ |
| 4 | หากยืนยันไม่ได้ → **ล็อกบัญชี** | ☐ |

## 3. การฟื้นฟู

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | ตั้งค่า Named Locations (trusted IPs) ใน IdP | ☐ |
| 2 | บังคับ Conditional Access ตาม location | ☐ |
| 3 | เปิด CAE (Continuous Access Evaluation) | ☐ |

## 4. เกณฑ์การยกระดับ

| เงื่อนไข | ยกระดับไปยัง |
|:---|:---|
| Token theft ยืนยัน | [PB-26 MFA Bypass](MFA_Bypass.th.md) |
| ข้อมูลถูก access | [PB-08 Data Exfil](Data_Exfiltration.th.md) |
| Admin account | CISO |

## เอกสารที่เกี่ยวข้อง
- [กรอบ IR](../Framework.th.md)
- [PB-05 บัญชีถูกบุกรุก](Account_Compromise.th.md)

## อ้างอิง
- [MITRE ATT&CK T1078 — Valid Accounts](https://attack.mitre.org/techniques/T1078/)
