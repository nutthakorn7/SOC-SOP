# คู่มือการจัดการ Content (Content Management Guide)

**ที่มา**: zcrAI System & Engineering Guides

## ภาพรวม
หน้า Content Management เป็นศูนย์กลางในการจัดการกฎการตรวจจับภัยคุกคาม (Detection Rules - Sigma/SNR) และเทมเพลตของกฎ (Rule Templates)

## ฟีเจอร์หลัก

### 1. ตัวกรองและการค้นหา (Filters & Search)
-   **หมวดหมู่ (Categories)**: กรองตามประเภทภัยคุกคาม (เช่น `privilege-escalation`, `reconnaissance`)
-   **ความรุนแรง (Severity)**: High, Critical, Medium, Low
-   **สถานะ (Status)**: เปิดใช้งาน (Enabled) / ปิดใช้งาน (Disabled)

### 2. การดำเนินการ (Actions)
-   **Bulk Actions**: เปิด/ปิด การใช้งานกฎหลายข้อพร้อมกัน
-   **สถานะของกฎ (Rule Status)**:
    -   **Event**: กฎที่บันทึกเหตุการณ์ความปลอดภัยทั่วไป
    -   **Finding**: กฎที่สร้างการค้นพบหรือการแจ้งเตือนที่มีความสำคัญสูง (High-fidelity)

## แคตตาล็อกของกฎ (Rule Catalogs)

### Content Packs
-   **Sigma Core**: กฎกว่า 2,660+ ข้อ (ครอบคลุม Endpoint, Network, Cloud)
-   **Windows Security**: การมองเห็นระดับ OS เชิงลึก
-   **Ransomware**: ชุดตรวจจับพิเศษสำหรับ Ransomware โดยเฉพาะ

### Rule Templates
รูปแบบมาตรฐานสำหรับการสร้างกฎใหม่:
-   **IAM**: การข้ามขั้นตอน MFA, การสร้างบัญชี Privilege
-   **Cloud**: S3 ปล่อย Public, การ Login ด้วย Root
-   **Email**: Phishing, รูปแบบ BEC ต่างๆ
