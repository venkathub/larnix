// Automated accessibility DOM audit (deferred item from review 2026-07-19 /
// D0017: "axe/pa11y DOM audit"). The deterministic CI gate (a11y_check.py)
// covers declared theme contrast + authored alt-text; this audit covers what
// only a rendered DOM can show — ARIA misuse, label/name gaps, landmark and
// list structure, runtime contrast of composed elements.
//
// Gate policy: fail on SERIOUS + CRITICAL violations (WCAG A/AA tags). Minor/
// moderate findings are logged for later tightening, not gated, so the gate
// stays honest and non-flaky while the bar ratchets up over time.

const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

const PAGES = [
  ["landing page", "/index.html"],
  ["curriculum", "/curriculum.html"],
  ["module index", "/modules/00-orientation/index.html"],
  ["chapter", "/modules/00-orientation/ch01-train-your-first-model.html"],
  ["capstone", "/modules/03-data/capstone.html"],
];

for (const [name, path] of PAGES) {
  test(`axe audit — ${name} has no serious/critical WCAG A/AA violations`, async ({ page }) => {
    await page.goto(path);

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      // Live code editors are third-party (CodeMirror via quarto-live); their
      // internals are not ours to fix here. Everything else is audited.
      .exclude(".exercise-editor")
      .analyze();

    const gating = results.violations.filter(
      (v) => v.impact === "serious" || v.impact === "critical"
    );
    const advisory = results.violations.filter(
      (v) => v.impact !== "serious" && v.impact !== "critical"
    );
    for (const v of advisory) {
      console.log(`[advisory] ${name}: ${v.id} (${v.impact}) × ${v.nodes.length} — ${v.help}`);
    }

    expect(
      gating.map((v) => ({
        id: v.id,
        impact: v.impact,
        help: v.help,
        nodes: v.nodes.slice(0, 3).map((n) => n.target.join(" ")),
      }))
    ).toEqual([]);
  });
}
