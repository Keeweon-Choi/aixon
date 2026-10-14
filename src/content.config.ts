import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const level = z.enum(['intuition', 'fundamentals', 'deep']);
const section = z.enum(['overview', 'why', 'mechanism', 'math', 'example', 'code', 'visual', 'limitations', 'history', 'related', 'references']);
export const collections = {
  wiki: defineCollection({
    loader: glob({ pattern: '**/*.mdx', base: process.env.AIXON_WIKI_DIR || 'src/content/wiki' }),
    schema: z.object({
      id: z.string().regex(/^wiki:[a-z0-9]+(?:-[a-z0-9]+)*$/), entity: z.string().regex(/^[a-z]+:[a-z0-9]+(?:-[a-z0-9]+)*$/), title: z.string().min(1), subtitle: z.string().min(1),
      status: z.enum(['outline', 'draft', 'reviewed', 'published']), levels: z.array(level).min(1), sections: z.array(section).min(1),
      authors: z.array(z.object({ id: z.string().regex(/^(agent|human):/), role: z.enum(['draft', 'edit', 'review']) })).min(1), ai_generated: z.boolean(),
      review: z.object({ by: z.string().regex(/^human:/), at: z.coerce.date(), decision: z.literal('approve'), note: z.string() }).nullable(), published_at: z.coerce.date().nullable(),
      sources: z.array(z.string()), claims: z.array(z.string()), labs: z.array(z.string()), figures: z.array(z.object({ id: z.string(), origin: z.literal('self-made'), alt: z.string().min(1) })), updated_at: z.coerce.date(),
    }).superRefine((value, ctx) => { if (['reviewed', 'published'].includes(value.status) && !value.review) ctx.addIssue({ code: 'custom', message: 'review required' }); if (value.status === 'published' && !value.published_at) ctx.addIssue({ code: 'custom', message: 'published_at required' }); }),
  }),
};
