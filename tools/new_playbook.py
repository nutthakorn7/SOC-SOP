#!/usr/bin/env python3
import os
import datetime

TEMPLATE = """# Playbook: {title}

**Severity**: {severity} | **Category**: {category}

## 1. Analysis (Triage)
-   **Trigger**: What caused this alert?
-   **Validation**: How to confirm it's true positive?

## 2. Containment
-   **Immediate Action**: Steps to stop the threat.

## 3. Remediation
-   **Clean up**: Steps to remove the threat.

## 4. Recovery
-   **Restore**: Steps to bring systems back online.
"""

def create_playbook():
    print("--- New Playbook Wizard ---")
    title = input("Playbook Title (e.g., SQL Injection): ").strip()
    filename = title.replace(" ", "_") + ".md"
    severity = input("Severity (Low/Medium/High/Critical): ").strip()
    category = input("Category (Network/Identity/Endpoint/Cloud): ").strip()
    
    # English Version
    output_dir = "../05_Incident_Response/Playbooks"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filepath_en = os.path.join(output_dir, filename.replace(".md", ".en.md"))
    
    with open(filepath_en, "w") as f:
        f.write(TEMPLATE.format(title=title, severity=severity, category=category))
        
    print(f"✅ Created: {filepath_en}")
    print("You can now open this file and fill in the details.")

if __name__ == "__main__":
    if os.path.dirname(__file__):
        os.chdir(os.path.dirname(__file__))
    create_playbook()
