# Automation Tools & Workflows / เครื่องมือและขั้นตอนอัตโนมัติ

This directory contains utility scripts to help maintain the SOC repository. These tools are automatically run by GitHub Actions but can also be run locally.
โฟลเดอร์นี้เก็บสคริปต์ช่วยงานต่างๆ ซึ่งจะถูกรันอัตโนมัติโดย GitHub Actions หรือสามารถรันเองในเครื่องก็ได้

## 1. Sigma Rule Validation (`validate_sigma.py`)
**Workflow**: 
1.  **Trigger**: Runs automatically on every `git push` or `pull request` to `main`.
2.  **Action**: Scans all `.yml` files in `07_Detection_Rules/`.
3.  **Check**: Verifies that every rule has required fields (`title`, `logsource`, `detection`, `condition`).
4.  **Output**: Fails the build if any rule is invalid.

**Run Locally**:
```bash
python3 tools/validate_sigma.py
```

## 2. Broken Link Checker (`check_links.py`)
**Workflow**:
1.  **Trigger**: Runs automatically on every `git push`.
2.  **Action**: Scans all `.md` files in the repository.
3.  **Check**: Finds all `[Link](path)` references and verifies that the target file exists.
4.  **Output**: Fails the build if any link is broken.

**Run Locally**:
```bash
python3 tools/check_links.py
```

## 3. New Playbook Wizard (`new_playbook.py`)
**Workflow**:
1.  **Trigger**: Manual execution by an Analyst/Engineer.
2.  **Action**: Asks for `Title`, `Severity`, and `Category`.
3.  **Output**: Generates a new `.md` file in `05_Incident_Response/Playbooks/` with the standard template pre-filled.

**Run Locally**:
```bash
python3 tools/new_playbook.py
```

## 4. Documentation Site Deployment (`deploy_docs.yml`)
**Workflow**:
1.  **Trigger**: Runs when changes are pushed to `main`.
2.  **Action**:
    -   Installs `mkdocs-material`.
    -   Builds the static website from `mkdocs.yml`.
    -   Deploys the site to the `gh-pages` branch.
3.  **Result**: The website is updated live.
