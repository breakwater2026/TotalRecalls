#!/usr/bin/env python3
"""Convert markdown user guides to professionally styled .docx files."""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

def set_cell_background(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def md_to_docx(md_path, docx_path, title_main):
    doc = docx.Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
    lines = open(md_path, "r", encoding="utf-8").readlines()
    
    in_code = False
    code_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\r\n")
        
        if line.startswith("```"):
            if in_code:
                # Flush code block
                table = doc.add_table(rows=1, cols=1)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell = table.cell(0, 0)
                set_cell_background(cell, "F4F4F5")
                set_cell_margins(cell, top=120, bottom=120, left=200, right=200)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run("\n".join(code_lines))
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0x27, 0x27, 0x2A)
                in_code = False
                code_lines = []
            else:
                in_code = True
                code_lines = []
            i += 1
            continue
            
        if in_code:
            code_lines.append(line)
            i += 1
            continue
            
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
            
        # Callout block
        if stripped.startswith(">"):
            callout_text = stripped.lstrip("> ").strip()
            table = doc.add_table(rows=1, cols=1)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = table.cell(0, 0)
            set_cell_background(cell, "FEF3C7") # Warm amber background
            set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(callout_text.replace("**", ""))
            run.font.name = "Segoe UI"
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x92, 0x40, 0x0E)
            i += 1
            continue

        # Headers
        if line.startswith("# "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(line[2:].strip())
            run.font.name = "Segoe UI"
            run.font.size = Pt(22)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x18, 0x18, 0x1B)
        elif line.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(line[3:].strip())
            run.font.name = "Segoe UI"
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xB4, 0x54, 0x3A)
        elif line.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(line[4:].strip())
            run.font.name = "Segoe UI"
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x27, 0x27, 0x2A)
        elif line.startswith("---"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run("____________________________________________________________________")
            run.font.color.rgb = RGBColor(0xE4, 0xE4, 0xE7)
            run.font.size = Pt(8)
        elif line.startswith("* ") or line.startswith("- "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            text = line[2:].strip()
            # Clean bold markers
            parts = text.split("**")
            for idx, part in enumerate(parts):
                run = p.add_run(part)
                run.font.name = "Segoe UI"
                run.font.size = Pt(10)
                if idx % 2 == 1:
                    run.font.bold = True
        elif line[0].isdigit() and line[1:3] in (". ", ") "):
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            text = line[3:].strip()
            parts = text.split("**")
            for idx, part in enumerate(parts):
                run = p.add_run(part)
                run.font.name = "Segoe UI"
                run.font.size = Pt(10)
                if idx % 2 == 1:
                    run.font.bold = True
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            parts = line.split("**")
            for idx, part in enumerate(parts):
                run = p.add_run(part)
                run.font.name = "Segoe UI"
                run.font.size = Pt(10)
                if idx % 2 == 1:
                    run.font.bold = True
                    
        i += 1
        
    doc.save(docx_path)
    print(f"Generated {docx_path} ({os.path.getsize(docx_path):,} bytes)")

def main():
    qs_md = os.path.join(DOCS_DIR, "TOTALRECALLS_SSE_QUICK_START_GUIDE.md")
    qs_docx = os.path.join(DOCS_DIR, "TOTALRECALLS_SSE_QUICK_START_GUIDE.docx")
    md_to_docx(qs_md, qs_docx, "TotalRecalls Smart Search Engine (SSE) — Quick-Start Guide")
    
    pu_md = os.path.join(DOCS_DIR, "TOTALRECALLS_POWER_USER_MANUAL.md")
    pu_docx = os.path.join(DOCS_DIR, "TOTALRECALLS_POWER_USER_MANUAL.docx")
    md_to_docx(pu_md, pu_docx, "TOTALRECALLS POWER USER MANUAL")

if __name__ == "__main__":
    main()
