# คู่มือ Integration Hub

**ที่มา**: zcrAI System & Engineering Guides

## ภาพรวม
Integration Hub รองรับ **ผู้ให้บริการความปลอดภัยกว่า 43+ ราย** แบ่งเป็นหลายระดับ (EDR, SIEM, Cloud, Identity, Email, Threat Intel)

## องค์ประกอบหลัก

### 1. Community Feeds (Abuse.ch)
บริการต่อไปนี้ถูกเชื่อมต่อแบบ "No-Key" (ไม่ต้องใช้ API Key):
-   ThreatFox
-   URLhaus
-   MalwareBazaar
-   Feodo Tracker

### 2. การตรวจสอบสถานะ (Health Monitoring)
-   **รอบการตรวจสอบ**: ทุกๆ 30 วินาที
-   **การแก้ปัญหาเบื้องต้น**:
    -   หากหน้า UI แสดง "Error" แต่ Global Key ใช้งานได้ ให้ตรวจสอบ **Credentials เฉพาะของ Tenant** ในตาราง `api_keys`

## การพัฒนาและการแก้ปัญหา

-   **Dev Mode**: ใช้ `VITE_BYPASS_AUTH=true` ใน `frontend/.env` เพื่อเข้าถึง Catalog โดยไม่ต้องรัน Backend/Database
-   **การเชื่อมต่อ**: หาก `localhost` ใช้งานไม่ได้ ให้ลองใช้ `http://127.0.0.1:8000`
