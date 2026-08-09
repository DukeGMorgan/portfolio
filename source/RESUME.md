# DUKE MORGAN, RN, BSHA

**Director of Clinical Systems | Clinical AI, Automation & Enterprise EMR**

Nashville, TN Region · 931-384-0389 · Dukeisrn@me.com · linkedin.com/in/duke-morgan-rn-bsha-029b50b

---

## SUMMARY

Registered nurse turned healthcare technology executive, with 20+ years spanning emergency
department floors, enterprise EMR implementation, and applied AI architecture. I own clinical
systems strategy for a 17-site, multi-state fertility care network — three enterprise EMR
platforms, 3,000+ clinical users, and a $2M+ annual vendor portfolio.

I also build. I architected the organization's first sanctioned, BAA-governed multi-agent AI
platform, and I write the SQL, Python, and automation that runs on it. Very few people in
healthcare IT hold an active clinical license and a production codebase at the same time.
That combination is why my roadmaps survive contact with real clinics.

---

## CORE COMPETENCIES

**Leadership & Strategy**
Enterprise EMR Product Ownership · Clinical Systems Roadmap · Multi-Site Deployment ·
Vendor & Contract Negotiation · Executive & C-Suite Stakeholder Management · Budget Ownership

**Clinical Informatics**
EMR/EHR Implementation & Optimization · Clinical Workflow Design · Clinical Decision Support ·
CPOE · HL7 / FHIR Interoperability · Legacy EMR Data Migration · Go-Live Leadership

**AI, Automation & Engineering**
Multi-Agent AI Orchestration · Azure AI Foundry · LiteLLM Routing · Local LLM Deployment
(Ollama/Qwen) for PHI Isolation · Retrieval-Augmented Generation · AI-Assisted Workflow
Automation · Automated UI + Database Regression Testing

**Compliance & Security**
HIPAA & PHI Governance · BAA-Governed AI Architecture · HITRUST-Aligned Design ·
Entra ID / SSO · Role-Based Access Control · Audit & Access Remediation ·
Joint Commission / CMS Readiness

**Technical**
MS SQL Server (600+ table clinical schemas) · Python · PowerShell · .NET · React / TypeScript ·
REST APIs · Git · Azure · Supabase / PostgreSQL · Windows Enterprise Administration · Microsoft 365

---

## PROFESSIONAL EXPERIENCE

### Director of Clinical Systems
**Inception Fertility Ventures, LLC** — Nashville, TN · Jun 2017 – Present

Clinical systems strategy and product ownership for the largest fertility care network in North
America: 17 sites, 3,000+ users, multi-state operations.

- Own the full product lifecycle for three enterprise EMR platforms — roadmap, release
  governance, vendor alignment, and optimization across the workflows clinicians use to
  deliver patient care.
- Manage a $2M+ annual vendor contract portfolio. Negotiations, SLA enforcement, and renewal
  strategy, consistently expanding capability without expanding spend.
- Direct cross-functional delivery across clinical operations, engineering, external vendors, and
  the executive team. Sustained 95% on-time delivery through platform upgrades, cloud
  migrations, and compliance programs.
- Built the business case for enterprise AI in a PHI environment and won VP of Technology
  approval for a BAA-governed Azure AI Foundry pathway — the organization's first sanctioned
  route for AI-assisted clinical operations work.
- Chartered and own the 2026 clinical systems roadmap: 11 server migration and platform
  conversion initiatives, each architected so AI tooling touches schema and metadata only,
  never patient data.
- Serve as the escalation point for defects the vendor cannot reproduce. Root-caused a
  stored-procedure fault causing 100% silent failure of a clinical documentation workflow at one
  site, and a null-dereference that made affected patient charts both un-openable and invisible
  to search.

**Selected Architecture & Build Work**

- **Clinical Intelligence Orchestration Platform** — Architected an enterprise multi-agent AI
  system routed through LiteLLM to Azure AI Foundry under an active BAA. A deliberate two-lane
  topology keeps PHI-bearing work on BAA-covered or fully local inference (Ollama/Qwen) while
  routing schema, code, and architecture work to commercial models. This became the
  organization's first HIPAA-aligned pathway for AI in clinical operations.

