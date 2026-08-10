#!/usr/bin/env python3
"""Post-deploy safety check for dukemorgan.net.

The site makes a promise in its own footer: vendor, product and platform names
are generalized, and no private material is published. That promise is only as
good as whoever last remembered it. This script enforces it mechanically.

It answers four questions about the site as it is actually being served:

  1. Does everything that should load, load?
  2. Is anything that should NOT be public reachable?
  3. Are the security headers still applied?
  4. Does any real product, platform or employer name appear on the page?

Question 4 is the one that matters. Everything else is a nice-to-have.

Run it after a deploy:

    python check_deploy.py

Exit code 0 means clean, 1 means something needs attention. No dependencies —
standard library only, matching the rest of the project.
"""

from __future__ import annotations

import re
import subprocess
import sys
import urllib.error
import urllib.request

SITE = "https://dukemorgan.net"
TIMEOUT = 30
UA = {"User-Agent": "deploy-check/1.0 (+https://dukemorgan.net)"}

# Must be publicly reachable — these are the site.
MUST_SERVE = [
    "/",
    "/assets/css/styles.css",
    "/assets/js/main.js",
    "/assets/img/og-card.jpg",
    "/assets/img/headshot-formal.jpg",
    "/resume/Duke-Morgan-Resume.pdf",
]

# Must NOT be reachable. `site/` is the deploy root precisely so the repo root
# stays unserved; if any of these return 200, the publish directory has drifted.
MUST_NOT_SERVE = [
    "/README.md",
    "/netlify.toml",
    "/source/build_resume.py",
    "/source/RESUME.md",
    "/NOTES.private.md",
    "/.gitignore",
]

REQUIRED_HEADERS = [
    "strict-transport-security",
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
]

# Real names that must never appear on the public page. Word-boundary matched
# and case-insensitive. Add to this list rather than relying on memory.
FORBIDDEN_TERMS = [
    "eivf", "origins", "sentinel", "legacyemrviewer", "legacy emr viewer",
    "ollama", "qwen", "litellm",
    "practiceflow", "practice flow",
    "hermes", "jarvis", "muxforge", "agent quorum", "helix",
]

# The employer is named in exactly one place by design: the Experience entry.
# More than one occurrence means it has leaked into the generalized copy.
EMPLOYER = "Inception Fertility"
EMPLOYER_EXPECTED = 1

# Files that must never be tracked by git, regardless of what .gitignore says.
NEVER_TRACK = ["NOTES.private.md"]

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
failures: list[str] = []
warnings: list[str] = []


def ok(msg: str) -> None:
    print(f"  {GREEN}PASS{RESET}  {msg}")


def bad(msg: str) -> None:
    print(f"  {RED}FAIL{RESET}  {msg}")
    failures.append(msg)


def warn(msg: str) -> None:
    print(f"  {YELLOW}WARN{RESET}  {msg}")
    warnings.append(msg)


def fetch(path: str):
    """Return (status, headers, body_text). Status is None if unreachable."""
    req = urllib.request.Request(SITE + path, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read()
            text = raw.decode("utf-8", "replace") if "text" in r.headers.get(
                "Content-Type", "") or path.endswith(".html") or path == "/" else ""
            return r.status, {k.lower(): v for k, v in r.headers.items()}, text
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, ""
    except Exception as e:  # noqa: BLE001 - network failure shape varies
        print(f"  {DIM}({type(e).__name__}: {e}){RESET}")
        return None, {}, ""


def section(title: str) -> None:
    print(f"\n{title}")


# ── 1. git hygiene, before anything reaches the network ──────────────────
section("Repository")
try:
    tracked = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    for name in NEVER_TRACK:
        if name in tracked:
            bad(f"{name} is TRACKED BY GIT — it maps every pseudonym to its real name")
        else:
            ok(f"{name} is not tracked")
except Exception:  # noqa: BLE001
    warn("could not run git — skipped repository checks")

# ── 2. the site loads ────────────────────────────────────────────────────
section("Serving")
homepage = ""
for path in MUST_SERVE:
    status, headers, body = fetch(path)
    if status == 200:
        ok(f"{path}")
        if path == "/":
            homepage = body
    else:
        bad(f"{path} returned {status}, expected 200")

# ── 3. nothing private is reachable ──────────────────────────────────────
section("Not public")
for path in MUST_NOT_SERVE:
    status, _, _ = fetch(path)
    if status == 200:
        bad(f"{path} is PUBLICLY REACHABLE — check `publish` in netlify.toml")
    else:
        ok(f"{path} -> {status}")

# ── 4. security headers ──────────────────────────────────────────────────
section("Headers")
_, headers, _ = fetch("/")
for h in REQUIRED_HEADERS:
    if h in headers:
        ok(f"{h}: {headers[h]}")
    else:
        bad(f"{h} is missing")

# ── 5. the check that actually matters ───────────────────────────────────
section("Anonymization")
if not homepage:
    bad("could not read the homepage — anonymization NOT verified")
else:
    clean = True
    for term in FORBIDDEN_TERMS:
        for m in re.finditer(rf"\b{re.escape(term)}\b", homepage, re.I):
            start, end = max(0, m.start() - 60), min(len(homepage), m.end() + 60)
            context = " ".join(homepage[start:end].split())
            bad(f'"{term}" appears on the live page: ...{context}...')
            clean = False
    if clean:
        ok(f"none of the {len(FORBIDDEN_TERMS)} forbidden terms appear")

    seen = homepage.count(EMPLOYER)
    if seen == EMPLOYER_EXPECTED:
        ok(f'"{EMPLOYER}" appears exactly {seen}x (the Experience entry, by design)')
    elif seen == 0:
        warn(f'"{EMPLOYER}" not found — the Experience entry may have changed')
    else:
        bad(f'"{EMPLOYER}" appears {seen}x, expected {EMPLOYER_EXPECTED} — it has leaked '
            "beyond the Experience entry")

    host = SITE.split("//", 1)[1]
    for prop in ("og:image", "og:url"):
        m = re.search(rf'property="{prop}" content="([^"]+)"', homepage)
        if not m:
            warn(f"{prop} is missing")
        elif not m.group(1).startswith("https://"):
            bad(f"{prop} is relative ({m.group(1)}) — LinkedIn needs an absolute URL")
        elif host not in m.group(1):
            warn(f"{prop} points somewhere else: {m.group(1)}")
        else:
            ok(f"{prop} is absolute and on {host}")

# ── verdict ──────────────────────────────────────────────────────────────
print()
if failures:
    print(f"{RED}{len(failures)} problem(s) found.{RESET} The deploy needs attention.")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

if warnings:
    print(f"{YELLOW}Clean, with {len(warnings)} warning(s).{RESET}")
    sys.exit(0)

print(f"{GREEN}All checks passed.{RESET} {SITE} is serving correctly and stays anonymized.")
sys.exit(0)
