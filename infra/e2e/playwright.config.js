import { defineConfig } from "@playwright/test";

// Larnix e2e smoke config. The site under test is the already-rendered
// `_site/` (CI renders it in the same job; locally point SITE_DIR at any
// rendered copy). One worker: the tests share one static server.
export default defineConfig({
  testDir: "./tests",
  timeout: 240_000, // the Pyodide test legitimately downloads tens of MB once
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: process.env.CI ? [["github"], ["list"]] : "list",
  use: {
    baseURL: "http://127.0.0.1:4173",
    viewport: { width: 1280, height: 900 },
  },
  webServer: {
    command:
      "npx http-server " +
      (process.env.SITE_DIR || "../../_site") +
      " -p 4173 -a 127.0.0.1 --silent",
    url: "http://127.0.0.1:4173/index.html",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});
