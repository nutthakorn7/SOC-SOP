#!/usr/bin/env python3
"""
export_pdf.py — Export SOC SOP documents as client-ready PDF or HTML

Usage:
    python3 tools/export_pdf.py                   # Export EN-only HTML (all sections)
    python3 tools/export_pdf.py --lang th          # Export TH-only
    python3 tools/export_pdf.py --lang both        # Export combined EN+TH
    python3 tools/export_pdf.py --section ir       # Export only Incident Response
    python3 tools/export_pdf.py --format pdf       # Export as PDF (requires wkhtmltopdf or browser)

Output goes to: exports/SOC_SOP_Manual_<lang>.html (or .pdf)
Then open in browser & Print → Save as PDF for best results.
"""

import os
import sys
import argparse
import subprocess
import datetime

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXPORT_DIR = os.path.join(ROOT_DIR, "exports")

# Logical section ordering
SECTIONS = [
    {"key": "getting_started", "dir": "00_Getting_Started", "title": "Getting Started", "title_th": "เริ่มต้นใช้งาน"},
    {"key": "fundamentals",    "dir": "01_SOC_Fundamentals", "title": "SOC Fundamentals", "title_th": "พื้นฐาน SOC"},
    {"key": "onboarding",      "dir": "01_Onboarding", "title": "System Onboarding", "title_th": "การเปิดใช้งานระบบ"},
    {"key": "platform",        "dir": "02_Platform_Operations", "title": "Platform Operations", "title_th": "การดำเนินงานแพลตฟอร์ม"},
    {"key": "guides",          "dir": "03_User_Guides", "title": "User Guides", "title_th": "คู่มือผู้ใช้"},
    {"key": "troubleshooting", "dir": "04_Troubleshooting", "title": "Troubleshooting", "title_th": "การแก้ไขปัญหา"},
    {"key": "ir",              "dir": "05_Incident_Response", "title": "Incident Response", "title_th": "การตอบสนองต่อเหตุการณ์"},
    {"key": "operations",      "dir": "06_Operations_Management", "title": "Operations Management", "title_th": "การจัดการปฏิบัติงาน"},
    {"key": "detection",       "dir": "07_Detection_Rules", "title": "Detection Rules", "title_th": "กฎการตรวจจับ"},
    {"key": "simulation",      "dir": "08_Simulation_Testing", "title": "Simulation & Testing", "title_th": "การจำลองและทดสอบ"},
    {"key": "training",        "dir": "09_Training_Onboarding", "title": "Training & Onboarding", "title_th": "การฝึกอบรม"},
    {"key": "compliance",      "dir": "10_Compliance", "title": "Compliance", "title_th": "การปฏิบัติตามกฎหมาย"},
    {"key": "signatures",      "dir": "10_File_Signatures", "title": "File Signatures (YARA)", "title_th": "ลายเซ็นไฟล์ (YARA)"},
    {"key": "reporting",       "dir": "11_Reporting_Templates", "title": "Reporting Templates", "title_th": "แม่แบบรายงาน"},
    {"key": "templates",       "dir": "templates", "title": "Forms & Templates", "title_th": "แบบฟอร์ม"},
]

EXCLUDE_FILES = {"README.md", "README.th.md"}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap');

:root {
    --primary: #1a56db;
    --primary-light: #e1effe;
    --bg: #ffffff;
    --text: #1f2937;
    --text-muted: #6b7280;
    --border: #e5e7eb;
    --code-bg: #f3f4f6;
    --accent: #059669;
}

* { box-sizing: border-box; }

body {
    font-family: 'Inter', 'Noto Sans Thai', -apple-system, sans-serif;
    color: var(--text);
    line-height: 1.7;
    max-width: 210mm;
    margin: 0 auto;
    padding: 20mm 15mm;
    font-size: 11pt;
    background: var(--bg);
}

