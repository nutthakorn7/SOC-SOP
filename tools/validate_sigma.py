#!/usr/bin/env python3
import os
import yaml
import sys

RULES_DIR = "../08_Detection_Engineering"

def validate_rules():
    print(f"Validating Sigma Rules in {RULES_DIR}...")
    errors = []
    
    if not os.path.exists(RULES_DIR):
        print(f"Directory {RULES_DIR} not found.")
        sys.exit(1)

    for root, _, files in os.walk(RULES_DIR):
        for file in files:
            if file.endswith((".yml", ".yaml")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = yaml.safe_load(f)
                        
                        # Basic Schema Check
                        required_fields = ['title', 'logsource', 'detection']
                        missing = [field for field in required_fields if field not in content]
                        
                        if missing:
                            errors.append(f"{file}: Missing root fields {missing}")
                        
                        # Check for condition (can be in root or inside detection)
                        has_condition = 'condition' in content or ('detection' in content and 'condition' in content['detection'])
                        if not has_condition:
                             errors.append(f"{file}: Missing 'condition' field")
                            
                except yaml.YAMLError as e:
                    errors.append(f"{file}: Invalid YAML - {e}")
                except Exception as e:
                    errors.append(f"{file}: Error - {e}")

    if errors:
        print("❌ Validation Failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("✅ All Sigma Rules match basic schema.")

if __name__ == "__main__":
    if os.path.dirname(__file__):
        os.chdir(os.path.dirname(__file__))
    validate_rules()
