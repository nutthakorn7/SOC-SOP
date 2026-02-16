# Playbook: DNS Tunneling

**ID**: PB-25 | **ระดับความรุนแรง**: สูง | **MITRE**: [T1071.004](https://attack.mitre.org/techniques/T1071/004/)
**ทริกเกอร์**: DNS analytics alert, IDS, high-entropy subdomain detection

## 1. การวิเคราะห์
### 1.1 ตัวบ่งชี้
| ตัวบ่งชี้ | ค่าปกติ | ค่าน่าสงสัย |
|:---|:---|:---|
| Subdomain length | <30 chars | >50 chars |
| Shannon entropy | <3.5 | >4.0 |
| Query rate (single domain) | <10/min | >100/min |
| TXT query volume | ต่ำ | สูงผิดปกติ |
| NULL/CNAME unusual | น้อย | มาก |

### 1.2 เครื่องมือที่ใช้ DNS Tunnel
- iodine, dnscat2, DNSExfiltrator, Cobalt Strike DNS, SUNBURST

### 1.3 รายการตรวจสอบ
| รายการ | เสร็จ |
|:---|:---:|
| Domain ที่ใช้ tunnel | ☐ |
| Source host | ☐ |
| Process ที่ทำ DNS queries | ☐ |
| ปริมาณข้อมูลที่ส่งออก | ☐ |

## 2. การควบคุม
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **Block** tunnel domain (DNS RPZ / Sinkhole) | ☐ |
| 2 | **Isolate** source host | ☐ |
| 3 | **Kill** tunnel process | ☐ |

## 3. การฟื้นฟู
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | บังคับ DNS ภายในเท่านั้น (block external DNS) | ☐ |
| 2 | Block DoH/DoT ไปยัง external | ☐ |
| 3 | เปิด DNS analytics | ☐ |

## 4. เกณฑ์การยกระดับ
| เงื่อนไข | ยกระดับไปยัง |
|:---|:---|
| Confirmed data exfiltration | [PB-08 Data Exfil](Data_Exfiltration.th.md) + Legal |
| C2 over DNS | [PB-13 C2](C2_Communication.th.md) |
| APT indicators | CISO + Threat Intel |

## เอกสารที่เกี่ยวข้อง
- [กรอบ IR](../Framework.th.md) | [PB-13 C2](C2_Communication.th.md)