/* Cover Page */
.cover-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 90vh;
    text-align: center;
    page-break-after: always;
}
.cover-page h1 {
    font-size: 32pt;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.cover-page .subtitle {
    font-size: 14pt;
    color: var(--text-muted);
    margin-bottom: 40px;
}
.cover-page .meta {
    font-size: 10pt;
    color: var(--text-muted);
    border-top: 2px solid var(--primary);
    padding-top: 20px;
    margin-top: 40px;
}
.cover-page .badge {
    display: inline-block;
    background: var(--primary-light);
    color: var(--primary);
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 10pt;
    font-weight: 500;
    margin: 4px;
}
.cover-page .shield {
    font-size: 72pt;
    margin-bottom: 20px;
}

/* Headings */
h1 { font-size: 20pt; color: var(--primary); border-bottom: 2px solid var(--primary); padding-bottom: 6px; margin-top: 30px; }
h2 { font-size: 16pt; color: #374151; margin-top: 24px; }
h3 { font-size: 13pt; color: #4b5563; margin-top: 18px; }
h4 { font-size: 11pt; font-weight: 600; }

/* Section divider */
.section-divider {
    page-break-before: always;
    background: linear-gradient(135deg, var(--primary), #7c3aed);
    color: white;
    padding: 40px 30px;
    border-radius: 8px;
    margin: 40px 0 30px 0;
}
.section-divider h1 {
    color: white;
    border: none;
    font-size: 24pt;
    margin: 0;
    padding: 0;
}
.section-divider p {
    color: rgba(255,255,255,0.8);
    margin: 8px 0 0 0;
    font-size: 12pt;
}

/* Tables */
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 10pt; }
th { background: var(--primary); color: white; padding: 8px 12px; text-align: left; font-weight: 600; }
td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
tr:nth-child(even) { background: #f9fafb; }

/* Code */
code { background: var(--code-bg); padding: 2px 6px; border-radius: 4px; font-size: 9.5pt; font-family: 'SF Mono', 'Menlo', monospace; }
pre { background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 9pt; }
pre code { background: none; padding: 0; color: inherit; }

/* Blockquotes */
blockquote { border-left: 4px solid var(--primary); background: var(--primary-light); padding: 12px 16px; margin: 16px 0; border-radius: 0 6px 6px 0; }
blockquote p { margin: 0; }

/* Lists */
ul, ol { margin: 8px 0; padding-left: 24px; }
li { margin: 4px 0; }

/* Mermaid placeholder */
.mermaid-placeholder {
    background: var(--code-bg);
    border: 1px dashed var(--border);
    padding: 16px;
    border-radius: 8px;
    text-align: center;
    color: var(--text-muted);
    font-style: italic;
    margin: 16px 0;
}

/* Print */
@media print {
    body { padding: 0; max-width: 100%; }
    .section-divider { break-before: page; }
    pre { white-space: pre-wrap; word-wrap: break-word; }
    a { color: var(--primary); text-decoration: none; }
    a[href]::after { content: none; }
}

/* Checkboxes */
li input[type="checkbox"] { margin-right: 6px; }

/* Horizontal rules */
hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

/* Footer per page */
.doc-separator {
    border-top: 2px solid var(--primary-light);
    margin: 30px 0;
    padding-top: 10px;
}
"""


def get_files_for_section(section_dir, lang):
    """Get markdown files for a section filtered by language."""
    full_path = os.path.join(ROOT_DIR, section_dir)
    if not os.path.isdir(full_path):
        return []

    files = []
    for root, dirs, filenames in os.walk(full_path):
        dirs.sort()
        for fn in sorted(filenames):
            if fn in EXCLUDE_FILES:
                continue
            if not fn.endswith(".md"):
                continue

            # Language filter
            if lang == "en" and fn.endswith(".th.md"):
                continue
            elif lang == "th" and fn.endswith(".en.md"):
                continue
            elif lang == "en" and not fn.endswith(".en.md"):
                # Include non-language-specific .md files (like sigma rules READMEs)
                # but skip .th.md
                if fn.endswith(".th.md"):
                    continue

            files.append(os.path.join(root, fn))

    return files


def md_to_html_content(md_path):
    """Convert a single markdown file to HTML using pandoc."""
    try:
        result = subprocess.run(
            ["pandoc", "--from=gfm", "--to=html5", md_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            # Replace mermaid code blocks with placeholder
            html = result.stdout
            html = html.replace('<code class="language-mermaid">', '<code class="mermaid-code">')
            return html
        else:
            return f"<p><em>Error converting {md_path}: {result.stderr}</em></p>"
    except Exception as e:
        return f"<p><em>Error: {e}</em></p>"


def build_toc(sections_with_files):
    """Build a table of contents."""
    toc = '<div class="toc" style="page-break-after:always;">\n'
    toc += '<h1 style="text-align:center; border:none;">📑 Table of Contents</h1>\n'
    toc += '<table style="width:100%; font-size:11pt;">\n'
    toc += '<tr><th>#</th><th>Section</th><th>Documents</th></tr>\n'

    for i, (section, files) in enumerate(sections_with_files, 1):
        title = section["title"]
        count = len(files)
        if count > 0:
            toc += f'<tr><td style="width:40px;text-align:center;">{i}</td>'
            toc += f'<td><strong>{title}</strong></td>'
            toc += f'<td style="text-align:center;">{count}</td></tr>\n'

    toc += '</table>\n</div>\n'
    return toc


def build_html(sections_with_files, lang, company="[COMPANY]"):
    """Build the complete HTML document."""
    now = datetime.datetime.now().strftime("%B %d, %Y")
    lang_label = {"en": "English", "th": "ภาษาไทย", "both": "EN/TH Bilingual"}[lang]

    total_docs = sum(len(f) for _, f in sections_with_files)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SOC Standard Operating Procedures</title>
<style>{CSS}</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover-page">
    <div class="shield">🛡️</div>
    <h1>SOC Standard Operating Procedures</h1>
    <div class="subtitle">ระเบียบปฏิบัติมาตรฐานสำหรับศูนย์ปฏิบัติการความปลอดภัย</div>
    <div>
        <span class="badge">📄 {total_docs} Documents</span>
        <span class="badge">🌐 {lang_label}</span>
        <span class="badge">🔍 NIST / MITRE ATT&CK</span>
    </div>
    <div class="meta">
        <strong>Prepared for:</strong> {company}<br>
        <strong>Date:</strong> {now}<br>
        <strong>Version:</strong> 1.0<br>
        <strong>Classification:</strong> Confidential
    </div>
</div>

"""

    # Table of Contents
    html += build_toc(sections_with_files)

    # Content
    for section, files in sections_with_files:
        if not files:
            continue

        title = section["title"]
        title_th = section.get("title_th", "")

        html += f"""
<div class="section-divider">
    <h1>{title}</h1>
    <p>{title_th}</p>
</div>
"""

        for filepath in files:
            relpath = os.path.relpath(filepath, ROOT_DIR)
            basename = os.path.basename(filepath)
            content = md_to_html_content(filepath)

            html += f'<div class="doc-separator">\n'
            html += f'<p style="color:var(--text-muted);font-size:9pt;">📄 {relpath}</p>\n'
            html += content
            html += '</div>\n'

    # Footer
    html += f"""
<div style="text-align:center; margin-top:60px; padding-top:20px; border-top:2px solid var(--primary); color:var(--text-muted); font-size:9pt;">
    <p><strong>SOC Standard Operating Procedures</strong><br>
    Generated on {now} | cyberdefense.co.th<br>
    This document is confidential and intended for authorized personnel only.</p>
</div>

</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(description="Export SOC SOPs as client-ready PDF/HTML")
    parser.add_argument("--lang", choices=["en", "th", "both"], default="en",
                        help="Language: en (English only), th (Thai only), both (combined)")
    parser.add_argument("--section", default="all",
                        help="Section key to export (e.g., 'ir', 'operations', 'all')")
    parser.add_argument("--company", default="[COMPANY]",
                        help="Client company name for cover page")
    args = parser.parse_args()

    os.makedirs(EXPORT_DIR, exist_ok=True)

    # Filter sections
    sections_to_export = SECTIONS
    if args.section != "all":
        sections_to_export = [s for s in SECTIONS if s["key"] == args.section]
        if not sections_to_export:
            valid = ", ".join(s["key"] for s in SECTIONS)
            print(f"❌ Unknown section '{args.section}'. Valid: {valid}")
            sys.exit(1)

    # Collect files
    sections_with_files = []
    for section in sections_to_export:
        files = get_files_for_section(section["dir"], args.lang)
        sections_with_files.append((section, files))

    total = sum(len(f) for _, f in sections_with_files)
    print(f"📄 Found {total} documents ({args.lang})")

    if total == 0:
        print("❌ No documents found!")
        sys.exit(1)

    # Build HTML
    print("🔨 Building HTML...")
    html_content = build_html(sections_with_files, args.lang, args.company)

    # Write output
    suffix = args.section if args.section != "all" else args.lang
    output_file = os.path.join(EXPORT_DIR, f"SOC_SOP_Manual_{suffix}.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Exported to: {output_file}")
    print(f"")
    print(f"📖 To create PDF:")
    print(f"   1. Open the HTML file in your browser")
    print(f"   2. Press Cmd+P (Print)")
    print(f"   3. Select 'Save as PDF'")
    print(f"   4. Set margins to 'Default' or 'Minimum'")
    print(f"")
    print(f"   Or use: open {output_file}")


if __name__ == "__main__":
    if os.path.dirname(__file__):
        os.chdir(os.path.dirname(__file__))
    main()
