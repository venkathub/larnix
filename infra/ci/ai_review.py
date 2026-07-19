#!/usr/bin/env python3
"""AI review PR check (D0018) — AI-engineer + tutor perspective, advisory.

Posts one sticky PR comment reviewing the diff from the same rubric that steers
GitHub Copilot code review (single source of truth):

    .github/copilot-instructions.md                (repo-wide rubric)
    .github/instructions/modules.instructions.md   (content-chapter rubric)

Inference runs on **GitHub Models** via the Actions `GITHUB_TOKEN` with the
`models: read` permission — free tier, no API key, no secrets (the repo's ₹0
discipline applies to CI too).

Design decisions (see DECISIONS.md D0018):
- **Advisory by design.** LLM judgment is nondeterministic; it must never gate a
  merge. The check succeeds when it *ran* (or was cleanly skipped); the value is
  the review comment. Deterministic gates stay in `Checks`.
- **Graceful degradation.** Fork PRs (read-only token, no `models` permission),
  rate limits, or API errors post/print a notice and exit 0 — never a red X for
  infrastructure reasons.
- Generated files (`.ipynb` twins, lockfiles) are excluded from the diff before
  it is sent; the diff is clipped to a size cap with an explicit truncation note
  so the model never sees a silently-incomplete picture.

Usage (CI):    python3 ai_review.py --diff-file pr.diff --post
Usage (local): git diff main... | python3 ai_review.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

MODELS_URL = "https://models.github.ai/inference/chat/completions"
MODEL = "openai/gpt-4.1"  # GitHub Models free tier; bump deliberately (D0018)
TEMPERATURE = 0.2

# GitHub Models' free tier enforces a hard request-size cap (observed live on
# PR #5: HTTP 413 Payload Too Large at a 60k-char diff). The check therefore
# shrinks the diff and retries on 413 rather than assuming one cap — the last,
# smallest attempt still yields a useful architecture/summary-level review.
DIFF_CAPS = [16_000, 8_000, 4_000]
MAX_DIFF_CHARS = DIFF_CAPS[0]
MAX_BODY_CHARS = 2_000  # PR descriptions count against the same request cap

COMMENT_MARKER = "<!-- larnix-ai-review -->"

RUBRIC_FILES = [
    ".github/copilot-instructions.md",
    ".github/instructions/modules.instructions.md",
]

# Paths whose diffs are generated/vendored noise for a reviewer.
EXCLUDE_PATHSPECS = [
    ":(exclude)modules/**/*.ipynb",   # CI twins are derived from .qmd sources
    ":(exclude)**/package-lock.json",
    ":(exclude)_extensions/r-wasm/**",  # vendored quarto-live
]

SYSTEM_PREAMBLE = """\
You are the Larnix PR reviewer. Follow the repository rubric below exactly.
Output a single markdown review with these sections, in order:

## Verdict
One short paragraph: overall assessment from both the AI-engineer and the tutor
perspective, and whether anything looks dishonest or unverified.

## Findings
A list; each item starts with `[blocking]`, `[should-fix]`, or `[consider]`,
names the file, states the problem, the concrete fix, and — tutor mode — the
principle behind it in one sentence. If there are no findings in a severity,
omit that severity. If there are no findings at all, say so plainly.

## Questions for the author
Only genuinely load-bearing questions (0–3). Do not pad.

