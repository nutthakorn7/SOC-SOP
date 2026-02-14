# การจัดการฐานข้อมูลและความลับ (Database & Secrets Management)

**ที่มา**: zcrAI Platform Operations & Industrialization Master

## 1. ความคงทนของข้อมูล (Data Persistence & Resilience)

-   **PostgreSQL (`zcrai`)**: จัดเก็บ Alerts, Integrations, Detection Rules, และ Compliance Snapshots
-   **ClickHouse (`montara_analytics`)**: จัดเก็บ Security Events แบบ Columnar เพื่อการวิเคราะห์ที่รวดเร็ว
-   **Redis**: ใช้สำหรับ Session Caching; ระบบถูกออกแบบให้ทำงานต่อได้ (Fail-open) แม้ Redis จะไม่สามารถติดต่อได้

## 2. การ Seed กฎตรวจจับเบื้องหลัง (Background Rule Seeding)

เมื่อ Backend เริ่มทำงาน ระบบจะทำการ Seed Detection Rules อัตโนมัติ:
-   **การตรวจสอบ**: ดู Log ว่ามีข้อความ `✨ Seeding Complete!` หรือไม่
-   **คำเตือนเรื่องข้อขัดแย้ง**: การแก้กฎที่เป็น Default ผ่าน SQL โดยตรง จะถูกทับด้วยค่าเดิมเมื่อมีการ Restart ระบบ ให้ทำการแก้ไขผ่าน Source Seeding Scripts เท่านั้น (`backend/api/scripts/seed-detection-rules-v2.ts`)

## 3. การปฏิบัติการ (Operations)

### ความคงทนของ Content Library
ตาราง `content_packs` ใช้ติดตามสถานะการติดตั้งและเวอร์ชันของ Sigma rules กว่า 2,660+ ข้อ
-   **การจัดการ**: ใช้ Logic ใน `forensics.controller.ts` ซึ่งจะดึงข้อมูลจาก `content_packs`

### การแก้ปัญหาข้อมูลไม่แสดง (Troubleshooting Data Visibility)
หาก Alerts ไม่แสดงบนหน้า UI:
1.  **ตรวจสอบ Tenant ID**: ตรวจสอบว่า Session ของ SuperAdmin ตรงกับ `tenant_id` ของข้อมูล
2.  **ช่วงเวลา (Time Windows)**: ตรวจสอบตัวกรองเวลา (เช่น 24 ชม. ล่าสุด vs 7 วัน)
3.  **การ Map Entity**: ตรวจสอบว่า field `affectedUser` หรือ `sourceIp` มีข้อมูลครบถ้วน
