"""Build an ATS-safe DOCX resume for Duke Morgan.

ATS rules honoured here: no tables, no text boxes, no columns, no images,
no header/footer content, standard section headings, plain bullet lists,
and a common font. Everything is linear body text so a parser reads it
top-to-bottom in the right order.
"""

from pathlib import Path
import shutil
import subprocess
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ACCENT = RGBColor(0x0F, 0x3D, 0x56)   # deep slate blue
BODY = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x44, 0x4A, 0x50)

FONT = "Calibri"


def set_margins(doc, inches=0.45):
    for s in doc.sections:
        s.top_margin = Inches(inches)
        s.bottom_margin = Inches(inches)
        s.left_margin = Inches(inches + 0.05)
        s.right_margin = Inches(inches + 0.05)


def style_base(doc):
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(10)
    st.font.color.rgb = BODY
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    pf = st.paragraph_format
    pf.space_after = Pt(3)
    pf.space_before = Pt(0)
    pf.line_spacing = 1.0


def para(doc, text="", size=10, bold=False, italic=False, color=BODY,
         align=None, space_before=0, space_after=3, caps=False):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        r.font.color.rgb = color
        r.font.name = FONT
        if caps:
            r.font.all_caps = True
    return p


def rich(doc, parts, size=10, space_before=0, space_after=3, align=None):
    """parts = [(text, bold, italic, color), ...]"""
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    for text, bold, italic, color in parts:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        r.font.color.rgb = color
        r.font.name = FONT
    return p


def bottom_rule(p, color="0F3D56", size=6):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), color)
    bdr.append(bottom)
    pPr.append(bdr)


def section(doc, title):
    p = para(doc, title, size=10.5, bold=True, color=ACCENT,
             space_before=6, space_after=3, caps=True)
    for r in p.runs:
        r.font.spacing = Pt(1)
    bottom_rule(p)
    return p


def bullet(doc, text, size=9.5):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.name = FONT
    r.font.color.rgb = BODY
    return p


def lead_bullet(doc, lead, text, size=9.5):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.line_spacing = 1.0
    r1 = p.add_run(lead)
    r1.bold = True
    r1.font.size = Pt(size)
    r1.font.name = FONT
    r1.font.color.rgb = ACCENT
    r2 = p.add_run(text)
    r2.font.size = Pt(size)
    r2.font.name = FONT
    r2.font.color.rgb = BODY
    return p


def role(doc, title, org, meta):
    rich(doc, [(title, True, False, BODY)], size=10.5,
         space_before=5, space_after=0)
    rich(doc, [(org, True, False, ACCENT), ("  |  ", False, False, MUTED),
               (meta, False, False, MUTED)], size=9.5, space_after=2.5)


