# Playbook: การโจมตีเว็บแอปพลิเคชัน (Web Attack)

**ID**: PB-10
**ระดับความรุนแรง**: สูง | **หมวดหมู่**: ความปลอดภัยแอปพลิเคชัน
**MITRE ATT&CK**: [T1190](https://attack.mitre.org/techniques/T1190/) (Exploit Public-Facing Application)
**ทริกเกอร์**: WAF alert, IDS/IPS, รายงาน Bug Bounty, Defacement

---

## 1. การวิเคราะห์

### 1.1 ประเภทการโจมตีเว็บ

| ประเภท | OWASP | ตัวบ่งชี้ |
|:---|:---|:---|
| **SQL Injection** | A03 | `'`, `UNION SELECT`, `1=1` | 
| **XSS** | A03 | `<script>`, Event handlers |
| **Path Traversal** | A01 | `../`, `%2e%2e` |
| **Remote File Inclusion** | A08 | External URL params |
| **Web Shell** | A03 | New PHP/ASPX files |
| **SSRF** | A10 | Internal IP ใน URL params |
| **Command Injection** | A03 | `; | && ` charactersBin |
| **Brute Force (Auth)** | A07 | Login failures สูง |

### 1.2 รายการตรวจสอบ

| รายการ | วิธีตรวจสอบ | เสร็จ |
|:---|:---|:---:|
| ประเภทการโจมตี | WAF logs | ☐ |
| โจมตีสำเร็จหรือแค่ attempt? | Response code (200 vs 403/500) | ☐ |
| Source IP | WAF / Web logs | ☐ |
| Endpoint ที่ถูกโจมตี | URL path analysis | ☐ |
| มี web shell ถูกวาง? | FIM / file scan | ☐ |
| มีข้อมูลรั่วไหล? | Response body size | ☐ |

---

## 2. การควบคุม

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **Block** source IP ที่ WAF/Firewall | ☐ |
| 2 | **Virtual patch** — เพิ่ม WAF rule สำหรับ attack pattern | ☐ |
| 3 | **ลบ web shell** หากพบ | ☐ |
| 4 | **Take offline** หากข้อมูลรั่วไหลอยู่ | ☐ |

---

## 3. การกำจัด

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **Patch** แอปพลิเคชันที่มีช่องโหว่ | ☐ |
| 2 | ลบ backdoor / web shell ทั้งหมด | ☐ |
| 3 | ตรวจ database สำหรับ injected data | ☐ |
| 4 | รีเซ็ต application credentials | ☐ |

---

## 4. การฟื้นฟู

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | ปรับ WAF rules ถาวร | ☐ |
| 2 | เพิ่ม input validation / parameterized queries | ☐ |
| 3 | สั่ง penetration test | ☐ |
| 4 | เปิด SAST/DAST ใน CI/CD | ☐ |

---

## 5. เกณฑ์การยกระดับ

| เงื่อนไข | ยกระดับไปยัง |
|:---|:---|
| SQL Injection สำเร็จ — ข้อมูลรั่ว | Legal + DPO (PDPA 72 ชม.) |
| Web shell ถูกวาง | Tier 2 + [PB-13 C2](C2_Communication.th.md) |
| Defacement | PR + Management |
| SSRF เข้าถึงระบบภายใน | Major Incident |

---

## เอกสารที่เกี่ยวข้อง

- [กรอบการตอบสนองต่อเหตุการณ์](../Framework.th.md)
- [PB-18 Exploit](Exploit.th.md)

## อ้างอิง

- [OWASP Top 10](https://owasp.org/Top10/)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