- **Unified Clinical Record Access Platform** — Delivered a .NET 8 and React/TypeScript
  application on Azure that consolidates four legacy EMR platforms into a single read-only
  clinical viewer behind Entra ID SSO. Migrated 3M+ clinical records, 770K+ patient documents,
  and 80K+ treatment cycles. Eliminated shared-credential access to legacy systems across all
  sites and closed a cross-clinic PHI exposure with a global authorization filter.

- **Clinical Regression Automation Platform** — Built an AI-orchestrated test framework pairing
  UI automation with direct database-state validation, so a passing test proves the record
  actually changed rather than that a screen looked right. Replaced manual QA and UAT cycles
  and shortened release timelines.

- **EMR Administration & Data Operations Console** — Python/Flask multi-site administration tool
  spanning 19 site databases: chart merge, bulk user provisioning, drug library management, and
  permission governance. Includes a plan-then-apply safety model that re-validates against live
  state and refuses to execute on drift.

- **Clinical Schema Intelligence Assistant** — AI-assisted query assistant over a 600+ table
  clinical SQL Server schema, scoped to schema and metadata only. Cut root-cause analysis time
  and shortened analyst onboarding.

- **Ambient Clinical Documentation Pipeline** — Local speech recognition feeding an Azure-hosted
  language model for structured clinical note generation, built as a replacement for a costly
  per-seat dictation vendor.

**Selected Findings & Remediations**

- Audited application permissions across two production sites and executed a governed revocation
  of an over-provisioned module, with a verified rollback proving zero unintended change. Along
  the way, discovered that the vendor's own procedure writes no audit record for partial
  permission changes — a gap affecting every change made through the vendor UI, not just
  automated ones. Reported it and built tooling that logs out-of-band.
- Traced a data-integrity fault in a laboratory results migration to a non-unique record key that
  had been silently collapsing over 200,000 duplicate groups holding differing payloads. Re-keyed
  the pipeline and recovered 17,206 records that would otherwise have been lost.
- Identified and closed a publicly readable patient document storage bucket and implemented
  authenticated, row-level-secured access in its place.

---

### Clinical Implementation Specialist — Perioperative Systems
**MEDHOST** · Nov 2016 – Jun 2017

- Led surgical workflow optimization for multi-hospital EMR implementations, including gap
  analysis and future-state design across OR, pre-op, and PACU environments.
- Configured perioperative modules and delivered clinician training that measurably improved
  go-live adoption.

### Clinical Application Analyst — Corporate Deployment
**Community Health Systems** · Mar 2016 – Oct 2016

- Developed enterprise EMR workflow templates aligned to corporate clinical and regulatory
  standards.
- Provided onsite go-live support across emergency, surgical, and med/surg departments.

### Support & Implementation Clinical Analyst, RN
**MEDHOST** · Jan 2013 – Mar 2016

- Conducted clinical workflow analysis across ED, OR, and Med/Surg and configured EMR systems to
  clinical best practice.
- Trained staff on charge capture and documentation, partnering with bedside clinicians to
  validate build decisions before go-live.

---

## EARLIER CLINICAL PRACTICE

### Emergency Department Charge Nurse
**Williamson Medical Center** · Apr 2010 – Jan 2013

Led ED nursing operations and served as CPOE superuser, streamlining documentation workflows and
routing operational findings back to IT.

### Emergency Department Charge Nurse & Staff Nurse
**Southern Hills Medical Center (HCA)** · Jul 2005 – Jan 2010

Managed emergency nursing operations and supported EMR template optimization for Joint Commission
and regulatory compliance.

---

## EDUCATION

**Bachelor of Science, Healthcare Administration (BSHA)** — Western Governors University, 2025
**Associate of Applied Science, Nursing (ASN)** — Excelsior College, 2007

---

## LICENSURE & CERTIFICATIONS

- Registered Nurse (RN) — Tennessee / Multistate Compact License, Active
- Microsoft AI Agents with Azure AI Foundry — Microsoft / Coursera, 2025
- Microsoft SQL Server Professional Certificate — Coursera
</content>
</invoke>