Be specific and kind. Do not restate the diff. Do not invent findings to seem
thorough — an honest "this looks correct" is a valid review.
"""


def load_rubric(root: Path = REPO_ROOT) -> str:
    parts = []
    for rel in RUBRIC_FILES:
        p = root / rel
        if p.is_file():
            parts.append(f"<!-- rubric: {rel} -->\n{p.read_text(encoding='utf-8')}")
    if not parts:
        raise FileNotFoundError(
            "no rubric files found — expected " + ", ".join(RUBRIC_FILES)
        )
    return "\n\n".join(parts)


def clip_diff(diff: str, cap: int = MAX_DIFF_CHARS) -> tuple[str, bool]:
    """Clip the diff to `cap` chars; the truncation is announced, never silent."""
    if len(diff) <= cap:
        return diff, False
    return (
        diff[:cap]
        + "\n\n[DIFF TRUNCATED at "
        + str(cap)
        + " chars — review what is shown and say explicitly that the tail was not reviewed]"
    ), True


def build_messages(diff: str, pr_title: str, pr_body: str, rubric: str,
                   cap: int = MAX_DIFF_CHARS) -> list[dict]:
    clipped, _ = clip_diff(diff, cap)
    body = (pr_body or "(none)")[:MAX_BODY_CHARS]
    user = (
        f"PR title: {pr_title}\n\nPR description:\n{body}\n\n"
        f"Unified diff (generated files excluded):\n```diff\n{clipped}\n```"
    )
    return [
        {"role": "system", "content": SYSTEM_PREAMBLE + "\n\n" + rubric},
        {"role": "user", "content": user},
    ]


def extract_review(response: dict) -> str:
    try:
        return response["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError) as e:
        raise ValueError(f"unexpected Models API response shape: {e}") from e


def render_comment(review: str, model: str = MODEL, truncated: bool = False) -> str:
    note = (
        "\n\n> ⚠️ The diff exceeded the size cap and was truncated before review."
        if truncated
        else ""
    )
    return (
        f"{COMMENT_MARKER}\n## 🤖 AI review — AI-engineer + tutor (advisory)\n\n"
        f"{review}{note}\n\n"
        f"---\n*Advisory only — deterministic gates live in `Checks`. "
        f"Model: `{model}` via GitHub Models (free tier, no keys). "
        f"Rubric: `.github/copilot-instructions.md` (+ path-scoped instructions). "
        f"See DECISIONS.md D0018.*"
    )


# ── network (thin, untested by unit tests; exercised in CI) ─────────────────
def _post_json(url: str, token: str, payload: dict, method: str = "POST") -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.load(resp)


def _get_json(url: str, token: str) -> object:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def call_model(messages: list[dict], token: str) -> dict:
    return _post_json(
        MODELS_URL, token, {"model": MODEL, "messages": messages, "temperature": TEMPERATURE}
    )


def upsert_sticky_comment(repo: str, pr_number: int, body: str, token: str) -> None:
    """Update the existing marker comment if present, else create one."""
    api = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    existing = _get_json(api + "?per_page=100", token)
    if isinstance(existing, list):
        for c in existing:
            if COMMENT_MARKER in (c.get("body") or ""):
                _post_json(
                    f"https://api.github.com/repos/{repo}/issues/comments/{c['id']}",
                    token,
                    {"body": body},
                    method="PATCH",
                )
                print(f"ai-review: updated existing comment {c['id']}")
                return
    _post_json(api, token, {"body": body})
    print("ai-review: posted new comment")


def review_with_retry(diff: str, token: str, pr_title: str, pr_body: str,
                      rubric: str) -> tuple[str | None, int, Exception | None]:
    """Call the model, shrinking the diff on 413 (free-tier request cap).

    Returns (review, used_cap, last_error); review is None if every attempt
    failed (the caller degrades to an advisory skip).
    """
    last_err: Exception | None = None
    for cap in DIFF_CAPS:
        messages = build_messages(diff, pr_title, pr_body, rubric, cap)
        try:
            return extract_review(call_model(messages, token)), cap, None
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 413:  # request too large — shrink and retry
                print(f"ai-review: 413 at cap {cap} — retrying with a smaller diff")
                continue
            break
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            last_err = e
            break
    return None, DIFF_CAPS[-1], last_err


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--diff-file", help="unified diff to review (default: stdin)")
    ap.add_argument("--post", action="store_true", help="post/update the sticky PR comment")
    ap.add_argument("--dry-run", action="store_true", help="print the review, post nothing")
    args = ap.parse_args(argv)

    diff = (
        Path(args.diff_file).read_text(encoding="utf-8")
        if args.diff_file
        else sys.stdin.read()
    )
    if not diff.strip():
        print("ai-review: empty diff (generated files excluded) — nothing to review")
        return 0

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("ai-review: no GITHUB_TOKEN — skipping (advisory check, not a failure)")
        return 0

    rubric = load_rubric()
    review, used_cap, last_err = review_with_retry(
        diff, token,
        os.environ.get("PR_TITLE", "(unknown)"),
        os.environ.get("PR_BODY", ""),
        rubric,
    )

    if review is None:
        # Advisory by design: fork PRs have no `models` permission, and rate
        # limits happen. Say so visibly; never fail the check for infra reasons.
        print(f"ai-review: model call unavailable ({last_err}) — skipping (advisory)")
        return 0

    _, truncated = clip_diff(diff, used_cap)
    comment = render_comment(review, truncated=truncated)
    print(comment)

    if args.post and not args.dry_run:
        repo = os.environ.get("GITHUB_REPOSITORY", "")
        pr = os.environ.get("PR_NUMBER", "")
        if repo and pr:
            try:
                upsert_sticky_comment(repo, int(pr), comment, token)
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                print(f"ai-review: could not post comment ({e}) — review is in the log above")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
