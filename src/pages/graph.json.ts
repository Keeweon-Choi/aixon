import type { APIRoute } from 'astro';
import { getGraph, entityPath, claimPath } from '../lib/graph';
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

export const GET: APIRoute = () => {
  const g = getGraph();
  const paperTitles: Record<string, string[]> = {};
  for (const claim of Object.values(g.claims) as GraphClaim[]) {
    if (claim.predicate !== 'INTRODUCES' || claim.status !== 'verified') continue;
    const paper = g.entities[claim.subject || ''] as GraphEntity | undefined;
    if (typeof paper?.title === 'string' && claim.object)
      (paperTitles[claim.object] ||= []).push(paper.title);
  }
  const nodes = Object.entries(g.entities)
    .filter(([id]) => !['Claim', 'Source'].includes(g.types[id]))
    .map(([id, entity]) => {
      const node = entity as GraphEntity;
      const wiki = g.wikiFor(id);
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
        fields: strings(node.fields).filter((field) => Boolean(g.entities[field])),
        parents: g.types[id] === 'ResearchField' ? (g.parents[id] ?? []) : [],
        year: g.introYears[id],
        paperTitles: paperTitles[id] || [],
        summary: typeof entity.summary === 'string' ? entity.summary : '',
        status: typeof node.status === 'string' ? node.status : 'active',
        hasWiki: Boolean(wiki),
        wikiUrl: wiki ? url(`wiki/${wiki.id.split(':')[1]}/`) : undefined,
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
