# Playbook: AWS EC2 Instance Compromise

**ID**: PB-22 | **ระดับความรุนแรง**: วิกฤต | **MITRE**: [T1190](https://attack.mitre.org/techniques/T1190/), [T1496](https://attack.mitre.org/techniques/T1496/)
**ทริกเกอร์**: GuardDuty finding, CloudWatch CPU alarm, VPC Flow Log anomaly

## 1. การวิเคราะห์
### 1.1 GuardDuty Finding Types
| Finding | ความรุนแรง |
|:---|:---|
| `CryptoCurrency:EC2/BitcoinTool` | สูง |
| `Backdoor:EC2/C&CActivity` | สูง |
| `UnauthorizedAccess:EC2/SSHBruteForce` | ปานกลาง |
| `Trojan:EC2/BlackholeTraffic` | สูง |

### 1.2 รายการตรวจสอบ
| รายการ | เสร็จ |
|:---|:---:|
| Instance ID, Region, Owner tag | ☐ |
| Production หรือ Dev/Test? | ☐ |
| IAM role ที่ attach | ☐ |
| Security Group (เปิดอะไร?) | ☐ |
| VPC Flow Logs — outbound ผิดปกติ | ☐ |
| Entry vector (SSH เปิดหรือ web app?) | ☐ |

## 2. การควบคุม
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | **Snapshot EBS** สำหรับ forensics | ☐ |
| 2 | **Isolate** — attach restrictive SG | ☐ |
| 3 | **Deregister** จาก ALB/ASG | ☐ |
| 4 | **ปิด IAM role** credentials | ☐ |

## 3. การกำจัด
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | Terminate instance (ถ้า stateless) | ☐ |
| 2 | Rebuild จาก clean AMI | ☐ |
| 3 | หมุนเวียน IAM credentials + SSH keys | ☐ |
| 4 | Patch entry vector | ☐ |

## 4. การฟื้นฟู
| # | การดำเนินการ | เสร็จ |
|:---:|:---|:---:|
| 1 | ใช้ SSM แทน SSH | ☐ |
| 2 | บังคับ IMDSv2 (ปิด v1) | ☐ |
| 3 | เปิด GuardDuty | ☐ |

## 5. เกณฑ์การยกระดับ
| เงื่อนไข | ยกระดับไปยัง |
|:---|:---|
| Production ถูกบุกรุก | SOC Lead + Cloud |
| IAM credentials ถูกขโมย | [PB-16 Cloud IAM](Cloud_IAM.th.md) |
| Billing spike | Finance + Cloud |

## เอกสารที่เกี่ยวข้อง
- [กรอบ IR](../Framework.th.md) | [PB-16 Cloud IAM](Cloud_IAM.th.md)
