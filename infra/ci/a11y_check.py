#!/usr/bin/env python3
"""Minimal, deterministic accessibility gate (P0 task 10 / P0-D11, Option B).

Two browser-free checks:

1. **Alt-text** — every image in content (`.qmd`/`.md`) must have non-empty alt
   text. Catches both Markdown `![alt](src)` images and inline `<img>` tags.
2. **Contrast** — every declared theme colour pair (badges, Key Takeaways box,
   links — light and dark) must meet WCAG AA for normal text (>= 4.5:1).

Full page-level axe/pa11y scanning of the rendered DOM (generated images, runtime
contrast) is deferred to a later phase; this gate is deterministic and needs no
browser, so it runs in CI and locally.

Usage:
    python3 a11y_check.py [PATH ...]      # PATHs override the default content globs

Exit 0 = pass; 1 = any alt-text or contrast failure.
"""
from __future__ import annotations

import glob
import re
import sys
from html.parser import HTMLParser

# ── colour maths (WCAG 2.x) ─────────────────────────────────────────────────
def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _srgb_to_linear(r) + 0.7152 * _srgb_to_linear(g) + 0.0722 * _srgb_to_linear(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def blend(rgba: tuple[int, int, int, float], base_hex: str) -> str:
    """Flatten a translucent colour over an opaque base, returning a hex string."""
    base = base_hex.lstrip("#")
    br, bg, bb = (int(base[i : i + 2], 16) for i in (0, 2, 4))
    r, g, b, a = rgba
    out = tuple(round(c * a + bc * (1 - a)) for c, bc in ((r, br), (g, bg), (b, bb)))
    return "#%02x%02x%02x" % out


AA_NORMAL = 4.5

# Declared theme pairs — KEEP IN SYNC with theme/_larnix-components.scss
# (claymorphism palette) and larnix-dark.scss.
_LIGHT_BG = "#fdf4ea"
_DARK_BASE = "#181527"
THEME_PAIRS = [
    ("light: body text", "#2b2b3a", _LIGHT_BG),
    ("light: heading", "#1a1a2e", _LIGHT_BG),
    ("light: muted text", "#5d5d70", _LIGHT_BG),
    # Hero gradient word — large display text (≥ ~38px bold), WCAG AA large = 3:1.
    ("light: pop coral", "#e23b34", _LIGHT_BG, 3.0),
    ("light: pop violet", "#7c3aed", _LIGHT_BG, 3.0),
    ("light: pop sky", "#0284c7", _LIGHT_BG, 3.0),
    ("light: clay teal", "#0c5f57", "#d4f3ee"),
    ("light: clay coral", "#9c2a25", "#ffe0dc"),
    ("light: clay amber", "#7a5300", "#fdecbf"),
    ("light: clay violet", "#492c93", "#e8e1fd"),
    ("light: clay sky", "#0a4a72", "#d6ecfe"),
    ("light: clay mint", "#0a6a43", "#d4f5e4"),
    ("light: pill on teal card", "#0c5f57", blend((255, 255, 255, 0.62), "#d4f3ee")),
    ("light: pill on amber card", "#7a5300", blend((255, 255, 255, 0.62), "#fdecbf")),
    ("light: primary button", "#ffffff", "#0b6e6e"),
    ("light: cta gradient end", "#ffffff", "#6d28d9"),
    ("light: beginner badge", "#14532d", "#e6f4ea"),
    ("light: intermediate badge", "#6b3e09", "#fdf0d5"),
    ("light: advanced badge", "#7f1d1d", "#fde2e1"),
    ("light: browser badge", "#075985", "#e0f2fe"),
    ("light: colab badge", "#8a3b0c", "#fdebd8"),
    ("light: gpu badge", "#4c1d95", "#ede9fe"),
    ("light: stable badge", "#075f43", "#e9faf2"),
    ("light: frontier badge", "#8f1133", "#fff1f2"),
    ("light: Key Takeaways heading", "#0c5f57", "#d4f3ee"),
    ("light: primary link", "#0b6e6e", _LIGHT_BG),
    # Navbar is translucent (rgba(255,253,250,.82)) — flatten over the page bg.
    ("light: nav text", "#2b2b3a", blend((255, 253, 250, 0.82), _LIGHT_BG)),
    ("light: nav brand", "#0b6e6e", blend((255, 253, 250, 0.82), _LIGHT_BG)),
    ("light: details summary", "#0b6e6e", "#ffffff"),
    ("light: code label", "#5d5d70", "#ece4d8"),
    ("light: running label", "#0b6e6e", "#ece4d8"),
    ("terminal text", "#d7f5e3", "#14141f"),
    ("terminal label", "#9aa3b8", "#0e0e16"),
    ("dark: body text", "#e7e3f0", _DARK_BASE),
    ("dark: heading", "#ffffff", _DARK_BASE),
    ("dark: muted text", "#b3acc7", _DARK_BASE),
    ("dark: clay teal", "#7ff0e2", "#123f3b"),
    ("dark: clay coral", "#ffb3ad", "#45211f"),
    ("dark: clay amber", "#ffd98a", "#3c2f12"),
    ("dark: clay violet", "#cbbdff", "#2a2350"),
    ("dark: clay sky", "#a9ddff", "#11314a"),
    ("dark: clay mint", "#8ef0c0", "#123a2b"),
    ("dark: pill on teal card", "#7ff0e2", blend((0, 0, 0, 0.34), "#123f3b")),
    ("dark: pill on amber card", "#ffd98a", blend((0, 0, 0, 0.34), "#3c2f12")),
    ("dark: beginner badge", "#bbf7d0", blend((34, 197, 94, 0.20), _DARK_BASE)),
    ("dark: intermediate badge", "#fde68a", blend((217, 119, 6, 0.24), _DARK_BASE)),
    ("dark: advanced badge", "#fecaca", blend((239, 68, 68, 0.20), _DARK_BASE)),
    ("dark: browser badge", "#bae6fd", blend((56, 189, 248, 0.20), _DARK_BASE)),
    ("dark: colab badge", "#fed7aa", blend((249, 115, 22, 0.20), _DARK_BASE)),
    ("dark: gpu badge", "#ddd6fe", blend((139, 92, 246, 0.26), _DARK_BASE)),
    ("dark: stable badge", "#a7f3d0", blend((16, 185, 129, 0.20), _DARK_BASE)),
    ("dark: frontier badge", "#fecdd3", blend((244, 63, 94, 0.20), _DARK_BASE)),
    ("dark: Key Takeaways heading", "#7ff0e2", "#123f3b"),
    ("dark: primary link", "#5eead4", _DARK_BASE),
    ("dark: nav text", "#e7e3f0", _DARK_BASE),
    ("dark: nav brand", "#5eead4", _DARK_BASE),
    ("dark: code label", "#b3acc7", "#2a2440"),
    ("dark: running label", "#2dd4bf", "#2a2440"),
    # ── Sepia reading mode (warm paper; light Bootstrap base + token override) ──
    ("sepia: body text", "#43392c", "#f3e9d2"),
    ("sepia: heading", "#2c2519", "#f3e9d2"),
    ("sepia: muted text", "#6a5c45", "#f3e9d2"),
    ("sepia: primary link", "#0b6e6e", "#f3e9d2"),
    ("sepia: nav text", "#43392c", blend((248, 241, 225, 0.85), "#f3e9d2")),
    ("sepia: nav brand", "#0b6e6e", blend((248, 241, 225, 0.85), "#f3e9d2")),
    ("sepia: nav active tx", "#5f4a17", "#ece0c6"),
    ("sepia: Key Takeaways heading", "#5f4a17", "#e9dcc0"),
    ("sepia: code label", "#6a5c45", "#f1e8d3"),
    ("sepia: editor teal label", "#0b6e6e", "#f1e8d3"),
    # Clay pastel cards are reused from light on the sepia page; re-assert AA.
    ("sepia: clay teal", "#0c5f57", "#d4f3ee"),
    ("sepia: clay amber", "#7a5300", "#fdecbf"),
    ("sepia: clay violet", "#492c93", "#e8e1fd"),
]


def check_contrast(min_ratio: float = AA_NORMAL) -> list[str]:
    """Each pair is (name, fg, bg) needing AA 4.5:1, or (name, fg, bg, min) — used
    for genuinely large display text, where WCAG AA allows 3:1."""
    failures = []
    for pair in THEME_PAIRS:
        name, fg, bg = pair[0], pair[1], pair[2]
        needed = pair[3] if len(pair) > 3 else min_ratio
        ratio = contrast_ratio(fg, bg)
        if ratio < needed:
            failures.append(f"{name}: {fg} on {bg} = {ratio:.2f}:1 (needs >= {needed})")
    return failures


# ── SCSS ↔ THEME_PAIRS sync (review 2026-07-19 / D0017 deferred item) ───────
# THEME_PAIRS used to be mirrored from the SCSS by hand, with a "KEEP IN SYNC"
# comment as the only guard — the review found 3 pairs for a component that no
# longer existed. This check makes the drift mechanical, in both directions:
#
#   1. ORPHANS — every literal "#rrggbb" written in the THEME_PAIRS source block
#      must still appear somewhere in the theme SCSS. A colour tweak that edits
#      the SCSS but not this file now fails CI instead of silently gating
#      against stale colours. (Computed `blend(...)` entries are built from
#      literals that are themselves checked.)
#   2. COVERAGE — every declared clay component pair (`--clay-<n>-bg`/`-tx`),
#      Key-Takeaways pair (`--lx-kt-bg`/`--lx-kt-heading`), and light badge rule
#      (`.badge-x { background: …; color: …; }`) in the SCSS must be gated by
#      some THEME_PAIRS entry. A new themed component can't ship un-gated.

THEME_SCSS_FILES = [
    "theme/_larnix-components.scss",
    "theme/larnix.scss",
    "theme/larnix-dark.scss",
]

_HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
_CLAY_RE = re.compile(r"--clay-([a-z]+)-(bg|tx):\s*(#[0-9a-fA-F]{6})")
_KT_RE = re.compile(r"--lx-kt-(bg|heading):\s*(#[0-9a-fA-F]{6})")
_BADGE_RE = re.compile(
    r"\.badge-([a-z]+)\s*\{\s*background:\s*(#[0-9a-fA-F]{6});\s*color:\s*(#[0-9a-fA-F]{6})"
)


def _pairs_source_hexes(source: str) -> set[str]:
    """Literal hex colours written inside the THEME_PAIRS block of this file."""
    start = source.index("THEME_PAIRS = [")
    end = source.index("\n]", start)
    return {h.lower() for h in _HEX_RE.findall(source[start:end])}


def _gated_combos() -> set[tuple[str, str]]:
    """(fg, bg) combinations covered by THEME_PAIRS, lowercased."""
    return {(p[1].lower(), p[2].lower()) for p in THEME_PAIRS}


def check_scss_sync(scss_text: str, pairs_source: str) -> list[str]:
    failures: list[str] = []
    scss_hexes = {h.lower() for h in _HEX_RE.findall(scss_text)}

    # 1. Orphaned pair colours (pair references a colour the theme dropped).
    for h in sorted(_pairs_source_hexes(pairs_source)):
        if h not in scss_hexes:
            failures.append(
                f"THEME_PAIRS colour {h} no longer appears in the theme SCSS — "
                f"stale pair (update or remove it)"
            )

    # 2. Un-gated declared component pairs.
    gated = _gated_combos()

    clay: dict[str, dict[str, str]] = {}
    for name, kind, hexv in _CLAY_RE.findall(scss_text):
        clay.setdefault(name, {})[kind] = hexv.lower()
    for name, d in sorted(clay.items()):
        if "bg" in d and "tx" in d and (d["tx"], d["bg"]) not in gated:
            failures.append(
                f"clay pair '{name}' ({d['tx']} on {d['bg']}) declared in SCSS "
                f"but not contrast-gated — add it to THEME_PAIRS"
            )

    kt: dict[str, str] = {}
    kt_missing = []
    for kind, hexv in _KT_RE.findall(scss_text):
        # KT pairs repeat per theme block; pair each bg with the next heading.
        if kind == "bg":
            kt["bg"] = hexv.lower()
        elif "bg" in kt:
            if (hexv.lower(), kt["bg"]) not in gated:
                kt_missing.append((hexv.lower(), kt["bg"]))
            kt = {}
    for fg, bg in kt_missing:
        failures.append(
            f"Key Takeaways pair ({fg} on {bg}) declared in SCSS but not "
            f"contrast-gated — add it to THEME_PAIRS"
        )

    for name, bg, fg in _BADGE_RE.findall(scss_text):
        if (fg.lower(), bg.lower()) not in gated:
            failures.append(
                f"badge '{name}' ({fg} on {bg}) declared in SCSS but not "
                f"contrast-gated — add it to THEME_PAIRS"
            )

    return failures


def run_scss_sync(scss_files: list[str] | None = None) -> list[str]:
    texts = []
    for path in scss_files or THEME_SCSS_FILES:
        try:
            with open(path, encoding="utf-8") as fh:
                texts.append(fh.read())
        except OSError:
            pass  # theme file layout may differ under test fixtures
    if not texts:
        return ["no theme SCSS files found — SCSS/pairs sync could not run"]
    with open(__file__, encoding="utf-8") as fh:
        pairs_source = fh.read()
    return check_scss_sync("\n".join(texts), pairs_source)


# ── alt-text ────────────────────────────────────────────────────────────────
_MD_IMAGE = re.compile(r"!\[(?P<alt>.*?)\]\((?P<src>[^)]*)\)")


class _ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.missing: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "img":
            return
        d = dict(attrs)
        alt = d.get("alt")
        if alt is None or alt.strip() == "":
            self.missing.append(d.get("src", "<no src>"))


def check_alt_text_in_text(text: str) -> list[str]:
    """Return a list of image srcs that lack non-empty alt text."""
    problems = []
    for m in _MD_IMAGE.finditer(text):
        if m.group("alt").strip() == "":
            problems.append(m.group("src") or "<no src>")
    parser = _ImgParser()
    parser.feed(text)
    problems.extend(parser.missing)
    return problems


DEFAULT_GLOBS = ["*.qmd", "modules/**/*.qmd", "modules/**/*.md"]


def _collect(args: list[str]) -> list[str]:
    if args:
        out: list[str] = []
        for a in args:
            if glob.has_magic(a):
                out.extend(glob.glob(a, recursive=True))
            else:
                out.append(a)
    else:
        out = []
        for pat in DEFAULT_GLOBS:
            out.extend(glob.glob(pat, recursive=True))
    # Skip vendored extensions.
    return sorted({p for p in out if "_extensions" not in p})


def check_alt_text(paths: list[str]) -> list[str]:
    failures = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as e:
            failures.append(f"{path}: could not read ({e})")
            continue
        for src in check_alt_text_in_text(text):
            failures.append(f"{path}: image '{src}' has no alt text")
    return failures


def main(argv: list[str]) -> int:
    paths = _collect(argv)

    contrast_failures = check_contrast()
    sync_failures = run_scss_sync()
    alt_failures = check_alt_text(paths)

    print(f"Contrast: checked {len(THEME_PAIRS)} theme pairs.")
    for f in contrast_failures:
        print(f"  FAIL {f}")
    print("SCSS/pairs sync: checked orphans + clay/KT/badge coverage.")
    for f in sync_failures:
        print(f"  FAIL {f}")
    print(f"Alt-text: scanned {len(paths)} content file(s).")
    for f in alt_failures:
        print(f"  FAIL {f}")

    total = len(contrast_failures) + len(sync_failures) + len(alt_failures)
    if total:
        print(f"\na11y check failed: {total} issue(s)")
        return 1
    print("\na11y check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
