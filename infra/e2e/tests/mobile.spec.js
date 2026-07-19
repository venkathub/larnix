// Mobile viewport smoke (deferred item from review 2026-07-19 / D0017:
// "mobile check"). The theme has no width media queries by design (auto-fit
// grids + clamp()); nothing had ever verified that bet on a phone-sized
// viewport. Checks: no horizontal overflow on the key page types, and the two
// learner controls (quiz, mark-complete) stay usable at 375 px.

const { test, expect } = require("@playwright/test");

test.use({ viewport: { width: 375, height: 812 } }); // iPhone-class

const CHAPTER = "/modules/00-orientation/ch01-train-your-first-model.html";

async function horizontalOverflow(page) {
  return page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth
  );
}

test("landing page fits a 375px viewport", async ({ page }) => {
  await page.goto("/index.html");
  expect(await horizontalOverflow(page)).toBeLessThanOrEqual(1);
  await expect(page.locator(".lx-hero")).toBeVisible();
});

test("chapter page fits and its learner controls work at 375px", async ({ page }) => {
  await page.goto(CHAPTER);
  expect(await horizontalOverflow(page)).toBeLessThanOrEqual(1);

  // Quiz is answerable and scorable on mobile.
  const quiz = page.locator(".larnix-quiz");
  await quiz.scrollIntoViewIfNeeded();
  const fieldsets = await quiz.locator("fieldset").all();
  for (const fs of fieldsets) {
    await fs.locator('input[type="radio"]').first().check();
  }
  await quiz.getByRole("button", { name: "Check answers" }).click();
  await expect(quiz.locator(".larnix-quiz-score")).toContainText(/You scored/);

  // Mark-complete is reachable and togglable.
  const btn = page.locator(".lx-complete-btn");
  await btn.scrollIntoViewIfNeeded();
  await btn.click();
  await expect(btn).toHaveAttribute("aria-pressed", "true");
});

test("module index + curriculum fit a 375px viewport", async ({ page }) => {
  await page.goto("/modules/00-orientation/index.html");
  expect(await horizontalOverflow(page)).toBeLessThanOrEqual(1);
  await page.goto("/curriculum.html");
  // Wide tables scroll inside their wrapper, not the page.
  expect(await horizontalOverflow(page)).toBeLessThanOrEqual(1);
});
