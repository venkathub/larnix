// Larnix learner-path smoke tests (review 2026-07-19, finding E1).
//
// P0/P1 shipped with every Python gate unit-tested but ZERO automated coverage
// of the two paths a learner actually depends on: the client-side quiz engine
// and the in-browser Pyodide runtime. Both were verified by hand ("exhaustive
// ₹0 browser sweep") — honest, but unrepeatable. These tests convert those
// manual claims into a CI gate:
//
//   1. chapter page loads with badges + meta strip + quiz; quiz scores,
//      persists to localStorage, locks the attempt, offers Try again;
//   2. chapter progress: mark-complete persists and the module landing page
//      reflects it in the real progress bar;
//   3. a live Pyodide cell actually executes Python in the browser (the ₹0
//      promise itself — needs CDN access; this is the slow test).

const { test, expect } = require("@playwright/test");

const CHAPTER = "/modules/00-orientation/ch01-train-your-first-model.html";
const MODULE_INDEX = "/modules/00-orientation/index.html";
const QUIZ_KEY = "larnix-quiz:m0-ch1-train-your-first-model";
const PROGRESS_KEY = "larnix-progress:v1";

test("chapter renders and the quiz scores, persists, and locks", async ({ page }) => {
  await page.goto(CHAPTER);
  await expect(page).toHaveTitle(/Train your first model/);

  // Design-system pillars the Varsity contract promises on every chapter.
  await expect(page.locator(".larnix-badge").first()).toBeVisible();
  await expect(page.locator(".lx-chapter-meta")).toContainText("min");
  await expect(page.locator(".key-takeaways")).toBeVisible();

  // Quiz: answer every question (first option — score value is not the point),
  // submit, and verify scoring + persistence + attempt-locking.
  const quiz = page.locator(".larnix-quiz");
  await expect(quiz.locator("fieldset")).not.toHaveCount(0);
  const fieldsets = await quiz.locator("fieldset").all();
  for (const fs of fieldsets) {
    await fs.locator('input[type="radio"]').first().check();
  }
  await quiz.getByRole("button", { name: "Check answers" }).click();

  await expect(quiz.locator(".larnix-quiz-score")).toContainText(/You scored \d+ \/ \d+/);
  await expect(quiz.locator('input[type="radio"]').first()).toBeDisabled();
  await expect(quiz.getByRole("button", { name: "Try again" })).toBeVisible();

  const saved = await page.evaluate((k) => localStorage.getItem(k), QUIZ_KEY);
  expect(saved).not.toBeNull();
  expect(JSON.parse(saved)).toHaveProperty("best");

  // Try again re-renders a clean attempt.
  await quiz.getByRole("button", { name: "Try again" }).click();
  await expect(quiz.getByRole("button", { name: "Check answers" })).toBeVisible();
});

test("mark-complete persists and the module page shows real progress", async ({ page }) => {
  await page.goto(CHAPTER);
  const btn = page.locator(".lx-complete-btn");
  await expect(btn).toHaveAttribute("aria-pressed", "false");
  await btn.click();
  await expect(btn).toHaveAttribute("aria-pressed", "true");

  const map = JSON.parse(
    await page.evaluate((k) => localStorage.getItem(k) || "{}", PROGRESS_KEY)
  );
  expect(map["00-orientation/ch01-train-your-first-model"]).toMatchObject({ done: true });

  // Module landing page: the (formerly demo-only) progress bar is now real.
  await page.goto(MODULE_INDEX);
  await expect(page.locator(".lx-progress--live .lx-progress-label")).toContainText(
    /1 of \d+ complete/
  );
  const width = await page
    .locator(".lx-progress--live .lx-fill")
    .evaluate((el) => el.style.width);
  expect(parseInt(width, 10)).toBeGreaterThan(0);

  // Sidebar shows the completed tick.
  await expect(page.locator('#quarto-sidebar a.lx-done .lx-done-tick').first()).toBeVisible();
});

test("a live Pyodide cell executes Python in the browser (₹0 promise)", async ({ page }) => {
  test.slow(); // first run downloads the Pyodide runtime + wheels from the CDN
  await page.goto(CHAPTER);

  // quarto-live enables the toolbar once the runtime is ready.
  const firstEditor = page.locator(".exercise-editor").first();
  await expect(firstEditor).toBeVisible();
  const runButton = firstEditor.locator(".exercise-editor-btn-run-code");
  await expect(runButton).toBeVisible({ timeout: 120_000 });

  await runButton.click();
  // The worked cell prints; its output block must appear with real content —
  // and no runtime-failure banner (the watchdog stays quiet on success).
  const output = page.locator(".exercise-cell-output").first();
  await expect(output).toBeVisible({ timeout: 180_000 });
  await expect(output).not.toHaveText(/^\s*$/);
  await expect(page.locator(".lx-runtime-alert")).toHaveCount(0);
});
