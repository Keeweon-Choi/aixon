import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const base = process.env.AIXON_BASE || '/';
export default defineConfig({
  site: process.env.AIXON_SITE || 'http://localhost:4321',
  base,
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [mdx(), react(), sitemap()],
  // Astro 7: remark plugins need the optional @astrojs/markdown-remark peer (I-19)
  markdown: { remarkPlugins: [remarkMath], rehypePlugins: [rehypeKatex] },
});
