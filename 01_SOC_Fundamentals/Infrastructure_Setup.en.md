# SOC Infrastructure Setup Guide — Hands-On Installation

> **Document ID:** INFRA-001  
> **Version:** 1.0  
> **Last Updated:** 2026-02-15  
> **Prerequisite:** Read [Technology Stack Guide](Technology_Stack.en.md) to choose your stack

---

## This Guide Covers

Step-by-step installation of the **Open-Source Stack (Stack A)** using Wazuh. This is the recommended starting point for beginners — zero cost, full functionality.

> If you chose Microsoft Sentinel (Stack B), skip to [Sentinel Quick Setup](#sentinel-quick-setup).

---

## Part 1: Wazuh All-in-One Installation

### Requirements

| Item | Minimum | Recommended |
|:---|:---|:---|
| OS | Ubuntu 22.04 LTS / CentOS 8 | Ubuntu 22.04 LTS |
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disk | 50 GB | 200 GB+ (depends on log volume) |
| Network | Static IP, port 1514/1515/443 open | Dedicated VLAN |

### Step 1: Install Wazuh (Single-Node)

```bash
# Download and run Wazuh installer (automated)
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.9/config.yml

# Edit config.yml — set your server IP
cat > config.yml << 'EOF'
nodes:
  indexer:
    - name: wazuh-indexer
      ip: "YOUR_SERVER_IP"
  server:
    - name: wazuh-server
      ip: "YOUR_SERVER_IP"
  dashboard:
    - name: wazuh-dashboard
      ip: "YOUR_SERVER_IP"
EOF

# Run installer (takes 5-10 minutes)
sudo bash wazuh-install.sh -a

# ⚠️ SAVE the admin password printed at the end!
# Access dashboard: https://YOUR_SERVER_IP
# Username: admin
# Password: (shown in output)
```

### Step 2: Verify Installation

```bash
# Check all services running
sudo systemctl status wazuh-manager
sudo systemctl status wazuh-indexer
sudo systemctl status wazuh-dashboard

# Check Wazuh API
curl -k -u admin:PASSWORD https://localhost:55000/?pretty

# Open browser → https://YOUR_SERVER_IP
# Login → You should see the Wazuh dashboard
```

### Step 3: Deploy Agents on Endpoints

#### Windows Agent
```powershell
# Download from Wazuh dashboard → Agents → Deploy new agent
# Or use PowerShell:
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.0-1.msi -OutFile wazuh-agent.msi

# Install with server address
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="YOUR_SERVER_IP" WAZUH_AGENT_GROUP="default"

# Start service
net start WazuhSvc
```

#### Linux Agent
```bash
# Ubuntu/Debian
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo gpg --dearmor -o /usr/share/keyrings/wazuh.gpg
echo "deb [signed-by=/usr/share/keyrings/wazuh.gpg] https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list
sudo apt update && sudo apt install wazuh-agent -y

# Configure manager address
sudo sed -i 's/MANAGER_IP/YOUR_SERVER_IP/' /var/ossec/etc/ossec.conf

# Start agent
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

### Step 4: Verify Agents Connected

```bash
# On Wazuh server — list connected agents
sudo /var/ossec/bin/agent_control -l

# Expected output:
# ID: 001, Name: web-server-01, Status: Active
# ID: 002, Name: dc-01, Status: Active
```

---

## Part 2: Configure Log Sources

### Active Directory Logs → Wazuh

On each Domain Controller, configure the Wazuh agent:

```xml
<!-- Add to agent ossec.conf on DC -->
<ossec_config>
  <localfile>
    <location>Security</location>
    <log_format>eventchannel</log_format>
    <query>Event/System[EventID=4624 or EventID=4625 or EventID=4648 or
           EventID=4672 or EventID=4688 or EventID=4720 or EventID=4726 or
           EventID=4732 or EventID=4756 or EventID=1102]</query>
  </localfile>
  <localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
  </localfile>
</ossec_config>
```

### Firewall (Syslog) → Wazuh

```xml
<!-- Add to Wazuh server ossec.conf -->
<ossec_config>
  <remote>
    <connection>syslog</connection>
    <port>514</port>
    <protocol>udp</protocol>
    <allowed-ips>FIREWALL_IP</allowed-ips>
  </remote>
</ossec_config>
```

On your firewall, configure syslog output to `WAZUH_SERVER_IP:514`.

### Linux Servers → Wazuh

```xml
<!-- Auto-monitored on agent install, but add custom logs: -->
<ossec_config>
  <localfile>
    <location>/var/log/auth.log</location>
    <log_format>syslog</log_format>
  </localfile>
  <localfile>
    <location>/var/log/nginx/access.log</location>
    <log_format>syslog</log_format>
  </localfile>
</ossec_config>
```

---

## Part 3: Install Sysmon (Windows Enhanced Logging)

Sysmon dramatically improves Windows detection capability:

```powershell
# Download Sysmon
Invoke-WebRequest -Uri https://download.sysinternals.com/files/Sysmon.zip -OutFile Sysmon.zip
Expand-Archive Sysmon.zip

# Download recommended config (SwiftOnSecurity)
Invoke-WebRequest -Uri https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml -OutFile sysmonconfig.xml

# Install Sysmon with config
.\Sysmon64.exe -accepteula -i sysmonconfig.xml

# Verify
Get-Service Sysmon64
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 5
```

---

## Part 4: Import Sigma Rules into Wazuh

```bash
# Wazuh uses its own rule format, but you can create custom rules
# based on Sigma detection logic

# Example: Create a brute force detection rule
sudo cat >> /var/ossec/etc/rules/local_rules.xml << 'EOF'
<group name="authentication_failures,">
  <rule id="100001" level="10" frequency="10" timeframe="300">
    <if_matched_sid>60122</if_matched_sid>
    <description>SOC: Brute force - 10+ login failures in 5 min (PB-04)</description>
    <mitre>
      <id>T1110</id>
    </mitre>
    <group>attack,brute_force,PB-04</group>
  </rule>
</group>
EOF

# Restart to apply
sudo systemctl restart wazuh-manager

# Validate rules
sudo /var/ossec/bin/wazuh-logtest
```

---

## Part 5: Set Up Alert Notifications

### Email Alerts

```xml
<!-- Add to Wazuh server ossec.conf -->
<ossec_config>
  <global>
    <email_notification>yes</email_notification>
    <smtp_server>smtp.gmail.com</smtp_server>
    <email_from>soc-alerts@company.com</email_from>
    <email_to>soc-team@company.com</email_to>
    <email_maxperhour>100</email_maxperhour>
  </global>
  
  <email_alerts>
    <email_to>soc-team@company.com</email_to>
    <level>10</level>
  </email_alerts>
</ossec_config>
```

### Slack Integration

```bash
# Create a Wazuh integration script for Slack
sudo cat > /var/ossec/integrations/custom-slack.py << 'PYEOF'
#!/usr/bin/env python3
import sys, json, requests

SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

def main():
    alert_file = open(sys.argv[1])
    alert = json.load(alert_file)
    
    msg = {
        "text": f"🚨 *SOC Alert (Level {alert['rule']['level']})*\n"
                f"Rule: {alert['rule']['description']}\n"
                f"Agent: {alert.get('agent', {}).get('name', 'N/A')}\n"
                f"Time: {alert['timestamp']}"
    }
    requests.post(SLACK_WEBHOOK, json=msg)

if __name__ == "__main__":
    main()
PYEOF

chmod 750 /var/ossec/integrations/custom-slack.py
chown root:wazuh /var/ossec/integrations/custom-slack.py
```

---

## Part 6: TheHive Installation (Ticketing)

```bash
# Install prerequisites
sudo apt install -y openjdk-11-jre-headless

# Add TheHive repository
wget -qO- https://raw.githubusercontent.com/StrangeBeeCorp/Security/main/PGP%20keys/packages.key | sudo gpg --dearmor -o /usr/share/keyrings/strangebee-archive-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/strangebee-archive-keyring.gpg] https://deb.strangebee.com thehive-5.x main' | sudo tee /etc/apt/sources.list.d/strangebee.list

sudo apt update && sudo apt install -y thehive

# Start TheHive
sudo systemctl enable thehive
sudo systemctl start thehive

# Access: http://YOUR_SERVER_IP:9000
# Default login: admin@thehive.local / secret
# ⚠️ CHANGE PASSWORD IMMEDIATELY
```

---

## Sentinel Quick Setup

If you chose **Stack B (Microsoft)**:

```
Step 1: Azure Portal → Create resource → Microsoft Sentinel
Step 2: Create Log Analytics Workspace
Step 3: Add Sentinel to workspace
Step 4: Data connectors → Enable:
        ✅ Microsoft 365 Defender
        ✅ Azure Active Directory
        ✅ Azure Activity
        ✅ Microsoft Defender for Cloud
Step 5: Analytics → Rule templates → Enable recommended rules
Step 6: Done! You have a SIEM.
```

> Time estimate: **30 minutes** if you have Azure admin access.

---

## Verification Checklist

After setup, verify everything works:

```
□ Wazuh dashboard accessible at https://SERVER_IP
□ At least 3 agents connected and active
□ Events visible in dashboard (real-time)
□ AD login events appearing (Event ID 4624/4625)
□ Firewall logs arriving via syslog
□ Sysmon installed on Windows endpoints
□ Custom brute-force rule triggers on test
□ Email/Slack alerts received
□ TheHive accessible and login works
□ Take a screenshot and celebrate! 🎉
```

---

## Troubleshooting

| Problem | Solution |
|:---|:---|
| Agent can't connect | Check firewall: port 1514/1515 open? |
| No data in dashboard | Wait 5 min, then check agent status |
| Syslog not arriving | Check `tcpdump -i any port 514` on Wazuh server |
| High disk usage | Reduce log retention or add disk |
| Dashboard slow | Increase indexer RAM to 16 GB |
| Agent shows "Disconnected" | Restart agent: `systemctl restart wazuh-agent` |

---

## Related Documents

- [SOC Building Roadmap](SOC_Building_Roadmap.en.md)
- [Technology Stack Guide](Technology_Stack.en.md)
- [Log Source Onboarding](../06_Operations_Management/Log_Source_Onboarding.en.md)
- [Detection Rules Index](../07_Detection_Rules/README.md)
