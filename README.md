# Duke Morgan — Portfolio Site

Source for my personal site. A registered nurse who moved into healthcare technology
leadership and never stopped building — the site covers clinical AI, operational AI, and
enterprise EMR work.

**Live at:** <https://dukemorgan.net>

---

## Stack

There isn't one, and that's deliberate.

Plain HTML, one CSS file, one JavaScript file. No framework, no bundler, no
`node_modules`, no build step. The `site/` directory *is* the deployable website — any
static host serves it as-is.

The site is responsive, works without JavaScript for all content, ships an accessible
`aria-label` description of the architecture diagram for screen readers, and loads no
third-party scripts or trackers. Total dependency count: zero, unless you count Google
Fonts.

## Layout

```
site/                    ← the deployable website; point a host at this folder
  index.html
  assets/css/styles.css
  assets/js/main.js
  assets/img/
  resume/Duke-Morgan-Resume.pdf
source/
  build_resume.py        ← generates the résumé; the single source of truth for its copy
hooks/
  pre-commit             ← blocks commits that would leak internal names
  scan_staged.py
```

## Running it locally

```bash
python -m http.server 8899 --directory site
```

Then open <http://localhost:8899>.

Opening `site/index.html` directly works too, though the web fonts need a network
connection.

## The résumé generator

`source/build_resume.py` builds the résumé as a DOCX via `python-docx`.

It exists because ATS résumé parsers are unforgiving: no tables, no text boxes, no
columns, no images, nothing in headers or footers, standard section headings, and a
common font — everything linear so a parser reads it top to bottom in the intended order.
Those constraints are easy to violate by hand in Word and easy to enforce in code.

```bash
python source/build_resume.py
```

Exporting the PDF is a **second, separate step** — the script writes only the DOCX, while
the site serves the PDF. Word is driven through COM to convert it and report the page
count, which matters because the layout is tuned to fit exactly two pages:

```powershell
$d = "$PWD\site\resume\Duke-Morgan-Resume.docx"; $p = $d -replace '\.docx$','.pdf'
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$doc = $w.Documents.Open($d, $false, $true)
"PAGES: " + $doc.ComputeStatistics(2)
$doc.SaveAs([ref]$p, [ref]17); $doc.Close([ref]$false); $w.Quit()
```

Skip that step and the site keeps serving the previous PDF.

## Checking a deploy

```bash
python check_deploy.py
```

Verifies the live site: that everything which should load does, that the repo root
isn't being served, that security headers are applied, and — the part that matters —
that no real product, platform or employer name has found its way onto the public
page. Exits non-zero if anything needs attention.

## The pre-commit guard

`check_deploy.py` inspects the *deployed page*, which means it can only ever report a
leak after it is already public. The hook in `hooks/` closes that window by checking what
git is about to commit. Enable it once per clone:

```bash
git config core.hooksPath hooks
```

It refuses a commit that stages a private file, names an internal tool, carries something
shaped like a credential, or changes how many times the employer is named. The term list
lives in exactly one place — `check_deploy.py` — and the hook reads it from there, so the
two checks cannot drift apart. To override for a single commit: `git commit --no-verify`.

---

## A note on content

Vendor, product and platform names are generalized throughout the site. No patient data,
protected health information, credentials, connection strings, or proprietary source
appears anywhere in this repository.

## License

None. All rights reserved.

You're welcome to read this and borrow ideas — that's rather the point of publishing it.
It is not licensed for reuse, redistribution, or commercial use.
