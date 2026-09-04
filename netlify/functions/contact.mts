const TURNSTILE_VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
const RESEND_EMAIL_URL = 'https://api.resend.com/emails';
const DEFAULT_ORIGIN = 'https://www.scout-finance.co.il';
const TEST_SECRET_KEYS = new Set([
  '1x0000000000000000000000000000000AA',
  '2x0000000000000000000000000000000AA',
  '3x0000000000000000000000000000000AA',
]);
const ALLOWED_FIELDS = new Set([
  'lang', 'name', 'email', 'organization', 'phone', 'message',
  'privacy_ack', 'website', 'cf-turnstile-response',
]);

const normalize = (value) => String(value ?? '')
  .replace(/\r\n?/g, '\n')
  .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '')
  .trim();

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function validateFields(input) {
  const values = {
    lang: normalize(input.lang),
    name: normalize(input.name),
    email: normalize(input.email),
    organization: normalize(input.organization),
    phone: normalize(input.phone),
    message: normalize(input.message),
    privacy_ack: normalize(input.privacy_ack),
    website: normalize(input.website),
    turnstile: normalize(input['cf-turnstile-response']),
  };
  const errors = [];
  if (!['he', 'en'].includes(values.lang)) errors.push('lang');
  if (!values.name || values.name.length > 120) errors.push('name');
  if (!values.email || values.email.length > 254 || !emailPattern.test(values.email)) errors.push('email');
  if (values.organization.length > 160) errors.push('organization');
  if (values.phone.length > 40) errors.push('phone');
  if (!values.message || values.message.length > 5000) errors.push('message');
  if (values.privacy_ack !== 'yes') errors.push('privacy_ack');
  return { valid: errors.length === 0, errors, values };
}

const json = (status, code, message, requestId, extraHeaders = {}) => new Response(
  JSON.stringify({ ok: status >= 200 && status < 300, ...(code ? { code } : {}), ...(message ? { message } : {}), ...(requestId ? { requestId } : {}) }),
  {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff',
      ...extraHeaders,
    },
  },
);

const htmlEscape = (value) => normalize(value).replace(/[&<>"']/g, (character) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
})[character]);

function configurationReady(env) {
  const required = ['TURNSTILE_SECRET_KEY', 'RESEND_API_KEY', 'CONTACT_TO_EMAIL', 'CONTACT_FROM_EMAIL'];
  if (required.some((name) => !normalize(env[name]))) return false;
  if (normalize(env.CONTEXT).toLowerCase() === 'production' && TEST_SECRET_KEYS.has(normalize(env.TURNSTILE_SECRET_KEY))) return false;
  return true;
}

async function verifyTurnstile(token, requestId, ip, deps) {
  if (!token) return false;
  const body = new URLSearchParams({
    secret: deps.env.TURNSTILE_SECRET_KEY,
    response: token,
    idempotency_key: requestId,
  });
  if (ip) body.set('remoteip', ip);
  try {
    const response = await deps.fetch(TURNSTILE_VERIFY_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
      signal: AbortSignal.timeout(8_000),
    });
    if (!response.ok) return false;
    const result = await response.json();
    if (result.success !== true) return false;
    const expected = normalize(deps.env.TURNSTILE_EXPECTED_HOSTNAME);
    return !expected || normalize(result.hostname) === expected;
  } catch (_error) {
    return false;
  }
}

function messageBodies(values, requestId) {
  const labels = values.lang === 'he'
    ? { name: 'שם', email: 'דוא״ל', organization: 'ארגון', phone: 'טלפון', message: 'הודעה' }
    : { name: 'Name', email: 'Email', organization: 'Organization', phone: 'Phone', message: 'Message' };
  const rows = [
    [labels.name, values.name],
    [labels.email, values.email],
    [labels.organization, values.organization || '—'],
    [labels.phone, values.phone || '—'],
    [labels.message, values.message],
    ['Request ID', requestId],
  ];
  return {
    text: rows.map(([label, value]) => `${label}:\n${value}`).join('\n\n'),
    html: `<div style="font-family:Arial,sans-serif;line-height:1.6">${rows.map(([label, value]) => `<p><strong>${htmlEscape(label)}</strong><br><span style="white-space:pre-wrap">${htmlEscape(value)}</span></p>`).join('')}</div>`,
  };
}

