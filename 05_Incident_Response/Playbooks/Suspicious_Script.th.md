# Playbook: การรัน Script ที่น่าสงสัย

**ID**: PB-11
**ระดับความรุนแรง**: สูง | **หมวดหมู่**: Endpoint / Execution
**MITRE ATT&CK**: [T1059](https://attack.mitre.org/techniques/T1059/) (Command & Scripting Interpreter)
**ทริกเกอร์**: EDR alert (PowerShell EncodedCommand, WScript), AMSI block

## 1. การวิเคราะห์

### 1.1 Script Engines

| Engine | ตัวบ่งชี้ | ความเสี่ยง |
|:---|:---|:---|
| **PowerShell** | `-EncodedCommand`, `-NoProfile`, AMSI bypass | 🔴 สูง |
| **VBScript/JScript** | wscript.exe, cscript.exe child process | 🟠 สูง |
| **Python** | python.exe unexpected execution | 🟠 สูง |
| **Bash/Shell** | curl \| bash, wget + chmod +x | 🔴 สูง |
| **Office Macro** | WINWORD.EXE → cmd.exe/powershell.exe | 🔴 สูง |

### 1.2 รายการตรวจสอบ

| รายการ | วิธีตรวจสอบ | เสร็จ |
|:---|:---|:---:|
| Script engine ที่ใช้ | EDR process tree | ☐ |
| Command line ที่รัน | EDR / Sysmon Event 1 | ☐ |
| Decoded content (ถ้า encoded) | CyberChef / EDR | ☐ |
| Parent process | EDR | ☐ |
| มีการเชื่อมต่อเครือข่าย? | EDR / Sysmon Event 3 | ☐ |
| มีไฟล์ถูกสร้างหรือแก้ไข? | EDR / Sysmon Event 11 | ☐ |

## 2. การควบคุม

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **Kill** process ที่รัน script | ☐ |
| 2 | **Isolate** host | ☐ |
| 3 | **Block** script hash ที่ EDR | ☐ |
| 4 | **Block** C2 domain/IP (ถ้ามีการเชื่อมต่อ) | ☐ |

## 3. การกำจัด

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | ลบ script + payload ที่ดาวน์โหลดมา | ☐ |
| 2 | ลบ persistence (scheduled task, registry) | ☐ |
| 3 | หมุนเวียน credentials ถ้าถูกเก็บ | ☐ |
| 4 | สแกน AV/EDR เต็มรูปแบบ | ☐ |

## 4. การฟื้นฟู

| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | เปิด Script Block Logging | ☐ |
| 2 | บังคับ Constrained Language Mode | ☐ |
| 3 | ใช้ AppLocker / WDAC | ☐ |

## 5. เกณฑ์การยกระดับ

| เงื่อนไข | ยกระดับไปยัง |
|:---|:---|
| Malware payload ถูกดาวน์โหลด | [PB-03 Malware](Malware_Infection.th.md) |
| C2 callback | [PB-13 C2](C2_Communication.th.md) |
| หลาย host ถูกรัน script เดียวกัน | Major Incident |
| AMSI bypass สำเร็จ | Tier 2 |

## เอกสารที่เกี่ยวข้อง
- [กรอบ IR](../Framework.th.md)
- [PB-03 มัลแวร์](Malware_Infection.th.md)

## อ้างอิง
- [MITRE ATT&CK T1059](https://attack.mitre.org/techniques/T1059/)
