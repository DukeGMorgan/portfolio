#!/usr/bin/env python3
"""Pre-commit guard: refuse to commit anything this repo promises not to publish.

Why this exists. `source/RESUME.md` sat in this public repo naming three internal
tools for a day. The deployed site was clean the whole time and `check_deploy.py`
kept reporting success, because that script only ever looks at the *live page* --
never at what git is about to push. The scan that was supposed to catch it was a
`git grep` run by hand, and its pattern happened to omit those three terms.

Two lists of the same thing had drifted apart, and the shorter one was the gate.

So this hook does not restate the terms. It reads FORBIDDEN_TERMS, NEVER_TRACK,
EMPLOYER and EMPLOYER_EXPECTED straight out of check_deploy.py, giving one list and
two enforcement points: check_deploy.py guards what is *served*, this guards what
gets *committed*. Add a term in one place and both tighten together.

The values are lifted with `ast` rather than by importing the module, because
check_deploy.py is a flat script -- it performs live HTTP checks at module level and
calls sys.exit() when done. Importing it would fire a network request on every
commit and then exit with the *deploy* result, silently skipping this scan
entirely. Parsing the literals keeps the shared list without running anything.

Enable once per clone:

    git config core.hooksPath hooks

Bypass for a single commit, knowingly:

    git commit --no-verify

Standard library only, matching the rest of the project.
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

# Names lifted from check_deploy.py. Keep in sync with what that file defines.
SHARED = ("FORBIDDEN_TERMS", "NEVER_TRACK", "EMPLOYER", "EMPLOYER_EXPECTED")

# Files that legitimately contain the forbidden terms because their job is to
# hold or enforce the list. Scanning these would guarantee a self-trip.
EXEMPT = {
    "check_deploy.py",
    "hooks/scan_staged.py",
}

# Credential shapes that should never be committed in any file.
SECRET_PATTERNS = [
    (r"\bapi[_-]?key\b", "possible API key"),
    (r"\bsecret\b", "possible secret"),
    (r"\bpassword\b", "possible password"),
    (r"\bpwd\s*=", "possible password assignment"),
    (r"\bconnection ?string\b", "possible connection string"),
    (r"\bserver\s*=\s*\S", "possible SQL connection fragment"),
]

RED, GREEN, YELLOW, DIM, RESET = (
    "\033[31m", "\033[32m", "\033[33m", "\033[2m", "\033[0m",
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout


def repo_root() -> Path:
    return Path(git("rev-parse", "--show-toplevel").strip())


def staged_paths() -> list[str]:
    """Paths added, copied, modified or renamed in the index."""
    out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    return [p for p in out.split("\0") if p]


def staged_text(path: str) -> str | None:
    """Staged content of `path`, or None if it is binary or unreadable.

    Reads from the index (`git show :path`), not the working tree, so what is
    scanned is exactly what would be committed.
    """
    try:
        blob = subprocess.run(
            ["git", "show", f":{path}"], capture_output=True, check=True
        ).stdout
    except subprocess.CalledProcessError:
        return None
    if b"\0" in blob[:8000]:
        return None  # binary; the generator that produces it is scanned instead
    try:
        return blob.decode("utf-8")
    except UnicodeDecodeError:
        return None


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def shared_config(path: Path) -> dict[str, object]:
    """Lift the SHARED constants out of check_deploy.py without executing it."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, object] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in SHARED:
                try:
                    found[target.id] = ast.literal_eval(node.value)
                except ValueError:
                    pass  # not a literal; reported as missing below
    missing = [n for n in SHARED if n not in found]
    if missing:
        raise KeyError(", ".join(missing))
    return found


def main() -> int:
    root = repo_root()
    source = root / "check_deploy.py"
    try:
        cfg = shared_config(source)
    except (OSError, SyntaxError, KeyError) as exc:
        print(
            f"{RED}pre-commit: cannot read the shared config from {source}{RESET}\n"
            f"  {type(exc).__name__}: {exc}\n"
            "  That file owns the forbidden-term list; the scan will not run blind.",
            file=sys.stderr,
        )
        return 1

    forbidden_terms = cfg["FORBIDDEN_TERMS"]
    never_track = cfg["NEVER_TRACK"]
    employer = cfg["EMPLOYER"]
    employer_expected = cfg["EMPLOYER_EXPECTED"]

    failures: list[str] = []
    paths = staged_paths()

    # 1. Files that must never be tracked, whatever .gitignore currently says.
    tracked = set(git("ls-files", "-z").split("\0"))
    for never in never_track:
        if never in tracked or never in paths:
            failures.append(f"{never} is staged or tracked and must never be committed")

    # 2. Internal names, and credential shapes, in staged text.
    term_res = [
        (t, re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE))
        for t in forbidden_terms
    ]
    secret_res = [(re.compile(p, re.IGNORECASE), why) for p, why in SECRET_PATTERNS]

    for path in paths:
        if path in EXEMPT:
            continue
        text = staged_text(path)
        if text is None:
            continue
        for term, rx in term_res:
            m = rx.search(text)
            if m:
                failures.append(
                    f"{path}:{line_of(text, m.start())} contains the internal "
                    f'name "{term}"'
                )
        for rx, why in secret_res:
            m = rx.search(text)
            if m:
                failures.append(
                    f"{path}:{line_of(text, m.start())} {why} "
                    f'({m.group(0).strip()!r})'
                )

    # 3. The employer is named in exactly one place by design.
    index_html = "site/index.html"
    if index_html in paths:
        text = staged_text(index_html)
        if text is not None:
            n = text.count(employer)
            if n != employer_expected:
                failures.append(
                    f'{index_html} names "{employer}" {n} time(s); '
                    f"expected exactly {employer_expected}"
                )

    if failures:
        print(f"\n{RED}pre-commit: refusing to commit ({len(failures)} issue(s)){RESET}\n",
              file=sys.stderr)
        for f in failures:
            print(f"  {RED}x{RESET} {f}", file=sys.stderr)
        print(
            f"\n{YELLOW}This repo is public.{RESET} Fix the above, or if a hit is a "
            f"false positive:\n"
            f"  - add the file to EXEMPT in hooks/scan_staged.py, or\n"
            f"  - commit once with {DIM}git commit --no-verify{RESET}\n",
            file=sys.stderr,
        )
        return 1

    scanned = len([p for p in paths if p not in EXEMPT])
    print(f"{GREEN}pre-commit: clean{RESET} {DIM}({scanned} staged file(s) scanned){RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