async function deliverEmail(values, requestId, deps) {
  const content = messageBodies(values, requestId);
  const prefix = values.lang === 'he' ? 'פנייה מאתר Scout Finance' : 'Scout Finance website enquiry';
  try {
    const response = await deps.fetch(RESEND_EMAIL_URL, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${deps.env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: deps.env.CONTACT_FROM_EMAIL,
        to: [deps.env.CONTACT_TO_EMAIL],
        reply_to: values.email,
        subject: `${prefix} · ${requestId}`,
        text: content.text,
        html: content.html,
      }),
      signal: AbortSignal.timeout(10_000),
    });
    return response.ok;
  } catch (_error) {
    return false;
  }
}

export async function handleContact(request, deps) {
  const requestId = normalize(deps.requestId);
  if (request.method !== 'POST') {
    return json(405, 'method_not_allowed', 'Method not allowed.', requestId, { Allow: 'POST' });
  }

  const expectedOrigin = normalize(deps.env.CONTACT_ALLOWED_ORIGIN || deps.env.SITE_ORIGIN || DEFAULT_ORIGIN);
  if (normalize(request.headers.get('Origin')) !== expectedOrigin) {
    return json(403, 'origin_rejected', 'Request origin was rejected.', requestId);
  }

  const contentType = normalize(request.headers.get('Content-Type')).toLowerCase();
  if (!contentType.startsWith('multipart/form-data') && !contentType.startsWith('application/x-www-form-urlencoded')) {
    return json(415, 'unsupported_media_type', 'Unsupported form encoding.', requestId);
  }

  let form;
  try {
    form = await request.formData();
  } catch (_error) {
    return json(400, 'invalid_form', 'The submitted form could not be read.', requestId);
  }

  const input = {};
  for (const [key, value] of form.entries()) {
    if (!ALLOWED_FIELDS.has(key) || typeof value !== 'string' || Object.hasOwn(input, key)) {
      return json(400, 'invalid_form', 'Please check the submitted fields.', requestId);
    }
    input[key] = value;
  }

  if (normalize(input.website)) return json(200, null, null, requestId);

  const validation = validateFields(input);
  if (!validation.valid) return json(400, 'invalid_form', 'Please check the required fields.', requestId);

  if (!configurationReady(deps.env)) {
    return json(503, 'service_unavailable', 'The contact service is not configured.', requestId);
  }

  const verified = await verifyTurnstile(validation.values.turnstile, requestId, normalize(deps.ip), deps);
  if (!verified) return json(400, 'turnstile_failed', 'Security verification failed.', requestId);

  const delivered = await deliverEmail(validation.values, requestId, deps);
  if (!delivered) return json(502, 'delivery_failed', 'The enquiry could not be delivered.', requestId);

  return json(200, null, null, requestId);
}

const runtimeEnvironment = () => {
  const names = [
    'CONTEXT', 'SITE_ORIGIN', 'CONTACT_ALLOWED_ORIGIN', 'TURNSTILE_SECRET_KEY',
    'TURNSTILE_EXPECTED_HOSTNAME', 'RESEND_API_KEY', 'CONTACT_TO_EMAIL',
    'CONTACT_FROM_EMAIL',
  ];
  return Object.fromEntries(names.map((name) => [name, globalThis.Netlify?.env?.get(name) || '']));
};

export default async (request, context) => handleContact(request, {
  fetch: globalThis.fetch,
  env: runtimeEnvironment(),
  requestId: context?.requestId || crypto.randomUUID(),
  ip: context?.ip || '',
});

export const config = {
  path: '/api/contact',
  method: 'POST',
  rateLimit: {
    windowLimit: 8,
    windowSize: 60,
    aggregateBy: ['ip', 'domain'],
  },
};
