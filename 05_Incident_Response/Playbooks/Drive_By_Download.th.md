# Playbook: การตอบสนอง Drive-By Download

**ID**: PB-44
**ความรุนแรง**: สูง | **ประเภท**: Initial Access / Execution
**MITRE ATT&CK**: [T1189](https://attack.mitre.org/techniques/T1189/) (Drive-by Compromise), [T1204.001](https://attack.mitre.org/techniques/T1204/001/) (Malicious Link)
**Trigger**: EDR (exploit execution หลังเข้าเว็บ), proxy/DNS (redirect ไปยัง domain อันตราย), IDS (exploit kit traffic), user รายงาน (download/popup ผิดปกติ)

> ⚠️ **คำเตือน**: Drive-by downloads ไม่ต้องอาศัยการมีส่วนร่วมของ user — แค่เข้าเว็บที่ถูก compromise ก็เพียงพอ Exploit kits สำรวจ browser และส่ง malware อย่างเงียบๆ

### Drive-By Download Attack Flow

```mermaid
graph LR
    A["1️⃣ ล่อ\nMalvertising / SEO"] --> B["2️⃣ Redirect\nTraffic Distribution"]
    B --> C["3️⃣ Exploit Kit\nLanding Page"]
    C --> D["4️⃣ สำรวจ\nBrowser/OS/Plugins"]
    D --> E["5️⃣ Exploit\nทำงานเงียบๆ"]
    E --> F["6️⃣ Payload\nMalware ติดตั้ง"]
    style A fill:#ffcc00,color:#000
    style C fill:#ff6600,color:#fff
    style E fill:#ff4444,color:#fff
    style F fill:#660000,color:#fff
```

### ระบบนิเวศ Exploit Kit

```mermaid
graph TD
    EK["🔴 Exploit Kits"] --> RIG["RIG EK\nยังทำงานอยู่ 2024"]
    EK --> Magnitude["Magnitude EK\nAsia-Pacific"]
    EK --> Fallout["Fallout EK\nส่ง GandCrab"]
    EK --> Purple["PurpleFox EK\nแพร่กระจายเอง"]
    EK --> Bottle["Bottle EK\nมุ่งเป้า Japan/Korea"]
    
    RIG --> IE["Internet Explorer\nVBScript exploits"]
    RIG --> Flash["Adobe Flash\n(ระบบเก่า)"]
    Magnitude --> Win["Windows\nElevation of privilege"]
    
    style EK fill:#cc0000,color:#fff
    style RIG fill:#ff4444,color:#fff
    style Magnitude fill:#ff4444,color:#fff
```

---

## Decision Flow

```mermaid
graph TD
    Alert["🚨 อาจเป็น Drive-By Download"] --> Source{"แหล่งตรวจจับ?"}
    Source -->|"EDR"| EDR["Post-exploit process\nหลัง browser"]
    Source -->|"Proxy"| Proxy["Redirect ไปยัง EK\nหรือ domain ผิดปกติ"]
    Source -->|"User รายงาน"| User["Download ที่ไม่คาดคิด\nหรือ popup window"]
    Source -->|"IDS"| IDS["Exploit kit traffic\npattern match"]
    EDR --> Isolate["🔴 แยก endpoint\nเก็บ memory"]
    Proxy --> Block["Block domain\nตรวจใครเข้าเว็บ"]
    User --> Scan["สแกน endpoint เต็มรูป\nตรวจ downloads folder"]
    IDS --> Analyze["วิเคราะห์ PCAP\nดึง IOCs"]
    Isolate --> Payload{"Payload ทำงาน?"}
    Payload -->|ใช่| Full["🔴 สันนิษฐาน full compromise"]
    Payload -->|"ไม่ — ถูก block"| Partial["🟡 ความพยายามถูก block\nตรวจ endpoint"]
    Full --> IR["สืบสวน IR"]
    style Alert fill:#ff4444,color:#fff
    style Full fill:#660000,color:#fff
```

### ขั้นตอนการสืบสวน

```mermaid
sequenceDiagram
    participant EDR
    participant SOC as SOC Analyst
    participant Proxy as Proxy/DNS
    participant Sandbox
    participant IR as IR Team

    EDR->>SOC: 🚨 Browser สร้าง process ผิดปกติ
    SOC->>EDR: Process tree เต็ม + network connections
    SOC->>Proxy: ดึง URL chain (redirects)
    Proxy->>SOC: URL1 → URL2 → EK landing → payload
    SOC->>Sandbox: ส่ง payload เข้า sandbox
    Sandbox->>SOC: ระบุกลุ่ม malware
    SOC->>IR: ยืนยัน drive-by — escalate
    IR->>Proxy: Block redirect chain ทั้งหมด
    IR->>EDR: Sweep endpoints หา payload hash เดียวกัน
```

### Traffic Distribution System (TDS)

```mermaid
graph TD
    User["User ท่องเว็บ"] --> Ad["Malvertising\nหรือ เว็บที่ compromise"]
    Ad --> TDS["Traffic Distribution\nSystem (TDS)"]
    TDS --> Check{"Profile เป้าหมาย\nตรงกัน?"}
    Check -->|"ไม่ตรง"| Clean["Redirect ไปยัง\nเนื้อหาปกติ"]
    Check -->|"ตรง: browser/OS\nมีช่องโหว่"| EK["Exploit Kit\nLanding Page"]
    EK --> Exploit["Exploit ทำงาน\nอย่างเงียบๆ"]
    Exploit --> C2["C2 beacon\n+ persistence"]
    style TDS fill:#ff6600,color:#fff
    style EK fill:#cc0000,color:#fff
    style C2 fill:#660000,color:#fff
```

### เป้าหมายช่องโหว่ Browser

```mermaid
graph TD
    subgraph "เป้าหมาย Exploit ที่พบบ่อย"
        T1["Internet Explorer\n(CVE-2021-26411)"]
        T2["Chrome V8\n(CVE-2023-2033)"]
        T3["Firefox\n(CVE-2024-9680)"]
        T4["Edge Chromium\n(shared Chrome CVEs)"]
        T5["WebKit/Safari\n(CVE-2023-42917)"]
    end
    subgraph "Plugin เป้าหมาย (Legacy)"
        P1["Adobe Flash\n(Deprecated)"]
        P2["Java Applets\n(หายาก)"]
        P3["Silverlight\n(Deprecated)"]
    end
    style T1 fill:#cc0000,color:#fff
    style T2 fill:#ff6600,color:#fff
    style P1 fill:#999,color:#fff
```

### Timeline การตอบสนอง

```mermaid
gantt
    title Drive-By Download Response Timeline
    dateFormat HH:mm
    axisFormat %H:%M
    section Detection
        Alert triggered         :a1, 00:00, 5min
        ยืนยัน exploitation     :a2, after a1, 10min
    section Containment
        แยก endpoint            :a3, after a2, 5min
        Block redirect chain    :a4, after a3, 15min
    section Investigation
        วิเคราะห์ process tree  :a5, after a4, 30min
        Sandbox payload         :a6, after a5, 30min
        Sweep endpoints         :a7, after a6, 60min
    section Recovery
        Reimage ถ้าจำเป็น       :a8, after a7, 120min
        อัปเดต browser/patches  :a9, after a8, 60min
```

---

## 1. การดำเนินการทันที (15 นาทีแรก)

| # | การดำเนินการ | ผู้รับผิดชอบ |
|:---|:---|:---|
| 1 | แยก endpoint ผ่าน EDR | SOC T1 |
| 2 | เก็บ browser process tree และ network connections | SOC T1 |
| 3 | Block redirect chain ทั้งหมด (ทุก domains/IPs) | SOC T2 |
| 4 | ตรวจ proxy logs: users อื่นที่เข้า URL เดียวกัน | SOC T2 |
| 5 | ส่ง payload ที่ download ไป sandbox | SOC T2 |
| 6 | ตรวจ browser และ plugin patch level | IT Team |

## 2. รายการตรวจสอบ

### วิเคราะห์ Browser/Endpoint
- [ ] Process tree: browser → child processes
- [ ] ไฟล์ที่ download ใน temp/downloads folders
- [ ] Browser history: URL chain ที่นำไปยัง exploit
- [ ] Network connections หลัง exploitation
- [ ] Scheduled tasks, services, หรือ registry ใหม่
- [ ] Memory dump สำหรับวิเคราะห์ exploit shellcode

### วิเคราะห์ Network/Proxy
- [ ] URL redirect chain เต็มจาก proxy logs
- [ ] DNS queries ไปยัง domains ผิดปกติ
- [ ] ข้อมูล certificate สำหรับ HTTPS connections
- [ ] ตรวจว่า URL อยู่ใน threat intel blocklists
- [ ] วิเคราะห์ JavaScript จาก exploit kit landing page

### ประเมินขอบเขต
- [ ] มี users กี่คนที่เข้า URL อันตรายเดียวกัน?
- [ ] มี endpoints อื่นที่ถูก exploit ด้วยหรือไม่?
- [ ] แหล่งที่มาเป็นเว็บปกติที่ถูก compromise หรือสร้างขึ้นมา?
- [ ] เป็นส่วนหนึ่งของ malvertising campaign หรือไม่?

## 3. การควบคุม (Containment)

| ขอบเขต | การดำเนินการ |
|:---|:---|
| **Endpoint** | EDR isolation, เก็บสำหรับ forensics |
| **เครือข่าย** | Block domains/IPs ทั้งหมดใน redirect chain |
| **DNS** | Sinkhole exploit kit domains |
| **Proxy** | เพิ่ม URL category block สำหรับ exploit kits |
| **Browser** | บังคับอัปเดตเวอร์ชันล่าสุด |

## 4. การกำจัดและกู้คืน

1. Reimage endpoint ถ้ายืนยัน post-exploitation activity
2. บังคับอัปเดต browser ทั้งองค์กร
3. ปิด legacy plugins (Flash, Java, Silverlight)
4. Deploy browser isolation สำหรับการ browse ที่มีความเสี่ยง
5. อัปเดต proxy/DNS blocklists ด้วย IOCs ใหม่

## 5. หลังเหตุการณ์ (Post-Incident)

| คำถาม | คำตอบ |
|:---|:---|
| Exploit อะไรถูกใช้ (CVE)? | [CVE number] |
| Browser patch เต็มหรือไม่? | [ใช่/ไม่] |
| Legacy plugins เปิดอยู่หรือไม่? | [รายการ] |
| User ถูกพาไปยังเว็บอันตรายอย่างไร? | [Malvertising/link/redirect] |

## 6. Detection Rules (Sigma)

```yaml
title: Browser Spawning Suspicious Child Process
logsource:
    product: windows
    category: process_creation
detection:
    selection_parent:
        ParentImage|endswith:
            - '\chrome.exe'
            - '\msedge.exe'
            - '\firefox.exe'
            - '\iexplore.exe'
    selection_child:
        Image|endswith:
            - '\cmd.exe'
            - '\powershell.exe'
            - '\wscript.exe'
            - '\mshta.exe'
    condition: selection_parent and selection_child
    level: high
```

## เอกสารที่เกี่ยวข้อง
- [Watering Hole Playbook](Watering_Hole.th.md)
- [Malware Infection Playbook](Malware_Infection.th.md)
- [Exploit Playbook](Exploit.th.md)

## References
- [MITRE T1189 — Drive-by Compromise](https://attack.mitre.org/techniques/T1189/)
- [Trend Micro — Exploit Kit Overview](https://www.trendmicro.com/vinfo/us/security/definition/exploit-kit)
