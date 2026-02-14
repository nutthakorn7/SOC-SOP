# การเปิดใช้งานระบบและลำดับการเริ่มทำงาน (System Activation & Startup Sequence)

**ที่มา**: zcrAI Platform Operations & Industrialization Master

## 1. การเริ่มต้นโครงสร้างพื้นฐาน (Docker)

แพลตฟอร์ม SOC ทำงานบนสถาปัตยกรรมแบบ Multi-service ที่ประกอบด้วย:
-   **PostgreSQL**: ฐานข้อมูลหลัก (Port 5432)
-   **ClickHouse**: ระบบวิเคราะห์ข้อมูล (Port 8123/9000)
-   **Redis**: ระบบ Cache (Port 6379)

### ขั้นตอนการเริ่มระบบ
1.  **เปิด Docker Desktop**: ตรวจสอบให้แน่ใจว่า Docker Daemon ทำงานปกติ
2.  **เริ่มบริการต่างๆ**:
    ```bash
    docker compose up -d postgres redis clickhouse
    ```
3.  **ตรวจสอบ Port Mapping**:
    -   PostgreSQL: `5433` -> `5432`
    -   Redis: `6379`
    -   ClickHouse: `9000` (Native) / `8123` (HTTP)

## 2. การกำหนดค่าฐานข้อมูล (Database Initialization)

### PostgreSQL (Drizzle)
อัปเดต Schema และเพิ่มข้อมูลเริ่มต้น:

```bash
# ส่ง schema ไปยัง PostgreSQL container
ssh zcrAI "docker exec zcrai_backend bun run db:push"

# สร้างข้อมูลผู้ดูแลระบบและ SuperAdmin เริ่มต้น
bun run scripts/seed-superadmin.ts
```

### ClickHouse Initialization
จำเป็นต้องทำหลังจากมีการล้างข้อมูล (Wipe) หรือติดตั้งใหม่:

1.  **สร้างฐานข้อมูล**:
    ```bash
    ssh zcrAI "docker exec zcrai_clickhouse clickhouse-client --query='CREATE DATABASE IF NOT EXISTS zcrai'"
    ```
2.  **Sync Schema**:
    ตรวจสอบให้แน่ใจว่าตาราง `security_events` และ Materialized Views ถูกสร้างเรียบร้อย (อ้างอิง `collector/infra/db/clickhouse/migrations/001_init_schema.sql`)
3.  **ตรวจสอบความถูกต้อง**:
    ```bash
    ssh zcrAI "docker exec zcrai_clickhouse clickhouse-client --query='SHOW TABLES FROM zcrai'"
    ```

## 3. การกำหนดค่า Content Library

ไลบรารี Content (Sigma rules) ต้องการตาราง `content_packs` เพื่อทำงาน

1.  **สร้าง Migration**:
    ```bash
    ssh zcrAI "docker exec zcrai_backend bun run db:generate"
    ```
2.  **ใช้งาน Migration**:
    ```bash
    ssh zcrAI "docker exec zcrai_backend cat drizzle/0035_striped_groot.sql | docker exec -i zcrai_postgres psql -U postgres -d zcrai"
    ```
3.  **ตรวจสอบ**:
    เช็คว่าตารางถูกสร้างแล้ว:
    ```bash
    ssh zcrAI "docker exec zcrai_postgres psql -U postgres -d zcrai -c '\dt content_packs'"
    ```

## 4. สถาปัตยกรรมบริการบน Local (Local Service Architecture)

| บริการ (Service) | พอร์ต (Local Port) | รายละเอียด |
| :--- | :--- | :--- |
| **Frontend** | `5173` | React/HeroUI Dev Server |
| **SOC API** | `8000` | Bun/Elysia Backend |
| **PostgreSQL** | `5433` | Metadata Store |
| **ClickHouse** | `8123` | Analytics Warehouse |
| **Redis** | `6380` | Session/Lockout Cache |
