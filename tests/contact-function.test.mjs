import assert from 'node:assert/strict';
import test from 'node:test';

import { handleContact, validateFields } from '../netlify/functions/contact.mts';

const origin = 'https://www.scout-finance.co.il';
const validFields = {
  lang: 'en',
  name: 'Dana Cohen',
  email: 'dana@example.com',
  organization: '',
  phone: '',
  message: 'We need help reviewing our control environment.',
  privacy_ack: 'yes',
  website: '',
  'cf-turnstile-response': 'valid-token',
};
const validEnv = {
  SITE_ORIGIN: origin,
  TURNSTILE_SECRET_KEY: 'production-secret',
  TURNSTILE_EXPECTED_HOSTNAME: 'www.scout-finance.co.il',
  RESEND_API_KEY: 'resend-secret',
  CONTACT_TO_EMAIL: 'inbox@scout-finance.co.il',
  CONTACT_FROM_EMAIL: 'website@scout-finance.co.il',
  CONTEXT: 'deploy-preview',
};

function requestFor(overrides = {}, options = {}) {
  const fields = { ...validFields, ...overrides };
  const body = new FormData();
  for (const [key, value] of Object.entries(fields)) {
    if (value !== undefined) body.set(key, value);
  }
  return new Request(`${origin}/api/contact`, {
    method: options.method || 'POST',
    headers: { Origin: options.origin || origin, ...(options.headers || {}) },
    ...(options.method === 'GET' ? {} : { body }),
  });
}

function successfulFetch(log = []) {
  return async (url, init) => {
    log.push({ url: String(url), init });
    if (String(url).includes('siteverify')) {
      return Response.json({ success: true, hostname: 'www.scout-finance.co.il' });
    }
    return Response.json({ id: 'email-1' }, { status: 200 });
  };
}

async function responseJson(request, overrides = {}) {
  const response = await handleContact(request, {
    fetch: overrides.fetch || successfulFetch(),
    env: { ...validEnv, ...(overrides.env || {}) },
    requestId: overrides.requestId || 'req-123',
    ip: '203.0.113.12',
  });
  return { response, body: await response.json() };
}

test('rejects non-POST requests with 405', async () => {
  const { response } = await responseJson(requestFor({}, { method: 'GET' }));
  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'POST');
});

test('rejects an invalid origin with 403', async () => {
  const { response, body } = await responseJson(requestFor({}, { origin: 'https://attacker.example' }));
  assert.equal(response.status, 403);
  assert.equal(body.code, 'origin_rejected');
});

test('rejects unsupported content types with 415', async () => {
  const request = new Request(`${origin}/api/contact`, { method: 'POST', headers: { Origin: origin, 'Content-Type': 'application/json' }, body: '{}' });
  const { response } = await responseJson(request);
  assert.equal(response.status, 415);
});

test('validates privacy acknowledgement, limits and email shape', () => {
  assert.equal(validateFields({ ...validFields, privacy_ack: '' }).valid, false);
  assert.equal(validateFields({ ...validFields, name: 'x'.repeat(121) }).valid, false);
  assert.equal(validateFields({ ...validFields, message: 'x'.repeat(5001) }).valid, false);
  assert.equal(validateFields({ ...validFields, email: 'invalid' }).valid, false);
  assert.equal(validateFields(validFields).valid, true);
});

test('rejects missing privacy acknowledgement with 400', async () => {
  const { response, body } = await responseJson(requestFor({ privacy_ack: undefined }));
  assert.equal(response.status, 400);
  assert.equal(body.code, 'invalid_form');
});

test('rejects name over 120 characters and message over 5000 characters', async () => {
  assert.equal((await responseJson(requestFor({ name: 'x'.repeat(121) }))).response.status, 400);
  assert.equal((await responseJson(requestFor({ message: 'x'.repeat(5001) }))).response.status, 400);
});

test('accepts optional empty organization and phone', async () => {
  const { response, body } = await responseJson(requestFor());
  assert.equal(response.status, 200);
  assert.deepEqual(body, { ok: true, requestId: 'req-123' });
});

