# Playbook: การนำข้อมูลออก (Data Exfiltration)

**ID**: PB-08
**ระดับความรุนแรง**: สูง/วิกฤต | **หมวดหมู่**: ความปลอดภัยข้อมูล
**MITRE ATT&CK**: [T1041](https://attack.mitre.org/techniques/T1041/) (Exfiltration Over C2 Channel), [T1048](https://attack.mitre.org/techniques/T1048/) (Exfiltration Over Alternative Protocol)
**ทริกเกอร์**: DLP alert, Netflow anomaly, UEBA, proxy alert

---

## 1. การวิเคราะห์

### 1.1 ช่องทางนำข้อมูลออก

| ช่องทาง | ตัวบ่งชี้ | การตรวจจับ |
|:---|:---|:---|
| **HTTPS upload** (cloud storage) | ปริมาณ upload สูง | DLP / Proxy |
| **อีเมล** (แนบไฟล์) | ไฟล์ขนาดใหญ่ / ปริมาณมาก | DLP / Mail gateway |
| **USB / Removable** | Copy ไฟล์ไป USB | EDR / DLP endpoint |
| **DNS tunneling** | Payload ใน DNS queries | DNS analytics |
| **FTP / SCP / SFTP** | Outbound file transfer | Netflow |
| **พิมพ์ / ถ่ายรูป** | Physical exfiltration | DLP / กล้อง |

### 1.2 รายการตรวจสอบ

| รายการ | วิธีตรวจสอบ | เสร็จ |
|:---|:---|:---:|
| ข้อมูลอะไรถูกนำออก? จำแนกประเภท | DLP | ☐ |
| ปริมาณเท่าไหร่? | Proxy / Netflow | ☐ |
| ช่องทางอะไร? | DLP / EDR / SIEM | ☐ |
| ใคร / process ใด? | UEBA / EDR | ☐ |
| ปลายทาง (destination) | Proxy / DNS / Netflow | ☐ |
| เจตนาร้ายหรือไม่ตั้งใจ? | Context analysis | ☐ |

---

## 2. การควบคุม

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **บล็อก** destination IP/domain | ☐ |
| 2 | **Isolate** host ต้นทาง | ☐ |
| 3 | **ล็อกบัญชี** ผู้ใช้ | ☐ |
| 4 | **บล็อก** USB ports (หาก USB exfil) | ☐ |
| 5 | **เพิ่ม DLP monitoring** | ☐ |

---

## 3. การกำจัด

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | ลบ malware/tools ที่ใช้ exfiltrate | ☐ |
| 2 | ลบ persistence | ☐ |
| 3 | หมุนเวียน credentials ที่เกี่ยวข้อง | ☐ |

---

## 4. การฟื้นฟู

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | เพิ่ม DLP rules สำหรับข้อมูลสำคัญ | ☐ |
| 2 | จำกัด USB / removable media | ☐ |
| 3 | เปิด egress filtering | ☐ |
| 4 | จำแนกและติดแท็กข้อมูลสำคัญ | ☐ |

---

## 5. เกณฑ์การยกระดับ

| เงื่อนไข | ยกระดับไปยัง |
|:---|:---|
| PII / ข้อมูลลูกค้ารั่วไหล | Legal + DPO (PDPA 72 ชม.) |
| ทรัพย์สินทางปัญญา | Legal + CISO |
| เจตนาร้าย (insider) | [PB-14 Insider Threat](Insider_Threat.th.md) + HR |
| ปริมาณมาก (>100MB) | SOC Lead |

---

## เอกสารที่เกี่ยวข้อง

- [กรอบการตอบสนองต่อเหตุการณ์](../Framework.th.md)
- [PB-14 ภัยคุกคามจากภายใน](Insider_Threat.th.md)
- [PB-25 DNS Tunneling](DNS_Tunneling.th.md)

## อ้างอิง

- [MITRE ATT&CK — Exfiltration](https://attack.mitre.org/tactics/TA0010/)
