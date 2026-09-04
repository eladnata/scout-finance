import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';

const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
const output = path.resolve('artifacts/release-qa');
await mkdir(output, { recursive: true });

const captures = [
  ['he-home-desktop', '/he/', 1440, 1100],
  ['he-home-mobile', '/he/', 390, 844],
  ['he-contact-desktop', '/he/contact/', 1440, 1100],
  ['he-contact-mobile', '/he/contact/', 390, 844],
  ['en-home-desktop', '/en/', 1440, 1100],
  ['en-home-mobile', '/en/', 390, 844],
  ['he-audit-tablet', '/he/audit/', 768, 1024],
];

for (const [name, route, width, height] of captures) {
  const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  await page.route('https://challenges.cloudflare.com/**', (request) => request.abort());
  await page.addInitScript(() => localStorage.setItem('scout-consent-v1', JSON.stringify({ essential: true, analytics: false, version: 1 })));
  await page.goto(`http://127.0.0.1:4173${route}`, { waitUntil: 'networkidle' });
  await page.screenshot({ path: path.join(output, `${name}.png`), fullPage: true });
  await context.close();
}

await browser.close();
