#!/usr/bin/env python3
"""R6 free-fallback gate — paid-API lessons must show a free fallback (P0 task 11).

Per `CLAUDE.md`: every paid-API example (OpenAI/Anthropic/Gemini-paid) must also
show a free local/free-tier fallback (Ollama/Groq/free Gemini). This gate fails a
chapter that references a paid provider/key but shows no free fallback. No-op until
such a chapter exists; the mechanism is proven now.

Heuristic and intentionally conservative: it flags only when a paid marker is
present AND no free marker is found anywhere in the chapter.

Usage:
    python3 free_fallback_check.py [PATH ...]
Exit 0 = pass (or nothing to check); 1 = a paid-API chapter lacks a free fallback.
"""
from __future__ import annotations

import glob
import os
import re
import sys

# Markers that indicate a paid API is used on the required path.
PAID_MARKERS = [
    r"\bopenai\b", r"OPENAI_API_KEY", r"api\.openai\.com",
    r"\banthropic\b", r"ANTHROPIC_API_KEY", r"api\.anthropic\.com",
    r"GEMINI_API_KEY", r"GOOGLE_API_KEY",
]
# Markers that indicate a free fallback is shown.
FREE_MARKERS = [
    r"\bollama\b", r"\bgroq\b", r"localhost:11434",
    r"free tier", r"free fallback", r"gemini.*free", r"\bllama\.cpp\b",
]

PAID_RE = re.compile("|".join(PAID_MARKERS), re.IGNORECASE)
FREE_RE = re.compile("|".join(FREE_MARKERS), re.IGNORECASE)

DEFAULT_GLOBS = ["modules/**/*.qmd", "modules/**/*.ipynb"]


def check_text(text: str) -> list[str]:
    if PAID_RE.search(text) and not FREE_RE.search(text):
        return ["references a paid API but shows no free fallback (Ollama/Groq/free tier)"]
    return []


def _collect(args: list[str]) -> list[str]:
    if args:
        out: list[str] = []
        for a in args:
            out.extend(glob.glob(a, recursive=True) if glob.has_magic(a) else [a])
    else:
        out = []
        for pat in DEFAULT_GLOBS:
            out.extend(glob.glob(pat, recursive=True))
    return sorted({p for p in out if ".ipynb_checkpoints" not in p})


def main(argv: list[str]) -> int:
    targets = _collect(argv)
    if not targets:
        print("free-fallback-check (R6): no chapters found; nothing to check")
        return 0
    failed = 0
    for path in targets:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as e:
            print(f"FAIL {path}\n  - could not read ({e})")
            failed += 1
            continue
        problems = check_text(text)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"OK   {path}")
    if failed:
        print(f"\n{failed} chapter(s) use a paid API without a free fallback")
        return 1
    print(f"\nAll {len(targets)} chapter(s) provide a free path")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
