import type { APIRoute } from 'astro';
import { getGraph, entityPath } from '../lib/graph';
import { entityTypeLabels } from '../lib/badges';
import { url } from '../lib/url';
export const GET: APIRoute = () => {
  const g = getGraph();
  return new Response(
    JSON.stringify(
      Object.entries(g.entities).map(([id, n]: any) => ({
        id,
        type: entityTypeLabels[g.types[id]] || g.types[id],
        name: n.name || n.title,
        aliases: n.aliases || [],
        url: url(entityPath(id, g)),
      })),
    ),
    { headers: { 'Content-Type': 'application/json' } },
  );
};
