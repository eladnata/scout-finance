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

  test('service cards are wide enough to hold their content', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const width = await page.evaluate(() =>
      document.querySelector('.service-entry').getBoundingClientRect().width
    );
    if (testInfo.project.name === 'desktop') {
      expect(width).toBeGreaterThan(340);
    }
  });

  test('the process rail shows ordinals in a narrow track', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const item = await page.evaluate(() => {
      const el = document.querySelector('.method-grid .rail-item');
      if (!el) return null;
      const marker = el.querySelector('.rail-marker');
      return {
        markerText: marker ? marker.textContent.trim() : null,
        markerWidth: marker ? marker.getBoundingClientRect().width : null,
        columns: getComputedStyle(el).gridTemplateColumns.split(' ').length
      };
    });
    expect(item).not.toBeNull();
    expect(item.markerText).toBe('01');
    if (testInfo.project.name === 'desktop') {
      expect(item.columns).toBe(2);
    }
  });

  test('the hero resolves above the fold', async ({ page }, testInfo) => {
    await page.goto('/he/');
    const bottom = await page.evaluate(() =>
      document.querySelector('.hero-assurance').getBoundingClientRect().bottom
    );
    const viewport = testInfo.project.use.viewport.height;
    if (testInfo.project.name === 'desktop') {
      expect(bottom).toBeLessThanOrEqual(viewport);
    }
  });

  test('mobile chrome is proportionate and reachable', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'mobile only');
    await page.goto('/he/');
    const m = await page.evaluate(() => {
      const w = (sel) => {
        const el = document.querySelector(sel);
        return el ? el.getBoundingClientRect().width : null;
      };
      const targets = [...document.querySelectorAll('a.btn, button')]
        .filter((el) => el.offsetParent !== null)
        .map((el) => el.getBoundingClientRect().height);
      return {
        viewport: window.innerWidth,
        brand: w('.brand img'),
        footerLogo: w('.site-footer .brand img'),
        smallestTarget: Math.min(...targets)
      };
    });
    expect(m.brand).toBeLessThanOrEqual(180);
    expect(m.footerLogo).toBeLessThanOrEqual(m.viewport * 0.6);
    expect(m.smallestTarget).toBeGreaterThanOrEqual(44);
  });

  test('hero actions stack on small screens', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'mobile only');
    await page.goto('/he/');
    const tops = await page.evaluate(() =>
      [...document.querySelectorAll('.institutional-hero .actions .btn')]
        .map((el) => Math.round(el.getBoundingClientRect().top))
    );
    expect(new Set(tops).size).toBe(tops.length);
  });
});
