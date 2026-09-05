import { handleContact } from '../../shared/contact-handler.mts';

interface Env {
  CONTEXT?: string;
  SITE_ORIGIN?: string;
  CONTACT_ALLOWED_ORIGIN?: string;
  TURNSTILE_SECRET_KEY?: string;
  TURNSTILE_EXPECTED_HOSTNAME?: string;
  RESEND_API_KEY?: string;
  CONTACT_TO_EMAIL?: string;
  CONTACT_FROM_EMAIL?: string;
}

// Cloudflare Pages Functions: a file at functions/api/contact.ts serves
// the route /api/contact. onRequest handles every HTTP method — the
// shared handler itself returns 405 with an Allow header for anything
// but POST, matching the Netlify function's behaviour exactly.
export const onRequest: PagesFunction<Env> = async (context) => {
  const { request, env } = context;
  return handleContact(request, {
    fetch: fetch.bind(globalThis),
    env,
    requestId: crypto.randomUUID(),
    ip: request.headers.get('CF-Connecting-IP') || '',
  });
};
