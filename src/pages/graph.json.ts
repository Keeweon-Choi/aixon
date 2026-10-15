import type { APIRoute } from 'astro';
import fs from 'node:fs';
import path from 'node:path';
import { getGraph, entityPath, claimPath, publicSummary } from '../lib/graph';
import type { GraphEdge } from '../lib/graph/view';
import { url } from '../lib/url';

type GraphEntity = {
  name?: unknown;
  title?: unknown;
  aliases?: unknown;
  fields?: unknown;
  parents?: unknown;
  status?: unknown;
};

type GraphClaim = {
  id: string;
  predicate?: string;
  subject?: string;
  object?: string;
  status?: string;
  review?: { decision?: string } | null;
  qualifiers?: { for_dimension?: string } | null;
};

const strings = (value: unknown): string[] =>
  Array.isArray(value) ? value.filter((item): item is string => typeof item === 'string') : [];

function wikiIsVisible(slug: string, build: 'preview' | 'public'): boolean {
  const filename = path.resolve(process.env.AIXON_WIKI_DIR || 'src/content/wiki', `${slug}.mdx`);
  if (!fs.existsSync(filename)) return false;
  if (build !== 'public') return true;
  const source = fs.readFileSync(filename, 'utf8');
  return /^status:\s*published\s*$/m.test(source);
}

export const GET: APIRoute = () => {
  const g = getGraph();
  const nodes = Object.entries(g.entities)
    .filter(([id]) => !['Claim', 'Source'].includes(g.types[id]))
    .map(([id, entity]) => {
      const node = entity as GraphEntity;
      const slug = id.split(':')[1] || '';
      return {
        id,
        type: g.types[id],
        name:
          typeof node.name === 'string'
            ? node.name
            : typeof node.title === 'string'
              ? node.title
              : id,
        aliases: strings(node.aliases),
        fields: strings(node.fields),
        parents: g.types[id] === 'ResearchField' ? strings(node.parents) : [],
        year: g.introYears[id],
        summary: publicSummary(entity, g.build),
        status: typeof node.status === 'string' ? node.status : 'active',
        hasWiki: wikiIsVisible(slug, g.build),
        wikiUrl: url(`wiki/${slug}/`),
        url: url(entityPath(id, g)),
      };
    });
  const edges: GraphEdge[] = Object.values(g.claims).map((claim) => {
    const edge = claim as GraphClaim;
    return {
      id: edge.id,
      kind: 'claim' as const,
      predicate: edge.predicate || '',
      source: edge.subject || '',
      target: edge.object || '',
      status: edge.status,
      reviewed: edge.review?.decision === 'approve',
      qualifiers: { for_dimension: edge.qualifiers?.for_dimension },
      url: url(claimPath(edge.id)),
    };
  });
  for (const [child, ps] of Object.entries(g.parents))
    for (const parent of ps)
      edges.push({
        id: `parent:${child}>${parent}`,
        kind: 'taxonomy',
        source: child,
        target: parent,
      });
  for (const [field, members] of Object.entries(g.memberships))
    for (const member of members)
      edges.push({
        id: `member:${member}>${field}`,
        kind: 'membership',
        source: member,
        target: field,
      });
  return new Response(JSON.stringify({ graph_version: 'build', build: g.build, nodes, edges }), {
    headers: { 'Content-Type': 'application/json' },
  });
};
