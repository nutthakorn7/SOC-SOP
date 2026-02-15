# SOC Technology Stack Selection Guide

> **Document ID:** TECH-001  
> **Version:** 1.0  
> **Last Updated:** 2026-02-15  
> **Prerequisite:** Read [SOC Building Roadmap](SOC_Building_Roadmap.en.md) first

---

## Decision Framework

Choose technology based on **3 factors**:

```
                    ┌─────────────┐
                    │   Budget    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴─────┐ ┌───┴───┐ ┌─────┴─────┐
        │  ฿ Free   │ │ ฿฿ Mid│ │ ฿฿฿ High  │
        │ Open-Src  │ │ Mixed │ │ Enterprise│
        └───────────┘ └───────┘ └───────────┘

    ×   Existing Infrastructure (Azure? AWS? On-prem?)
    ×   Team Skill Level (Beginner? Expert?)
    =   Your Stack
```

---

## Stack A: Full Open-Source (฿0 Licensing)

**Best for:** Startups, small teams, learning, budget-conscious orgs

| Layer | Tool | Notes |
|:---|:---|:---|
| **SIEM** | Wazuh 4.x | All-in-one: SIEM + XDR + Compliance |
| **Endpoint** | Wazuh Agent | Built-in EDR, FIM, vulnerability scan |
| **Network IDS** | Suricata | High-performance, rule-based |
| **Network Metadata** | Zeek | Rich protocol analysis |
| **Threat Intel** | MISP + OpenCTI | TI platform + feeds |
| **Ticketing/IR** | TheHive + Cortex | IR case management + enrichment |
| **SOAR** | Shuffle | Drag-and-drop automation |
| **Vuln Scanner** | OpenVAS/Greenbone | Network vulnerability assessment |
| **Log Shipping** | Filebeat / rsyslog | Lightweight log forwarding |

### Architecture
```
Endpoints/Servers          Network              Cloud
  [Wazuh Agent] ──┐    [Suricata] ──┐     [CloudTrail] ──┐
  [Wazuh Agent] ──┤    [Zeek]     ──┤     [Flow Logs]  ──┤
  [Wazuh Agent] ──┤                 │                    │
                  ▼                 ▼                    ▼
            ┌─────────────────────────────────────────────┐
            │           Wazuh Manager + Indexer           │
            │         (Elasticsearch / OpenSearch)        │
            └──────────────────┬──────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Wazuh Dashboard     │ ← Analyst works here
                    │ TheHive (Tickets)   │
                    │ MISP (Threat Intel) │
                    │ Shuffle (SOAR)      │
                    └─────────────────────┘
```

### Server Requirements
| Component | CPU | RAM | Disk | VMs |
|:---|:---:|:---:|:---:|:---:|
| Wazuh Manager | 4 cores | 8 GB | 50 GB | 1 |
| Wazuh Indexer | 4 cores | 16 GB | 500 GB+ | 1–3 |
| Wazuh Dashboard | 2 cores | 4 GB | 20 GB | 1 |
| TheHive + Cortex | 4 cores | 8 GB | 100 GB | 1 |
| MISP | 2 cores | 4 GB | 50 GB | 1 |
| **Total (minimum)** | **16 cores** | **40 GB** | **720 GB** | **4–5** |

### Pros and Cons
| ✅ Pros | ❌ Cons |
|:---|:---|
| Zero license cost | Requires Linux admin skills |
| Full control over data | Manual updates and patching |
| Active community support | No vendor SLA / support |
| Customize anything | Integration requires effort |

---

## Stack B: Microsoft-Centric (Already have M365)

**Best for:** Organizations already using Microsoft 365 E3/E5 or Azure

| Layer | Tool | License |
|:---|:---|:---|
| **SIEM** | Microsoft Sentinel | Pay-per-GB ingestion |
| **Endpoint** | Microsoft Defender for Endpoint | M365 E5 or standalone |
| **Identity** | Entra ID Protection | M365 E5 |
| **Email** | Defender for Office 365 | M365 E5 |
| **Cloud** | Defender for Cloud | Per-resource pricing |
| **SOAR** | Sentinel Playbooks (Logic Apps) | Included with Sentinel |
| **Threat Intel** | Defender Threat Intelligence | Included |
| **Ticketing** | ServiceNow / Jira | Separate license |

### Architecture
```
   M365 Users          Azure VMs         On-prem Servers
   [Defender] ──┐    [Defender] ──┐    [AMA Agent] ──┐
   [Entra ID] ──┤    [NSG Logs] ──┤    [Syslog]    ──┤
                │                 │                   │
                ▼                 ▼                   ▼
           ┌──────────────────────────────────────────┐
           │         Microsoft Sentinel               │
           │      (Log Analytics Workspace)           │
           └───────────────────┬──────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Sentinel Workbooks  │
                    │ Analytics Rules     │
                    │ Playbooks (SOAR)    │
                    │ Hunting Queries     │
                    └─────────────────────┘
```

