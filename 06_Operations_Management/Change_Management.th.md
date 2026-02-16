# SOP การจัดการเปลี่ยนแปลง SOC

> **รหัสเอกสาร:** CHG-001  
> **เวอร์ชัน:** 1.0  
> **อัปเดตล่าสุด:** 2026-02-15  
> **เจ้าของ:** SOC Manager

---

## ขอบเขต

ครอบคลุมการเปลี่ยนแปลง: Detection rules, Playbooks, SIEM config, EDR policies, Firewall rules, SOAR workflows, TI feeds, เครื่องมือ SOC

---

## ประเภทการเปลี่ยนแปลง

| ประเภท | ความเสี่ยง | อนุมัติโดย | เวลา | ตัวอย่าง |
|:---|:---:|:---|:---:|:---|
| **Standard** | ต่ำ | SOC Lead | 1 วัน | Sigma rule ใหม่, whitelist |
| **Normal** | กลาง | SOC Manager | 3 วัน | SIEM parser, log source ใหม่ |
| **Emergency** | สูง | SOC Manager + CISO | ทันที | Patch เร่งด่วน, ตอบเหตุ |
| **Major** | สูง | CAB | 5+ วัน | SIEM upgrade, เครื่องมือใหม่ |

---

## ขั้นตอน

```mermaid
graph TD
    A[1. ส่ง Change Request] --> B[2. Review เทคนิค]
    B --> C[3. ทดสอบ Staging]
    C --> D[4. อนุมัติ]
    D --> E[5. Deploy Production]
    E --> F[6. ตรวจสอบหลัง Deploy]
    F --> G[7. ปิด & บันทึก]
```

### ขั้นตอนสำคัญ:
1. **ส่ง Change Request** — ใช้ [แม่แบบ](../templates/change_request_rfc.th.md)
2. **Review เทคนิค** — ตรวจสอบความถูกต้อง, conflict, rollback plan
3. **ทดสอบ** — Validate syntax, ทดสอบกับข้อมูลจริง 7 วัน
4. **อนุมัติ** — ตามระดับประเภท
5. **Deploy** — ใช้ version control (git), ติด tag
6. **ตรวจหลัง Deploy** — ภายใน 24 ชม.
7. **ปิด** — อัปเดตเอกสาร

---

## กรณีฉุกเฉิน

```
⚡ Emergency change:
   1. ขออนุมัติปากเปล่าจาก SOC Manager
   2. บันทึกภายใน 24 ชม.
   3. ทบทวนใน standup ถัดไป
   4. ต้องมี rollback plan เสมอ
```

---

## การประเมินความเสี่ยง

| ระดับ | เกณฑ์ | การอนุมัติ | หน้าต่างบำรุงรักษา |
|:---|:---|:---|:---|
| **ต่ำ** | เอกสาร, ไม่กระทบ | SOC Lead | ทุกเวลา |
| **กลาง** | Detection rule, Parser | SOC Manager | เวลาทำการ |
| **สูง** | SIEM config, Integration | SOC Manager + CAB | กำหนดเวลา |
| **วิกฤต** | โครงสร้างพื้นฐาน, Auth | CISO + CAB | Downtime กำหนด |

## รายการตรวจสอบการเปลี่ยนแปลง

| # | ขั้นตอน | ผู้รับผิดชอบ | เสร็จ |
|:---:|:---|:---|:---:|
| 1 | RFC ถูกส่งและอนุมัติ | Engineer | ☐ |
| 2 | Peer review เสร็จ | Detection Eng | ☐ |
| 3 | สำรองข้อมูลก่อน Deploy | Engineer | ☐ |
| 4 | ทดสอบใน Staging | Engineer | ☐ |
| 5 | แผน Rollback พร้อม | Engineer | ☐ |
| 6 | Deploy ไปยัง Production | Engineer | ☐ |
| 7 | ตรวจสอบ 30 นาทีหลัง Deploy | SOC Lead | ☐ |

## เอกสารที่เกี่ยวข้อง

- [แม่แบบ Change Request](../templates/change_request_rfc.th.md)
- [SOP ทดสอบ Detection Rule](Detection_Rule_Testing.th.md)
- [รายการตรวจสอบ SOC](SOC_Checklists.th.md)
