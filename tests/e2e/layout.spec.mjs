import { test, expect } from '@playwright/test';

const PAGES = ['/he/', '/en/'];

test.describe('layout system', () => {
  for (const path of PAGES) {
    test(`no horizontal overflow on ${path}`, async ({ page }) => {
      await page.goto(path);
      const overflow = await page.evaluate(() => {
        const d = document.documentElement;
        return d.scrollWidth - d.clientWidth;
      });
      expect(overflow).toBeLessThanOrEqual(1);
    });

    test(`body copy stays within its measure on ${path}`, async ({ page }) => {
      await page.goto(path);
      const ratio = await page.evaluate(() => {
        const p = document.querySelector('.section-intro');
        const fs = parseFloat(getComputedStyle(p).fontSize);
        // ~0.5em average advance width gives characters per line
        return (p.getBoundingClientRect().width / fs) * 2;
      });
      const ceiling = path === '/he/' ? 62 : 68;
      expect(ratio).toBeLessThanOrEqual(ceiling + 2);
    });
  }

  test('hebrew home headline resolves without an orphan line', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const { fontSize, lines } = await page.evaluate(() => {
      const h1 = document.querySelector('.institutional-hero h1');
      const cs = getComputedStyle(h1);
      const lh = parseFloat(cs.lineHeight);
      return {
        fontSize: parseFloat(cs.fontSize),
        lines: Math.round(h1.getBoundingClientRect().height / lh)
      };
    });
    if (testInfo.project.name === 'desktop') {
      expect(fontSize).toBeLessThanOrEqual(64);
      expect(lines).toBeLessThanOrEqual(2);
    } else {
      expect(fontSize).toBeLessThanOrEqual(40);
      expect(lines).toBeLessThanOrEqual(3);
    }
  });

  test('section rhythm varies by role', async ({ page }) => {
    await page.goto('/he/');
    const pads = await page.evaluate(() => {
      const pick = (sel) => {
        const el = document.querySelector(sel);
        return el ? parseFloat(getComputedStyle(el).paddingTop) : null;
      };
      return { feature: pick('.section--feature'), normal: pick('.section:not(.section--feature)') };
    });
    expect(pads.feature).toBeGreaterThan(pads.normal);
  });
});
