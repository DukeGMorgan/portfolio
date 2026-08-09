# Duke Morgan — Portfolio Site

Source for my personal site. A registered nurse who moved into healthcare technology
leadership and never stopped building — the site covers clinical AI, operational AI, and
enterprise EMR work.

**Live at:** _(add once the domain is connected)_

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
  build_resume.py        ← generates the résumé
  RESUME.md              ← résumé copy in plain text
```

## Running it locally

```bash
python -m http.server 8899 --directory site
```

Then open <http://localhost:8899>.

Opening `site/index.html` directly works too, though the web fonts need a network
connection.

## The résumé generator

`source/build_resume.py` builds the résumé as a DOCX via `python-docx`, then drives Word
through COM to export the PDF and report the page count.

It exists because ATS résumé parsers are unforgiving: no tables, no text boxes, no
columns, no images, nothing in headers or footers, standard section headings, and a
common font — everything linear so a parser reads it top to bottom in the intended order.
Those constraints are easy to violate by hand in Word and easy to enforce in code. The
page count check matters because the layout is tuned to fit exactly two pages, and it's
useful to find out that an edit broke that at build time rather than after sending it.

```bash
python source/build_resume.py
```

---

## A note on content

Vendor, product and platform names are generalized throughout the site. No patient data,
protected health information, credentials, connection strings, or proprietary source
appears anywhere in this repository.

## License

None. All rights reserved.

You're welcome to read this and borrow ideas — that's rather the point of publishing it.
It is not licensed for reuse, redistribution, or commercial use.
