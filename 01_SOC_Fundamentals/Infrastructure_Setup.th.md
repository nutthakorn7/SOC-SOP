# คู่มือติดตั้ง SOC Infrastructure — Hands-On

> **รหัสเอกสาร:** INFRA-001  
> **เวอร์ชัน:** 1.0  
> **อัปเดตล่าสุด:** 2026-02-15  
> **อ่านก่อน:** [คู่มือเลือก Technology Stack](Technology_Stack.th.md)

---

## คู่มือนี้ครอบคลุม

การติดตั้ง **Open-Source Stack (Stack A)** ด้วย Wazuh ทีละขั้น — ค่าใช้จ่ายศูนย์ ฟังก์ชันครบ

---

## ส่วนที่ 1: ติดตั้ง Wazuh

### ความต้องการขั้นต่ำ
- Ubuntu 22.04 LTS
- 4 cores / 8 GB RAM / 50 GB disk
- Static IP

### ติดตั้ง

```bash
# ดาวน์โหลดและรัน
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.9/config.yml

# แก้ config.yml — ใส่ IP เซิร์ฟเวอร์
# แล้วรัน:
sudo bash wazuh-install.sh -a

# ⚠️ จดรหัส admin ที่แสดงตอนจบ!
# เข้า: https://YOUR_SERVER_IP
```

### ตรวจสอบ
```bash
sudo systemctl status wazuh-manager
sudo systemctl status wazuh-indexer
sudo systemctl status wazuh-dashboard
```

---

## ส่วนที่ 2: ติดตั้ง Agent

### Windows
```powershell
# ดาวน์โหลดจาก Wazuh Dashboard → Agents → Deploy
# หรือ:
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.0-1.msi -OutFile wazuh-agent.msi
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="YOUR_SERVER_IP"
net start WazuhSvc
```

### Linux
```bash
# Ubuntu/Debian
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo gpg --dearmor -o /usr/share/keyrings/wazuh.gpg
echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list
sudo apt update && sudo apt install wazuh-agent -y
sudo sed -i 's/MANAGER_IP/YOUR_SERVER_IP/' /var/ossec/etc/ossec.conf
sudo systemctl enable --now wazuh-agent
```

---

## ส่วนที่ 3: ตั้งค่า Log Sources

### Active Directory
```xml
<!-- เพิ่มใน agent ossec.conf บน DC -->
<localfile>
  <location>Security</location>
  <log_format>eventchannel</log_format>
  <query>Event/System[EventID=4624 or EventID=4625 or EventID=4688 or EventID=4720 or EventID=1102]</query>
</localfile>
```

### Firewall (Syslog)
```xml
<!-- เพิ่มใน Wazuh server ossec.conf -->
<remote>
  <connection>syslog</connection>
  <port>514</port>
  <protocol>udp</protocol>
  <allowed-ips>FIREWALL_IP</allowed-ips>
</remote>
```

---

## ส่วนที่ 4: ติดตั้ง Sysmon (Windows)

```powershell
# เพิ่มความสามารถการตรวจจับ Windows อย่างมาก
Invoke-WebRequest -Uri https://download.sysinternals.com/files/Sysmon.zip -OutFile Sysmon.zip
Expand-Archive Sysmon.zip
Invoke-WebRequest -Uri https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml -OutFile sysmonconfig.xml
.\Sysmon64.exe -accepteula -i sysmonconfig.xml
```

---

## ส่วนที่ 5: ตั้งค่า Alert (Slack)

```bash
# สร้าง Slack webhook → ตั้งค่า Wazuh integration
# เมื่อมี alert level 10+ → ส่ง Slack ทันที
```

---

## ส่วนที่ 6: Sentinel (ถ้าเลือก Stack B)

```
1. Azure Portal → สร้าง Microsoft Sentinel
2. สร้าง Log Analytics Workspace
3. เชื่อม Data Connectors: M365 Defender, Azure AD, Azure Activity
4. เปิด Analytics Rules → ใช้ template
5. เสร็จ! มี SIEM ใน 30 นาที
```

---

## Checklist ตรวจสอบ

```
□ Wazuh Dashboard เข้าได้
□ Agent เชื่อมต่อ ≥3 เครื่อง
□ เห็น event real-time
□ AD login events มาถึง
□ Firewall logs มาถึง
□ Sysmon ติดตั้งบน Windows
□ Custom rule ทำงาน
□ Alert ส่ง Email/Slack ได้
□ 🎉 พร้อมเปิดปฏิบัติการ!
```

---

## เอกสารที่เกี่ยวข้อง

- [แผนงานสร้าง SOC](SOC_Building_Roadmap.th.md)
- [เลือก Technology Stack](Technology_Stack.th.md)
- [คู่มือ Onboard Log](../06_Operations_Management/Log_Source_Onboarding.th.md)
