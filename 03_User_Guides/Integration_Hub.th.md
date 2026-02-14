# กลยุทธ์การเชื่อมต่อเครื่องมือ (Tool Integration Strategy)

เอกสารนี้ระบุกลยุทธ์ในการเชื่อมต่อเครื่องมือความปลอดภัยและแหล่งข้อมูล Log เข้าสู่สถาปัตยกรรม SOC

## 1. การเชื่อมต่อ Log Source

### 1.1 กลไกการส่งข้อมูล
-   **API-based**: บริการ Cloud (AWS, M365, SaaS) มักต้องใช้วิธี API Polling
-   **Agent-based**: Server/Endpoint ใช้ Agent (เช่น Filebeat, Winlogbeat, OSQuery)
-   **Syslog**: อุปกรณ์เครือข่ายและระบบ Legacy

### 1.2 การปรับให้เป็นมาตรฐาน (Normalization)
-   Log ทั้งหมดต้องถูกปรับเนื้องหาให้เข้ากับ Schema มาตรฐาน (เช่น CIM, ECS)
-   **ฟิลด์สำคัญ (Key Fields)**:
    -   `timestamp` (UTC)
    -   `src_ip`, `dst_ip`
    -   `user`, `hostname`
    -   `action`, `outcome`

## 2. การเติมข้อมูล (Enrichment Integrations)

### 2.1 Threat Intelligence
-   เชื่อมต่อ Feed (เช่น ThreatFox, URLhaus, Commercial Feeds) เพื่อระบุค่าชื่อเสียง (Reputation)
-   **กระบวนการ**: ค้นหา IP, Domain, Hash จาก Alert โดยอัตโนมัติ

### 2.2 บริบทสินทรัพย์ (Asset Context)
-   เชื่อมต่อกับ CMDB หรือ Identity Provider (AD/LDAP)
-   **วัตถุประสงค์**: เพื่อให้บริบทว่า "ใคร" (บทบาทผู้ใช้) และ "อะไร" (ความสำคัญของ Server) ที่เกี่ยวข้องกับเหตุการณ์

## 3. การเฝ้าระวังสถานะ (Health Monitoring)

-   **Heartbeat**: ตรวจสอบว่า Integration ส่งสัญญาณสถานะมาสม่ำเสมอ
-   **ความสดใหม่ของข้อมูล**: แจ้งเตือนหาก Log Source หยุดส่งข้อมูลเกิน 1 ชั่วโมง
-   **อัตรา Error**: เฝ้าระวัง API error (401/403/429) เพื่อตรวจจับปัญหา Credential หรือ Quota
