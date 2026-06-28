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

# Declared theme pairs — KEEP IN SYNC with site/theme/_larnix-components.scss
# and larnix-dark.scss. Dark badge fills are translucent, flattened over the
# dark page background.
_DARK_BASE = "#1f2428"
THEME_PAIRS = [
    ("light: body text", "#1e293b", "#ffffff"),
    ("light: muted text", "#586374", "#ffffff"),
    ("light: heading", "#0f172a", "#ffffff"),
    ("light: hero text on brand", "#ffffff", "#0b6e6e"),
    ("light: hero text on brand-strong", "#ffffff", "#075050"),
    ("light: beginner badge", "#14532d", "#e6f4ea"),
    ("light: intermediate badge", "#6b3e09", "#fdf0d5"),
    ("light: advanced badge", "#7f1d1d", "#fde2e1"),
    ("light: browser badge", "#075985", "#e0f2fe"),
    ("light: colab badge", "#8a3b0c", "#fdebd8"),
    ("light: gpu badge", "#4c1d95", "#ede9fe"),
    ("light: stable badge", "#075f43", "#e9faf2"),
    ("light: frontier badge", "#8f1133", "#fff1f2"),
    ("light: Key Takeaways heading", "#064e4e", "#f3fbfa"),
    ("light: primary link", "#0b6e6e", "#ffffff"),
    ("dark: body text", "#e2e8f0", _DARK_BASE),
    ("dark: muted text", "#aeb8c4", _DARK_BASE),
    ("dark: heading", "#f1f5f9", _DARK_BASE),
    ("dark: beginner badge", "#bbf7d0", blend((34, 197, 94, 0.18), _DARK_BASE)),
    ("dark: intermediate badge", "#fde68a", blend((217, 119, 6, 0.20), _DARK_BASE)),
    ("dark: advanced badge", "#fecaca", blend((239, 68, 68, 0.18), _DARK_BASE)),
    ("dark: browser badge", "#bae6fd", blend((56, 189, 248, 0.18), _DARK_BASE)),
    ("dark: colab badge", "#fed7aa", blend((249, 115, 22, 0.18), _DARK_BASE)),
    ("dark: gpu badge", "#ddd6fe", blend((139, 92, 246, 0.22), _DARK_BASE)),
    ("dark: stable badge", "#a7f3d0", blend((16, 185, 129, 0.18), _DARK_BASE)),
    ("dark: frontier badge", "#fecdd3", blend((244, 63, 94, 0.18), _DARK_BASE)),
    ("dark: Key Takeaways heading", "#99f6e4", "#11302e"),
    ("dark: primary link", "#2dd4bf", _DARK_BASE),
]


def check_contrast(min_ratio: float = AA_NORMAL) -> list[str]:
    failures = []
    for name, fg, bg in THEME_PAIRS:
        ratio = contrast_ratio(fg, bg)
        if ratio < min_ratio:
            failures.append(f"{name}: {fg} on {bg} = {ratio:.2f}:1 (needs >= {min_ratio})")
    return failures


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
    alt_failures = check_alt_text(paths)

    print(f"Contrast: checked {len(THEME_PAIRS)} theme pairs.")
    for f in contrast_failures:
        print(f"  FAIL {f}")
    print(f"Alt-text: scanned {len(paths)} content file(s).")
    for f in alt_failures:
        print(f"  FAIL {f}")

    total = len(contrast_failures) + len(alt_failures)
    if total:
        print(f"\na11y check failed: {total} issue(s)")
        return 1
    print("\na11y check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
