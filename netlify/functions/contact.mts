import { handleContact, validateFields } from '../../shared/contact-handler.mts';

export { handleContact, validateFields };

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