def build():
    doc = Document()
    set_margins(doc)
    style_base(doc)

    # ---- Header -------------------------------------------------------
    p = para(doc, "DUKE MORGAN, RN, BSHA", size=21, bold=True, color=ACCENT,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    for r in p.runs:
        r.font.spacing = Pt(1.2)

    para(doc, "Director of Clinical Systems  |  Healthcare Technology and AI",
         size=10.5, bold=True, color=MUTED,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)

    p = para(doc,
             "Nashville, TN  |  931-384-0389  |  Dukeisrn@me.com  |  "
             "dukemorgan.net  |  linkedin.com/in/duke-morgan-rn-bsha-029b50b",
             size=9, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    bottom_rule(p, size=8)

    # ---- Summary ------------------------------------------------------
    section(doc, "Professional Summary")
    para(doc,
         "Registered nurse and healthcare technology leader with 20+ years of experience across "
         "emergency nursing, enterprise EMR implementation, and clinical systems leadership. "
         "Directs multiple EMR platforms and a multimillion-dollar vendor portfolio for a "
         "multi-state fertility care network. Combines clinical workflow expertise with hands-on "
         "software development to improve record access, automate operations, and introduce AI "
         "with defined controls for patient data.",
         size=9.5)

    # ---- Core Expertise -----------------------------------------------
    section(doc, "Core Expertise")
    para(doc,
         "Clinical systems strategy  |  EMR/EHR implementation and optimization  |  Product roadmaps  |  "
         "Vendor negotiation  |  Budget ownership  |  Cross-functional delivery  |  Clinical workflow design  |  "
         "Data migration  |  AI architecture and governance  |  HIPAA and PHI controls  |  HL7/FHIR interoperability",
         size=9.5, space_after=4)

    # ---- Experience ---------------------------------------------------
    section(doc, "Professional Experience")

    role(doc, "Director of Clinical Systems",
         "Inception Fertility Ventures, LLC", "Nashville, TN  |  Jun 2017 – Present")
    for b in [
        "Lead clinical systems strategy and the full product lifecycle for multiple enterprise EMR "
        "platforms supporting hundreds of clinical users across a multi-state fertility care network.",
        "Manage a multimillion-dollar annual vendor portfolio, including contract negotiations, "
        "service-level agreements, and renewals; expand platform capabilities while maintaining spend.",
        "Sustain 95% on-time delivery across platform upgrades, cloud migrations, and compliance "
        "programs by coordinating clinical operations, engineering, vendors, and executive stakeholders.",
        "Direct the clinical systems roadmap, including server migrations, platform conversions, "
        "enterprise application updates, and integration of new systems with the EMR.",
        "Built the business case for enterprise AI and established a BAA-governed Azure AI Foundry "
        "pathway. Enforce routing controls that keep PHI workloads on BAA-covered or local inference "
        "and limit commercial-model work to schema, code, and architecture.",
        "Run weekly reviews with the team to identify automation opportunities in clinical, "
        "administrative, and routine operational workflows.",
    ]:
        bullet(doc, b)

    role(doc, "Clinical Implementation Specialist, Perioperative Systems",
         "MEDHOST", "Nov 2016 – Jun 2017")
    bullet(doc, "Led workflow analysis and future-state design for multi-hospital perioperative EMR "
                "implementations across OR, pre-op, and PACU; configured modules and trained "
                "clinicians for go-live.")

    role(doc, "Clinical Application Analyst, Corporate Deployment",
         "Community Health Systems", "Mar 2016 – Oct 2016")
    bullet(doc, "Developed enterprise EMR workflow templates aligned with corporate clinical and "
                "regulatory standards; supported onsite go-lives in emergency, surgical, and "
                "medical-surgical departments.")

    role(doc, "Support and Implementation Clinical Analyst, RN",
         "MEDHOST", "Jan 2013 – Mar 2016")
    bullet(doc, "Analyzed clinical workflows, configured EMR systems, and worked with bedside "
                "clinicians to validate builds before go-live across emergency, perioperative, "
                "and medical-surgical settings.")

    # ---- Technology & Operational Results -----------------------------
    section(doc, "Selected Technology and Operational Results")

    for lead, body in [
        ("Unified clinical record access:  ",
         "Delivered a .NET 8 and React/TypeScript application on Azure that consolidated four legacy "
         "EMR platforms into one read-only clinical viewer. Migrated 3M+ clinical records, 770K+ "
         "documents, and 80K+ treatment cycles. Replaced shared credentials with Entra ID single "
         "sign-on and implemented a global authorization filter to control access across clinics."),
        ("AI orchestration and workflow automation:  ",
         "Architected and operate specialized AI agents through a model gateway to Azure AI Foundry, "
         "with access scoped by role and data classification. Built a shared knowledge base and "
         "reusable automation skills for project, task, knowledge base, and change advisory board "
         "intake. Added cross-model code review before work is marked complete."),
        ("EMR administration and clinical data analysis:  ",
         "Built a Python/Flask console for chart merges, bulk provisioning, drug library management, "
         "and permissions across site databases. Added live-state validation to stop changes when "
         "conditions differ from the approved plan. Developed a query assistant over a 600+ table SQL "
         "Server schema, restricted to schema and metadata, to shorten root-cause analysis and analyst "
         "onboarding."),
        ("Data integrity and access remediation:  ",
         "Corrected a non-unique record key in a laboratory results migration and recovered records "
         "that would otherwise have been lost. Audited permissions across two production sites, "
         "removed excess access, and identified a vendor audit gap for partial permission changes. "
         "Secured patient document storage with authenticated access and row-level controls."),
    ]:
        lead_bullet(doc, lead, body)

    # ---- Earlier Clinical Practice ------------------------------------
    section(doc, "Earlier Clinical Experience")

    role(doc, "Emergency Department Charge Nurse",
         "Williamson Medical Center", "Apr 2010 – Jan 2013")
    bullet(doc, "Led emergency nursing operations and served as a computerized provider order entry "
                "(CPOE) superuser, improving documentation workflows and communicating operational "
                "issues to IT.")

    role(doc, "Emergency Department Charge Nurse and Staff Nurse",
         "Southern Hills Medical Center (HCA)", "Jul 2005 – Jan 2010")
    bullet(doc, "Managed emergency nursing operations and supported EMR template optimization for "
                "Joint Commission and regulatory compliance.")

    # ---- Technical Skills ---------------------------------------------
    section(doc, "Technical Skills")
    para(doc,
         "SQL Server  |  Python  |  PowerShell  |  .NET  |  React/TypeScript  |  REST APIs  |  Git  |  "
         "Azure  |  Azure AI Foundry  |  Multi-agent orchestration  |  Retrieval-augmented generation  |  "
         "Local LLM deployment  |  Entra ID and SSO  |  Role-based access control  |  Supabase/PostgreSQL  |  "
         "Microsoft 365",
         size=9.5, space_after=4)

    # ---- Education ----------------------------------------------------
    section(doc, "Education")
    rich(doc, [("Bachelor of Science, Healthcare Administration", True, False, BODY),
               ("  |  Western Governors University  |  2025", False, False, MUTED)], size=9.5)
    rich(doc, [("Associate of Applied Science, Nursing", True, False, BODY),
               ("  |  Excelsior College  |  2007", False, False, MUTED)], size=9.5, space_after=4)

    # ---- Licensure and Certificates -----------------------------------
    section(doc, "Licensure and Certificates")
    bullet(doc, "Registered Nurse  |  Tennessee / Multistate Compact License  |  Active")
    bullet(doc, "OpenAI Academy  |  Agents and Workflows & AI Foundations Credential  |  2026")
    bullet(doc, "Claude Academy (Anthropic)  |  AI Fluency for Builders & Foundations  |  2026")
    bullet(doc, "Google Cloud  |  Generative AI Leader Specialization Certificate  |  2026")
    bullet(doc, "Microsoft  |  AI Agent Fundamentals with Azure AI Foundry Course Certificate  |  2026")
    bullet(doc, "Microsoft  |  SQL Server Specialization Certificate  |  2026")

    # Destination paths
    repo_root = Path(__file__).resolve().parent.parent
    resume_dir = repo_root / "site" / "resume"
    docx_out = resume_dir / "Duke-Morgan-Resume.docx"
    dated_docx_out = resume_dir / "Duke-Morgan-Resume-2026-11-01.docx"
    pdf_out = resume_dir / "Duke-Morgan-Resume.pdf"

    doc.save(docx_out)
    doc.save(dated_docx_out)
    print("Wrote DOCX to:", docx_out)
    print("Wrote DOCX to:", dated_docx_out)

    # Export to PDF via Word for Mac sandbox
    export_to_pdf(docx_out, pdf_out)


def export_to_pdf(docx_path: Path, pdf_path: Path):
    """Export DOCX to PDF using Microsoft Word for Mac without sandbox permission prompts."""
    word_container_docs = Path.home() / "Library" / "Containers" / "com.microsoft.Word" / "Data" / "Documents"
    if not word_container_docs.exists():
        word_container_docs.mkdir(parents=True, exist_ok=True)

    temp_docx = word_container_docs / "temp_resume_export.docx"
    temp_pdf = word_container_docs / "temp_resume_export.pdf"

    try:
        shutil.copy2(docx_path, temp_docx)
        ascript = f'''
        tell application "Microsoft Word"
            open "{temp_docx}"
            set activeDoc to active document
            save as activeDoc file name "{temp_pdf}" file format format PDF
            close activeDoc saving no
        end tell
        '''
        res = subprocess.run(["osascript", "-e", ascript], capture_output=True, text=True)
        if res.returncode != 0:
            print("AppleScript error:", res.stderr)
            return

        if temp_pdf.exists():
            shutil.copy2(temp_pdf, pdf_path)
            print("Wrote PDF to:", pdf_path)
        else:
            print("PDF was not created in sandbox")
    finally:
        if temp_docx.exists():
            temp_docx.unlink()
        if temp_pdf.exists():
            temp_pdf.unlink()


if __name__ == "__main__":
    build()
