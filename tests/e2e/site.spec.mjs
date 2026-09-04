import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const turnstileOffline = async (page) => {
  await page.route('https://challenges.cloudflare.com/**', (route) => route.fulfill({
    status: 200,
    contentType: 'application/javascript',
    body: '',
  }));
};

for (const lang of ['he', 'en']) {
  test(`${lang} home to contact keeps the conversion path available`, async ({ page }) => {
    await page.goto(`/${lang}/`);
    const cta = lang === 'he' ? 'בואו נדבר' : 'Discuss your needs';
    await page.getByRole('link', { name: cta }).first().click();
    await expect(page).toHaveURL(new RegExp(`/${lang}/contact/$`));
    const emailLabel = lang === 'he' ? 'דוא״ל עסקי *' : 'Work email *';
    await expect(page.getByLabel(emailLabel)).toBeVisible();
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations.filter((v) => ['critical', 'serious'].includes(v.impact))).toEqual([]);
  });
}

test('mobile Hebrew menu opens and closes with Escape', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/he/');
  const menu = page.getByRole('button', { name: 'תפריט' });
  await menu.click();
  await expect(menu).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(menu).toHaveAttribute('aria-expanded', 'false');
});

test('FAQ exposes its expanded state', async ({ page }) => {
  await page.goto('/en/faq/');
  const question = page.getByRole('button').filter({ hasText: 'When should an organization' }).first();
  await expect(question).toHaveAttribute('aria-expanded', 'false');
  await question.click();
  await expect(question).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('#faq-en-0')).toBeVisible();
});

test('cookie disclosure stores essential-only preferences', async ({ page }) => {
  await page.goto('/en/');
  await page.getByRole('button', { name: 'Understood' }).click();
  const stored = await page.evaluate(() => localStorage.getItem('scout-consent-v1'));
  expect(JSON.parse(stored)).toEqual({ essential: true, analytics: false, version: 1 });
  await page.reload();
  await expect(page.locator('.privacy-disclosure')).toBeHidden();
  await page.getByRole('button', { name: 'Privacy settings' }).click();
  await expect(page.locator('.privacy-disclosure')).toBeVisible();
});

for (const lang of ['he', 'en']) {
  for (const slug of ['', 'contact/', 'privacy/', 'cookies/', 'terms/', 'accessibility/', 'audit/']) {
    test(`${lang}/${slug || 'home'} has no critical or serious Axe findings`, async ({ page }) => {
      await turnstileOffline(page);
      await page.goto(`/${lang}/${slug}`);
      const results = await new AxeBuilder({ page }).analyze();
      expect(results.violations.filter((violation) => ['critical', 'serious'].includes(violation.impact))).toEqual([]);
    });
  }
}

test('services disclosure is keyboard operable', async ({ page }) => {
  await page.goto('/en/');
  const mobileMenu = page.getByRole('button', { name: 'Menu' });
  const isMobileMenu = await mobileMenu.isVisible();
  if (isMobileMenu) await mobileMenu.click();
  const services = page.getByRole('button', { name: 'Services' });
  await services.focus();
  await page.keyboard.press('Enter');
  await expect(services).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  if (isMobileMenu) {
    await expect(mobileMenu).toHaveAttribute('aria-expanded', 'false');
    await expect(mobileMenu).toBeFocused();
  } else {
    await expect(services).toHaveAttribute('aria-expanded', 'false');
    await expect(services).toBeFocused();
  }
});

async function completeContactForm(page) {
  await page.getByLabel('Name *').fill('Dana Cohen');
  await page.getByLabel('Work email *').fill('dana@example.com');
  await page.getByLabel('What would you like to discuss? *').fill('Control review');
  await page.getByLabel(/I acknowledge the collection notice/).check();
  await page.locator('[data-turnstile-token]').evaluate((input) => { input.value = 'test-token'; });
}

test('contact submission exposes pending state and reaches thank-you page', async ({ page }) => {
  await turnstileOffline(page);
  await page.route('**/api/contact', async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 120));
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, requestId: 'browser-1' }) });
  });
  await page.goto('/en/contact/');
  await completeContactForm(page);
  await page.getByRole('button', { name: 'Send enquiry' }).click();
  await expect(page.getByRole('button', { name: 'Sending securely…' })).toBeDisabled();
  await expect(page).toHaveURL(/\/en\/thank-you\/$/);
});

test('contact security failure restores the form and focuses its status', async ({ page }) => {
  await turnstileOffline(page);
  await page.route('**/api/contact', (route) => route.fulfill({ status: 400, contentType: 'application/json', body: JSON.stringify({ ok: false, code: 'turnstile_failed', message: 'Security verification failed.' }) }));
  await page.goto('/en/contact/');
  await completeContactForm(page);
  await page.getByRole('button', { name: 'Send enquiry' }).click();
  const status = page.getByRole('status');
  await expect(status).toHaveText('The security check was not completed. Please try again.');
  await expect(status).toBeFocused();
  await expect(page.getByRole('button', { name: 'Send enquiry' })).toBeEnabled();
});
