import type { APIRoute } from 'astro';
export const GET: APIRoute = () => new Response(import.meta.env.AIXON_BUILD === 'public' ? `User-agent: *\nAllow: /\nSitemap: ${new URL('sitemap-index.xml', import.meta.env.SITE || 'http://localhost:4321')}\n` : 'User-agent: *\nDisallow: /\n', {headers:{'Content-Type':'text/plain'}});
