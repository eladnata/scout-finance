import { test, expect } from '@playwright/test';

const routes = [
  '/he/',
  '/he/contact/',
  '/he/audit/',
  '/en/',
  '/en/contact/',
  '/en/audit/',
];
const widths = [320, 375, 390, 768, 1024, 1440];

for (const route of routes) {
  for (const width of widths) {
    test(`${route} has no horizontal overflow at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(route);
      const sizes = await page.evaluate(() => ({
        scroll: document.documentElement.scrollWidth,
        client: document.documentElement.clientWidth,
      }));
      expect(sizes.scroll).toBeLessThanOrEqual(sizes.client);
    });
  }
}

test('Hebrew contact values stay inside the mobile viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto('/he/contact/');
  for (const value of await page.locator('.contact-value').all()) {
    const box = await value.boundingBox();
    expect(box).not.toBeNull();
    expect(box.x).toBeGreaterThanOrEqual(0);
    expect(box.x + box.width).toBeLessThanOrEqual(390);
  }
});

test('mobile header reserves space for the approved wide logo', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto('/he/contact/');
  const box = await page.locator('.site-header .brand img').boundingBox();
  expect(box).not.toBeNull();
  expect(box.width).toBeLessThanOrEqual(220);
  expect(box.x).toBeGreaterThanOrEqual(0);
  expect(box.x + box.width).toBeLessThanOrEqual(390);
});
