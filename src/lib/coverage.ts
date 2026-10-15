import { reviewLabel } from './badges';
import type { GraphData } from './graph/types';

export const wikiStatuses = ['missing', 'outline', 'draft', 'reviewed', 'published'] as const;
export type WikiStatus = (typeof wikiStatuses)[number];
export interface CoverageRow {
  fieldId: string;
  entityIds: Set<string>;
  entities: number;
  kus: number;
  papers: number;
  wiki: Record<WikiStatus, number>;
  citedClaims: number;
  reviewedClaims: number;
}

/** Coverage of a field and all its descendant fields. */
export function rowFor(graph: GraphData, fieldId: string): CoverageRow {
  const children: Record<string, string[]> = {};
  for (const [child, parents] of Object.entries(graph.parents)) {
    for (const parent of parents) (children[parent] ||= []).push(child);
  }
  const fields = new Set<string>();
  const visit = (field: string) => {
    if (fields.has(field)) return;
    fields.add(field);
    for (const child of children[field] || []) visit(child);
  };
  visit(fieldId);
  const entityIds = new Set([...fields].flatMap((field) => graph.memberships[field] || []));
  const wiki = Object.fromEntries(wikiStatuses.map((status) => [status, 0])) as Record<
    WikiStatus,
    number
  >;
  for (const id of entityIds) {
    const entry = graph.wikiFor(id);
    const status =
      entry?.status && wikiStatuses.includes(entry.status as WikiStatus)
        ? (entry.status as WikiStatus)
        : 'missing';
    wiki[status] += 1;
  }
  const claims = Object.values(graph.claims).filter(
    (claim) => entityIds.has(String(claim.subject)) || entityIds.has(String(claim.object)),
  );
  return {
    fieldId,
    entityIds,
    entities: entityIds.size,
    kus: [...entityIds].filter(
      (id) => !['Paper', 'Dataset', 'Benchmark', 'Metric'].includes(graph.types[id]),
    ).length,
    papers: [...entityIds].filter((id) => graph.types[id] === 'Paper').length,
    wiki,
    citedClaims: claims.filter(
      (claim) =>
        ['verified', 'disputed'].includes(String(claim.status)) && Boolean(claim.verification),
    ).length,
    reviewedClaims: claims.filter((claim) => reviewLabel(claim) !== '검토 대기').length,
  };
}

export function coverageRows(graph: GraphData): { rows: CoverageRow[]; total: CoverageRow } {
  const rows = Object.keys(graph.fields).map((fieldId) => rowFor(graph, fieldId));
  const all = new Set(rows.flatMap((row) => [...row.entityIds]));
  const pseudo = {
    ...graph,
    memberships: { all: [...all] },
    parents: {},
    fields: { all: {} },
  } as GraphData;
  return { rows, total: rowFor(pseudo, 'all') };
}
