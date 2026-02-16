# Playbook: Cryptomining

**ID**: PB-31 | **ระดับความรุนแรง**: สูง | **MITRE**: [T1496](https://attack.mitre.org/techniques/T1496/)
**ทริกเกอร์**: GuardDuty CryptoCurrency finding, CPU/billing spike, IDS mining pool

## 1. การวิเคราะห์
| รายการ | เสร็จ |
|:---|:---:|
| Host/instance ที่ใช้ mining | ☐ |
| Mining binary (xmrig, cccminer, etc.) | ☐ |
| Mining pool domain/IP | ☐ |
| Entry vector (exploit/credential abuse) | ☐ |
| มีกี่เครื่อง? (ตรวจทุก region!) | ☐ |
| Billing impact | ☐ |

## 2. การควบคุม
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **Kill** mining process | ☐ |
| 2 | **Block** mining pool IPs/domains | ☐ |
| 3 | **Isolate** หรือ **terminate** instances | ☐ |
| 4 | **ปิด IAM credentials** ที่ใช้สร้าง instances | ☐ |

## 3. การกำจัด
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | ลบ mining binaries + persistence (crontab, systemd) | ☐ |
| 2 | ลบ instances ที่ผู้โจมตีสร้าง **(ทุก region!)** | ☐ |
| 3 | หมุนเวียน credentials | ☐ |

## 4. การฟื้นฟู
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | ตั้ง billing alerts + budget caps | ☐ |
| 2 | ใช้ SCP จำกัด instance types / regions | ☐ |
| 3 | ขอ billing credit จาก cloud provider | ☐ |

## 5. เกณฑ์การยกระดับ
| เงื่อนไข | ยกระดับไปยัง |
|:---|:---|
| Billing >$1,000 ผิดปกติ | Finance + Cloud team |
| Supply chain / insider | CISO + HR |
| หลาย accounts | Major Incident |

## เอกสารที่เกี่ยวข้อง
- [กรอบ IR](../Framework.th.md) | [PB-22 AWS EC2](AWS_EC2_Compromise.th.md)