### Cost Estimate
| Component | Monthly Cost (500 users) |
|:---|:---|
| M365 E5 license (500 users) | ~฿1.5M/mo |
| Sentinel ingestion (50 GB/day) | ~฿150K/mo |
| Defender for Cloud | ~฿30K/mo |
| **Total** | **~฿1.7M/mo** |

> **Tip:** If you already have M365 E5, you already have Defender. Just enable Sentinel and connect the data sources — you could have a working SIEM in 1 day.

### Pros and Cons
| ✅ Pros | ❌ Cons |
|:---|:---|
| Native integration with M365 | Vendor lock-in |
| Fast to deploy | Costs scale with data volume |
| AI-powered detection (Copilot) | Complex pricing model |
| Strong identity protection | Limited multi-cloud support |

---

## Stack C: AWS-Centric

**Best for:** Organizations running primarily on AWS

| Layer | Tool | Notes |
|:---|:---|:---|
| **SIEM** | Amazon Security Lake + OpenSearch | Native AWS integration |
| **Endpoint** | CrowdStrike / SentinelOne | Third-party (AWS doesn't have EDR) |
| **Cloud Security** | GuardDuty | Threat detection for AWS |
| **Config** | AWS Config + Security Hub | Compliance and config monitoring |
| **Network** | VPC Flow Logs + Traffic Mirroring | Network visibility |
| **WAF** | AWS WAF | Web application firewall |
| **SOAR** | AWS Step Functions / Shuffle | Automation |

---

## Stack D: Elastic-Based (Flexible)

**Best for:** Multi-cloud, hybrid, or vendor-neutral preference

| Layer | Tool | Notes |
|:---|:---|:---|
| **SIEM** | Elastic Security (Free tier) | SIEM + Detection + Case management |
| **Endpoint** | Elastic Agent (Defend) | Built-in EDR |
| **Ingestion** | Elastic Agent / Beats | Hundreds of integrations |
| **SOAR** | n8n / Shuffle / Tines | Automation |
| **Threat Intel** | MISP + Elastic TI module | Feed integration |

### Architecture
```
  Endpoints         Cloud APIs        Network
  [Elastic Agent]   [AWS/Azure/GCP]   [Suricata/Zeek]
       │                 │                 │
       └────────────┬────┘─────────────────┘
                    ▼
         ┌──────────────────────┐
         │   Elasticsearch      │
         │   Kibana + Security  │
         │   Fleet Server       │
         └──────────┬───────────┘
                    │
             ┌──────┴──────┐
             │  Detection  │
             │  Rules      │
             │  Cases      │
             │  Timeline   │
             └─────────────┘
```

---

## Comparison Matrix

| Feature | Stack A (Open) | Stack B (MS) | Stack C (AWS) | Stack D (Elastic) |
|:---|:---:|:---:|:---:|:---:|
| License cost | ฿0 | ฿฿฿ | ฿฿ | ฿ (Free tier) |
| Setup difficulty | 🔴 Hard | 🟢 Easy | 🟡 Medium | 🟡 Medium |
| Time to value | 2–4 weeks | 1–3 days | 1–2 weeks | 1–2 weeks |
| Endpoint coverage | ✅ | ✅ | ⚠️ (need 3rd party) | ✅ |
| Cloud coverage | ⚠️ | ✅ Azure | ✅ AWS | ✅ Multi-cloud |
| SOAR built-in | ⚠️ (Shuffle) | ✅ | ⚠️ | ⚠️ |
| Community size | Large | Very large | Large | Very large |
| Vendor lock-in | None | High | High | Low |
| Sigma rule support | ✅ | ✅ (via KQL) | ⚠️ | ✅ |
| Best for | Learning, budget | M365 shops | AWS-heavy | Flexible orgs |

---

## Decision Tree

```
START
  │
  ├─ Already have Microsoft 365 E5?
  │   ├─ YES → Stack B (Microsoft)
  │   └─ NO ──┐
  │            │
  │   ├─ Primarily on AWS?
  │   │   ├─ YES → Stack C (AWS)
  │   │   └─ NO ──┐
  │   │            │
  │   │   ├─ Budget > ฿5M/year?
  │   │   │   ├─ YES → Stack D (Elastic)
  │   │   │   └─ NO → Stack A (Open-Source)
```

---

## Essential Add-Ons (Any Stack)

Regardless of which stack you choose, add these:

| Category | Recommendation | Why |
|:---|:---|:---|
| **Password Manager** | Bitwarden (team) | SOC handles many credentials |
| **Documentation** | MkDocs / Confluence | SOPs and runbooks (this repo!) |
| **Communication** | Slack / Teams + dedicated channels | Incident war rooms |
| **VPN** | WireGuard / existing enterprise VPN | Remote SOC access |
| **MFA** | Duo / Microsoft Authenticator | Protect SOC accounts |
| **Backup** | Veeam / Restic / AWS Backup | Evidence preservation |

---

## Related Documents

- [SOC Building Roadmap](SOC_Building_Roadmap.en.md)
- [Infrastructure Setup Guide](Infrastructure_Setup.en.md)
- [Log Source Onboarding](../06_Operations_Management/Log_Source_Onboarding.en.md)
