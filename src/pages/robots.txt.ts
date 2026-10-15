import type { APIRoute } from 'astro';
import { url } from '../lib/url';

// The sitemap lives under the deployment base (GitHub Pages serves the site below /<repo>/).
const sitemap = () =>
  new URL(url('sitemap-index.xml'), import.meta.env.SITE || 'http://localhost:4321');

export const GET: APIRoute = () =>
  new Response(
    import.meta.env.AIXON_BUILD === 'public'
      ? `User-agent: *\nAllow: /\nSitemap: ${sitemap()}\n`
      : 'User-agent: *\nDisallow: /\n',
    { headers: { 'Content-Type': 'text/plain' } },
  );