test('silently accepts a filled honeypot without external calls', async () => {
  let calls = 0;
  const { response } = await responseJson(requestFor({ website: 'spam.example' }), { fetch: async () => { calls += 1; throw new Error('not expected'); } });
  assert.equal(response.status, 200);
  assert.equal(calls, 0);
});

for (const [label, token, cloudflare, expectedHostname] of [
  ['missing token', undefined, null, null],
  ['network failure', 'token', new Error('network'), null],
  ['non-2xx response', 'token', new Response('bad gateway', { status: 502 }), null],
  ['unsuccessful response', 'token', Response.json({ success: false }), null],
  ['expired token', 'token', Response.json({ success: false, 'error-codes': ['timeout-or-duplicate'] }), null],
  ['hostname mismatch', 'token', Response.json({ success: true, hostname: 'other.example' }), 'www.scout-finance.co.il'],
]) {
  test(`rejects Turnstile ${label} without sending email`, async () => {
    let emailCalls = 0;
    const fetchDouble = async (url) => {
      if (!String(url).includes('siteverify')) { emailCalls += 1; return Response.json({ id: 'unexpected' }); }
      if (cloudflare instanceof Error) throw cloudflare;
      return cloudflare;
    };
    const { response, body } = await responseJson(requestFor({ 'cf-turnstile-response': token }), { fetch: fetchDouble, env: expectedHostname ? { TURNSTILE_EXPECTED_HOSTNAME: expectedHostname } : {} });
    assert.equal(response.status, 400);
    assert.equal(body.code, 'turnstile_failed');
    assert.equal(emailCalls, 0);
  });
}

test('fails closed when delivery configuration is missing', async () => {
  const { response, body } = await responseJson(requestFor(), { env: { RESEND_API_KEY: '', CONTACT_TO_EMAIL: '', CONTACT_FROM_EMAIL: '' } });
  assert.equal(response.status, 503);
  assert.equal(body.code, 'service_unavailable');
});

test('maps a Resend failure to delivery_failed', async () => {
  const fetchDouble = async (url) => String(url).includes('siteverify')
    ? Response.json({ success: true, hostname: 'www.scout-finance.co.il' })
    : Response.json({ message: 'failure' }, { status: 500 });
  const { response, body } = await responseJson(requestFor(), { fetch: fetchDouble });
  assert.equal(response.status, 502);
  assert.equal(body.code, 'delivery_failed');
});

test('validates Turnstile server-side and sends fixed-subject escaped email', async () => {
  const calls = [];
  const { response, body } = await responseJson(requestFor({ name: '<Dana>', message: '<b>Review</b>\r\nControls' }), { fetch: successfulFetch(calls), requestId: 'req-safe-456' });
  assert.equal(response.status, 200);
  assert.deepEqual(body, { ok: true, requestId: 'req-safe-456' });
  assert.equal(calls.length, 2);
  const verifyBody = new URLSearchParams(calls[0].init.body);
  assert.equal(verifyBody.get('response'), 'valid-token');
  assert.equal(verifyBody.get('remoteip'), '203.0.113.12');
  assert.equal(verifyBody.get('idempotency_key'), 'req-safe-456');
  const email = JSON.parse(calls[1].init.body);
  assert.equal(email.reply_to, 'dana@example.com');
  assert.match(email.subject, /^Scout Finance website enquiry · req-safe-456$/);
  assert.doesNotMatch(email.subject, /Dana|Review/);
  assert.match(email.html, /&lt;Dana&gt;/);
  assert.doesNotMatch(email.html, /<b>Review<\/b>/);
});

test('rejects published Cloudflare test secrets in production', async () => {
  const { response, body } = await responseJson(requestFor(), { env: { CONTEXT: 'production', TURNSTILE_SECRET_KEY: '1x0000000000000000000000000000000AA' } });
  assert.equal(response.status, 503);
  assert.equal(body.code, 'service_unavailable');
});
