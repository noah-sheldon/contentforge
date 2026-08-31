// Fetch Pixabay audio CDN links via the installed Playwright browser.
// Usage: node scripts/fetch_pixabay.mjs <search-url> <outfile>
import { chromium } from "playwright";
import { writeFile } from "node:fs/promises";

const url = process.argv[2];
const outfile = process.argv[3];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131 Safari/537.36" });
await page.goto(url, { waitUntil: "networkidle", timeout: 45000 }).catch(() => {});
await page.waitForTimeout(2500);

const data = await page.evaluate(() => {
  const out = [];
  for (const a of document.querySelectorAll("audio")) {
    if (a.src) out.push({ tag: "audio", url: a.src });
  }
  for (const s of document.querySelectorAll("script")) {
    const m = s.textContent.matchAll(/https:\/\/cdn\.pixabay\.com\/audio\/[^"'\\\s]+/g);
    for (const x of m) out.push({ tag: "cdn", url: x[0] });
  }
  for (const a of document.querySelectorAll("a[href*='cdn.pixabay.com/audio']")) {
    out.push({ tag: "link", url: a.href });
  }
  return [...new Map(out.map(o => [o.url, o])).values()].slice(0, 12);
});

await browser.close();
await writeFile(outfile, JSON.stringify(data, null, 2));
console.log(JSON.stringify(data.map(d => d.url), null, 1));
