# ขั้นตอนการ Deploy ระบบ (Deployment Procedures)

**ที่มา**: zcrAI Platform Operations & Industrialization Master

## 1. การ Deploy ขึ้น Production

เป้าหมาย: `https://app.zcr.ai` (Server IP: `45.118.132.160`)

### กระบวนการมาตรฐาน (Standard Pipeline)
-   **Trigger**: GitHub Actions ทำงานเมื่อมีการ Merge เข้า branch `main`
-   **Sync**: ใช้ `rsync` ส่งไฟล์ไปยัง Server
-   **Orchestration**:
    ```bash
    docker compose -f docker-compose.prod.yml up -d --build
    ```

### การเข้าถึงผ่าน IP โดยตรง & SSH
ใช้ IP ตรงหาก DNS หรือ SSH ผ่าน `zcr.ai` มีปัญหา
**SSH Config (`~/.ssh/config`)**:
```ssh
Host zcrAI
  HostName 45.118.132.160
  User root
  IdentityFile ~/.ssh/id_rsa
  IdentitiesOnly yes
```

## 2. รูปแบบการทำ Hotfix ด้วยตนเอง (Manual Hotfix Patterns)

### Frontend Hotfix (ไม่ต้อง Rebuild Image)
สำหรับการแก้ UI เร่งด่วน:
1.  **Local Build**:
    ```bash
    cd frontend && npm run build
    ```
2.  **Sync**:
    ```bash
    rsync -avz --progress frontend/dist/* zcrAI:/var/www/app.zcr.ai/
    ```
3.  **Bypass Cache**: แจ้งให้ผู้ใช้ทำ Hard Refresh (Ctrl+Shift+R)

### คำเตือนเรื่อง Frontend Persistence
การแก้ไขไฟล์ใน `dist/` บน Host จะไม่มีผลกับ Container ที่รันอยู่ หากไม่ได้ Mount Volume นั้นไว้ สำหรับการอัปเดตใน Container:
1.  **Copy Assets**:
    ```bash
    ssh zcrAI "docker cp /root/zcrAI/frontend/dist/. zcrai_frontend:/usr/share/nginx/html/"
    ```

### Backend Selective Rebuild
หากการ Build ทั้งระบบล้มเหลว ให้เลือก Build เฉพาะบริการ:
```bash
ssh zcrAI "cd /root/zcrAI && docker compose -f docker-compose.prod.yml up -d --build backend"
```

## 3. ตัวแปรสภาพแวดล้อม (Environment Variables)

**สำคัญ**: คำสั่ง `docker restart` **ไม่** โหลดค่า `.env` ใหม่

**ขั้นตอนการอัปเดต .env**:
1.  ตรวจสอบตำแหน่งไฟล์ (Root หรือ Nested)
2.  **สร้าง Container ใหม่ (Recreate)**:
    ```bash
    ssh zcrAI "docker rm -f zcrai_backend && docker run -d --name zcrai_backend --env-file /root/zcrAI/backend/api/.env ... zcrai-backend"
    ```

## 4. การกู้วิกฤตฉุกเฉิน (Emergency Restoration)

### การปิดการทำงานบางส่วน (Disabling Components)
หาก Dependency ใหม่ทำให้เกิด Crash Loop (502 Gateway) ให้ Comment ปิดการทำงานส่วนนั้นชั่วคราว (เช่น `scheduler.init()`) แล้ว `rsync` เฉพาะไฟล์นั้นขึ้นไป เพื่อให้ API หลักกลับมาทำงานได้ก่อน
