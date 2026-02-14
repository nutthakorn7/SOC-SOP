# การแก้ปัญหา: ปัญหาที่พบบ่อย (Troubleshooting: Common Issues)

**ที่มา**: zcrAI Platform Operations & Industrialization Master

## 1. Infrastructure & Docker

### ข้อมูล Metadata เสียหาย (500/EOF Errors)
หาก Docker แจ้ง error `input/output error`:
1.  ปิด Docker: `pkill -9 -f Docker`
2.  ลบไฟล์ Lock: `rm -rf ~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw.lock`
3.  เปิด Docker ใหม่

### พอร์ตชนกัน (Port Conflicts)
**อาการ**: `address already in use` (Port 8000)
**วิธีแก้**:
1.  หา Process: `lsof -i :8000`
2.  หยุด Process: `kill -9 <PID>`
3.  ตรวจสอบ Zombie process: `ssh zcrAI "fuser -k 8000/tcp"`

### Nginx SSL ล้มเหลว
**อาการ**: `BIO_new_file() failed`
**สาเหตุ**: พาธไฟล์บน Host ไม่ตรงกับที่ Mount เข้าไปใน Container (สำหรับ Certificates)
**วิธีแก้**: ตรวจสอบ `nginx.conf` ให้ชี้ไปยังพาธที่ถูกต้อง เช่น `/etc/letsencrypt/live/...` และแน่ใจว่าได้ Mount volume เข้าไปแล้ว

## 2. ปัญหา Backend

### Connection Timeouts & CPU สูง
**อาการ**: `zcrai_backend` ใช้ CPU 100%, Log ขึ้น `CONNECT_TIMEOUT`
**สาเหตุ**:
-   ติดต่อ Redis/Postgres ไม่ได้ ทำให้เกิดลูป Retry
-   รหัสผ่านใน `.env` ไม่ตรงกัน
**วิธีแก้**:
-   ตรวจสอบ `REDIS_PASSWORD` และ `DATABASE_URL`
-   ตรวจสอบว่า Backend Container อยู่ใน Network เดียวกับ Database (`zcrai_default`)

### "Module not found" / Binary ไม่ตรงรุ่น
**สาเหตุ**: การ Sync โฟลเดอร์ `node_modules` จากเครื่อง macOS ไปยัง Linux Server
**วิธีแก้**:
1.  ลบ `node_modules` บน Server ทิ้ง
2.  รัน `npm install` หรือ `bun install` ใหม่บน Server

## 3. ปัญหา Frontend

### ไม่เจอไฟล์ JS Bundle (404)
**อาการ**: หน้าขาว (Blank Page) หลังจากทำ Hotfix
**สาเหตุ**: ไฟล์ `index.html` อัปเดตแล้ว แต่อ้างถึงไฟล์ JS Hash ใหม่ที่ยังไม่ได้ก๊อปปี้ไป
**วิธีแก้**:
1.  ตรวจสอบว่าไฟล์มีอยู่จริงบน Host `dist/`
2.  รัน `docker cp` ไปยัง Container อีกครั้ง
3.  เคลียร์ Browser Cache

### Hardcoded API URLs
**อาการ**: Integrations พังบน Production แต่ใช้งานได้ปกติบน Local
**สาเหตุ**: ค่า `localhost:8000` ถูกฝัง (Bake) เข้าไปในไฟล์ JS
**วิธีแก้**:
-   เพิ่ม `.env` เข้าไปใน `.dockerignore`
-   Rebuild โดยใช้ flag `--no-cache`
