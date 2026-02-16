# Playbook: การตอบสนอง Rootkit / Bootkit

**ID**: PB-45
**ความรุนแรง**: วิกฤต | **ประเภท**: Defense Evasion / Persistence
**MITRE ATT&CK**: [T1014](https://attack.mitre.org/techniques/T1014/) (Rootkit), [T1542](https://attack.mitre.org/techniques/T1542/) (Pre-OS Boot), [T1542.003](https://attack.mitre.org/techniques/T1542/003/) (Bootkit)
**Trigger**: EDR alert (kernel-level hooking), AV (rootkit detection), ระบบไม่เสถียรพร้อม hidden processes, UEFI integrity check failure

> ⚠️ **วิกฤต**: Rootkits ทำงานต่ำกว่า OS — เครื่องมือมาตรฐานตรวจไม่พบ Bootkits อยู่รอดการ reinstall OS ต้องใช้เครื่องมือเฉพาะทางและอาจต้อง reimage hardware

### Rootkit / Bootkit Taxonomy

```mermaid
graph TD
    Root["💀 Rootkit / Bootkit"] --> User["User-mode Rootkit\nAPI hooking, DLL injection"]
    Root --> Kernel["Kernel-mode Rootkit\nDriver-level hiding"]
    Root --> UEFI["UEFI/Bootkit\nPre-OS persistence"]
    Root --> HW["Hardware/Firmware\nHDD/SSD firmware"]
    
    User --> UEx["ซ่อน processes\nซ่อน files\nซ่อน connections"]
    Kernel --> KEx["Kernel callbacks\nFilter drivers\nDKOM"]
    UEFI --> BEx["แก้ไข MBR/VBR\nUEFI implant\nBypass Secure Boot"]
    HW --> HEx["แก้ไข SSD firmware\nNIC firmware\nBMC/IPMI implant"]
    
    style Root fill:#660000,color:#fff
    style Kernel fill:#cc0000,color:#fff
    style UEFI fill:#cc0000,color:#fff
    style HW fill:#660000,color:#fff
```

### กลุ่ม Rootkit ที่รู้จัก

```mermaid
graph TD
    subgraph "UEFI/Bootkits"
        B1["BlackLotus\nBypass Secure Boot"]
        B2["CosmicStrand\nUEFI firmware rootkit"]
        B3["MosaicRegressor\nUEFI implant"]
        B4["ESPecter\nEFI partition"]
    end
    subgraph "Kernel Rootkits"
        K1["Necurs\nKernel driver"]
        K2["ZeroAccess\nKernel hooks"]
        K3["TDL4/TDSS\nMBR infection"]
        K4["FiveSys\nSigned driver"]
    end
    style B1 fill:#660000,color:#fff
    style B2 fill:#660000,color:#fff
    style K1 fill:#cc0000,color:#fff
```

---

## Decision Flow

```mermaid
graph TD
    Alert["🚨 สงสัย Rootkit/Bootkit"] --> Source{"วิธีตรวจจับ?"}
    Source -->|"EDR"| EDR["Kernel hooking ตรวจพบ\nDriver ผิดปกติ"]
    Source -->|"AV/UEFI scan"| AV["Rootkit signature match\nหรือ integrity failure"]
    Source -->|"Anomaly"| Anomaly["Hidden processes\nDisk space หายไป\nNetwork traffic ผิดปกติ"]
    EDR --> Confirm["รัน offline rootkit scanner"]
    AV --> Confirm
    Anomaly --> Confirm
    Confirm --> Found{"ยืนยัน rootkit?"}
    Found -->|"User-mode"| UserR["🟠 ปานกลาง\nลบได้ด้วย AV"]
    Found -->|"Kernel-mode"| KernelR["🔴 วิกฤต\nต้อง reimage"]
    Found -->|"UEFI/Bootkit"| UEFIR["💀 หายนะ\nต้อง reflash firmware"]
    Found -->|"ไม่พบ"| FP["ตรวจติดตามต่อ\nนัด deep scan"]
    KernelR --> Isolate["แยก — เก็บสำหรับ forensics"]
    UEFIR --> Isolate
    style Alert fill:#660000,color:#fff
    style UEFIR fill:#660000,color:#fff
    style KernelR fill:#cc0000,color:#fff
```

### ชั้น Visibility

```mermaid
graph TD
    subgraph "ชั้น Visibility"
        L1["Application Layer\n✅ AV มาตรฐานเห็นได้"]
        L2["User-mode API\n⚠️ API hooks ซ่อนได้"]
        L3["Kernel / Drivers\n🔴 Kernel rootkits ซ่อนที่นี่"]
        L4["Boot Process\n💀 Bootkits โหลดก่อน OS"]
        L5["Firmware/UEFI\n💀 แทบมองไม่เห็น"]
    end
    L1 --> L2 --> L3 --> L4 --> L5
    style L1 fill:#00aa00,color:#fff
    style L2 fill:#ffcc00,color:#000
    style L3 fill:#ff4444,color:#fff
    style L4 fill:#cc0000,color:#fff
    style L5 fill:#660000,color:#fff
```

### ขั้นตอนการสืบสวน

```mermaid
sequenceDiagram
    participant EDR
    participant SOC as SOC Analyst
    participant IR as IR Team
    participant Forensics
    participant IT as IT Ops

    EDR->>SOC: 🚨 Kernel-level anomaly ตรวจพบ
    SOC->>SOC: ยืนยันด้วย offline scan tool
    SOC->>IR: Escalate — สงสัย rootkit
    IR->>Forensics: Boot จาก clean USB, scan offline
    Forensics->>IR: ยืนยันประเภท rootkit & กลุ่ม
    IR->>IT: แยก — อย่า reboot (อาจทำลายหลักฐาน)
    IR->>Forensics: Memory dump + disk image
    Forensics->>IR: รายงานวิเคราะห์เต็ม
    IR->>IT: Reimage (kernel) หรือ reflash (UEFI)
```

### ความลึกของ Persistence

```mermaid
graph TD
    Persist["ความลึก Persistence"] --> AppP["Application\nรอดการ reboot"]
    Persist --> ServiceP["Service/Driver\nรอดการ reboot"]
    Persist --> BootP["Boot Sector\nรอดการ reinstall OS"]
    Persist --> FirmP["Firmware/UEFI\nรอดการเปลี่ยน disk"]
    AppP --> Reset1["🟢 วิธีแก้: ลบ app/service"]
    ServiceP --> Reset2["🟡 วิธีแก้: Reimage OS"]
    BootP --> Reset3["🔴 วิธีแก้: Wipe disk + reimage"]
    FirmP --> Reset4["💀 วิธีแก้: Reflash firmware\nหรือเปลี่ยน hardware"]
    style FirmP fill:#660000,color:#fff
    style Reset4 fill:#660000,color:#fff
```

### Timeline การตอบสนอง

```mermaid
gantt
    title Rootkit/Bootkit Response Timeline
    dateFormat HH:mm
    axisFormat %H:%M
    section Detection
        EDR/AV alert           :a1, 00:00, 10min
        ยืนยัน offline scan    :a2, after a1, 30min
    section Containment
        Network isolation      :a3, after a2, 5min
        Memory acquisition     :a4, after a3, 60min
    section Investigation
        จำแนก rootkit          :a5, after a4, 120min
        วิเคราะห์ persistence  :a6, after a5, 120min
    section Recovery
        Reimage/Reflash        :a7, after a6, 180min
        ยืนยันสถานะสะอาด       :a8, after a7, 60min
```

---

## 1. การดำเนินการทันที (30 นาทีแรก)

| # | การดำเนินการ | ผู้รับผิดชอบ |
|:---|:---|:---|
| 1 | **อย่า REBOOT** — rootkit อาจเปลี่ยนพฤติกรรมเมื่อ reboot | SOC T1 |
| 2 | แยกเครือข่าย endpoint (EDR หรือทางกายภาพ) | SOC T1 |
| 3 | เก็บ memory dump ก่อนทำ remediation ใดๆ | IR Team |
| 4 | เก็บ disk image สำหรับ forensic analysis | IR Team |
| 5 | รัน offline rootkit scanner จาก clean USB | IR Team |
| 6 | ตรวจ UEFI/Secure Boot integrity | IT Ops |

## 2. รายการตรวจสอบ

### เครื่องมือตรวจจับ Rootkit
- [ ] รัน GMER หรือ TDSSKiller (offline)
- [ ] ตรวจ kernel drivers ที่โหลด: `driverquery /v`
- [ ] เปรียบเทียบ processes (task manager vs API-level tools)
- [ ] ตรวจไฟล์ hidden ด้วย forensic tools (FTK Imager)
- [ ] ตรวจ MBR/VBR integrity (เปรียบเทียบกับ hash ที่รู้จัก)
- [ ] ตรวจ UEFI firmware hash กับ baseline ของผู้ผลิต

### ตัวบ่งชี้พฤติกรรม
- [ ] Processes เห็นใน memory dump แต่ไม่เห็นใน Task Manager
- [ ] Network connections ไม่แสดงใน `netstat`
- [ ] การใช้ disk space ไม่ตรงกับไฟล์ที่เห็น
- [ ] AV/EDR agent crash หรืออัปเดตไม่ได้
- [ ] นาฬิการะบบผิดปกติ
- [ ] Blue screens ด้วย stop codes ผิดปกติ

### วิเคราะห์ Persistence
- [ ] Kernel drivers โหลดจาก paths ผิดปกติ
- [ ] Services ที่ไม่มี binary ที่สอดคล้อง
- [ ] MBR/VBR แก้ไขจากสถานะที่รู้จัก
- [ ] UEFI variables หรือ EFI partition แก้ไข
- [ ] สถานะ Secure Boot (เปิด/ปิด/bypass)

## 3. การควบคุม (Containment)

| ขอบเขต | การดำเนินการ |
|:---|:---|
| **เครือข่าย** | แยกเต็มรูปแบบ — ไม่มีการเชื่อมต่อ |
| **Endpoint** | อย่า reboot, รักษาสถานะ |
| **หลักฐาน** | Memory dump + full disk image |
| **การแพร่กระจาย** | ตรวจ hardware model เดียวกันสำหรับการติดเชื้อเดียวกัน |

## 4. การกำจัดและกู้คืน

### ตามประเภท Rootkit
| ประเภท | วิธีกู้คืน |
|:---|:---|
| User-mode | AV removal → ยืนยัน → ตรวจติดตาม |
| Kernel-mode | Full disk wipe + OS reimage |
| Bootkit (MBR) | Wipe disk + reimage + ตรวจ MBR |
| UEFI rootkit | Reflash firmware จากผู้ผลิต + reimage |
| Firmware rootkit | เปลี่ยน hardware ถ้า reflash ไม่ได้ |

### ยืนยันการกู้คืน
1. Boot จาก media ที่สะอาดที่รู้ว่าสะอาด
2. รัน offline rootkit scan บนระบบที่ reimage
3. ยืนยันการตั้งค่า UEFI/Secure Boot
4. ตรวจติดตามสัญญาณการติดเชื้อซ้ำ (7 วัน)
5. Deploy kernel protection เพิ่มเติม (HVCI, VBS)

## 5. หลังเหตุการณ์ (Post-Incident)

| คำถาม | คำตอบ |
|:---|:---|
| Rootkit ถูกส่งมาอย่างไร? | [เวกเตอร์] |
| Secure Boot เปิดอยู่หรือไม่? | [ใช่/ไม่] |
| Driver signing บังคับใช้หรือไม่? | [ใช่/ไม่] |
| Rootkit ทำงานอยู่นานเท่าไหร่? | [ระยะเวลา] |
| มีระบบอื่นได้รับผลกระทบหรือไม่? | [จำนวน] |

## 6. Detection Rules (Sigma)

```yaml
title: Suspicious Kernel Driver Loaded
logsource:
    product: windows
    service: system
detection:
    selection:
        EventID: 7045
        ServiceType: 'kernel mode driver'
    filter:
        ImagePath|startswith:
            - 'C:\Windows\System32\drivers\'
    condition: selection and not filter
    level: critical
```

```yaml
title: Unsigned Driver Load Attempt
logsource:
    product: windows
    category: driver_load
detection:
    selection:
        Signed: 'false'
    condition: selection
    level: high
```

## เอกสารที่เกี่ยวข้อง
- [Malware Infection Playbook](Malware_Infection.th.md)
- [Credential Dumping Playbook](Credential_Dumping.th.md)
- [Wiper Attack Playbook](Wiper_Attack.th.md)
- [คู่มือ Tier 3](../Runbooks/Tier3_Runbook.th.md)

## References
- [MITRE T1014 — Rootkit](https://attack.mitre.org/techniques/T1014/)
- [MITRE T1542 — Pre-OS Boot](https://attack.mitre.org/techniques/T1542/)
- [ESET — UEFI Threats](https://www.welivesecurity.com/)
