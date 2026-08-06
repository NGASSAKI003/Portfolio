import type { APIRoute } from 'astro';
import { SITE_URL } from '../lib/site';

/**
 * Genere depuis SITE_URL : le sitemap declare ici suit automatiquement
 * un changement de domaine.
 */
export const GET: APIRoute = () =>
  new Response(
    `User-agent: *
Allow: /

Sitemap: ${SITE_URL}/sitemap-index.xml
`,
    { headers: { 'Content-Type': 'text/plain; charset=utf-8' } },
  );
