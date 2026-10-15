import { graphlib, layout } from '@dagrejs/dagre';

export type GraphNode = {
  id: string;
  type: string;
  name: string;
  aliases?: string[];
  fields?: string[];
  parents?: string[];
  year?: number;
  summary?: string;
  status?: string;
  hasWiki?: boolean;
  wikiUrl?: string;
  url?: string;
  paperTitles?: string[];
  synthetic?: boolean;
  position?: { x: number; y: number };
};

export type GraphEdge = {
  id: string;
  kind: 'claim' | 'taxonomy' | 'membership';
  source: string;
  target: string;
  predicate?: string;
  status?: string;
  reviewed?: boolean;
  url?: string;
  qualifiers?: { for_dimension?: string };
};

export type GraphViewData = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};

export type AtlasFilters = {
  types?: Set<string>;
  verifiedOnly?: boolean;
};

export type GraphProjection = {
  nodes: GraphNode[];
  edges: GraphEdge[];
  hiddenCount?: number;
};

const hiddenStatuses = new Set(['rejected', 'deprecated']);
const researchPredicates = new Set([
  'CITES',
  'INTRODUCES',
  'EXTENDS',
  'ADAPTS',
  'IMPROVES_ON',
  'ADDRESSES',
  'MITIGATES',
  'COMPARED_WITH',
  'EVALUATED_ON',
  'TRAINED_ON',
]);
const localPredicates = new Set([
  ...researchPredicates,
  'PREREQUISITE_OF',
  'RECOMMENDED_BEFORE',
  'PART_OF',
  'IS_A',
]);
export const TRACE_PREDICATES = [
  'INTRODUCES',
  'EXTENDS',
  'ADAPTS',
  'IMPROVES_ON',
  'ADDRESSES',
  'MITIGATES',
  'COMPARED_WITH',
];

export function nodeAnchor(id: string): string {
  return `#node-${id.replace(/:/g, '~')}`;
}

export function parseNodeAnchor(hash: string): string | undefined {
  const match = hash.match(/^#node-(.+)$/);
  if (!match) return undefined;
  try {
    return decodeURIComponent(match[1]).replace(/~/g, ':');
  } catch {
    return undefined;
  }
}

function visibleClaim(edge: GraphEdge): boolean {
  return edge.kind === 'claim' && !hiddenStatuses.has(edge.status || '');
}

function isAllowedType(node: GraphNode, filters: AtlasFilters): boolean {
  return node.type === 'ResearchField' || !filters.types || filters.types.has(node.type);
}

export function atlasVisible(
  data: GraphViewData,
  expanded: Set<string>,
  filters: AtlasFilters = {},
): GraphProjection {
  const byId = new Map(data.nodes.map((node) => [node.id, node]));
  const visibleIds = new Set(
    data.nodes
      .filter((node) => node.type === 'ResearchField' && (node.parents || []).length === 0)
      .map((node) => node.id),
  );

  for (const fieldId of expanded) {
    const field = byId.get(fieldId);
    if (!field || field.type !== 'ResearchField') continue;
    visibleIds.add(fieldId);
    for (const child of data.nodes)
      if (child.type === 'ResearchField' && (child.parents || []).includes(fieldId))
        visibleIds.add(child.id);
    for (const member of data.nodes)
      if (member.type !== 'ResearchField' && (member.fields || []).includes(fieldId))
        visibleIds.add(member.id);
  }

  const candidates = data.nodes.filter(
    (node) => visibleIds.has(node.id) && isAllowedType(node, filters),
  );
  const regularNodes = candidates.slice(0, 80);
  const visibleNodeIds = new Set(regularNodes.map((node) => node.id));
  const hiddenCount = Math.max(0, candidates.length - regularNodes.length);
  const nodes =
    hiddenCount > 0
      ? [
          ...regularNodes,
          {
            id: `more:${hiddenCount}`,
            type: 'More',
            name: `+${hiddenCount}개 더`,
            status: 'active',
            synthetic: true,
          },
        ]
      : regularNodes;
  const edges = data.edges.filter((edge) => {
    if (edge.kind === 'claim') {
      if (!visibleClaim(edge)) return false;
      if (filters.verifiedOnly && edge.status !== 'verified') return false;
    }
    return visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target);
  });
  return { nodes, edges, hiddenCount };
}

export function localNeighbourhood(
  data: GraphViewData,
  focus: string,
  options: { showCites?: boolean } = {},
): GraphProjection {
  const related = data.edges.filter(
    (edge) =>
      visibleClaim(edge) &&
      localPredicates.has(edge.predicate || '') &&
      (options.showCites || edge.predicate !== 'CITES'),
  );
  const visibleIds = new Set([focus]);
  for (const edge of related)
    if (edge.source === focus || edge.target === focus) {
      visibleIds.add(edge.source);
      visibleIds.add(edge.target);
    }
  const nodes = data.nodes.filter((node) => visibleIds.has(node.id));
  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges = related.filter((edge) => nodeIds.has(edge.source) && nodeIds.has(edge.target));
  return { nodes, edges };
}

export type TraceLayoutOptions = {
  showCites?: boolean;
  /** Research predicates to draw (default: all of TRACE_PREDICATES). CITES has its own switch. */
  predicates?: Set<string>;
};

export type TraceLayout = GraphProjection & {
  lanes: string[];
  minYear?: number;
};

export function traceLayout(data: GraphViewData, options: TraceLayoutOptions = {}): TraceLayout {
  const researchEdges = data.edges.filter(
    (edge) =>
      visibleClaim(edge) &&
      ((options.predicates ?? new Set(TRACE_PREDICATES)).has(edge.predicate || '') ||
        (options.showCites && edge.predicate === 'CITES')),
  );
  const introducedBy = new Map<string, string[]>();
  const papersWithTargets = new Set<string>();
  for (const edge of researchEdges)
    if (edge.predicate === 'INTRODUCES') {
      papersWithTargets.add(edge.source);
      const paper = data.nodes.find((node) => node.id === edge.source);
      if (paper) {
        const titles = introducedBy.get(edge.target) || [];
        titles.push(paper.name);
        introducedBy.set(edge.target, titles);
      }
    }
  const edgeIds = new Set(researchEdges.flatMap((edge) => [edge.source, edge.target]));
  const baseNodes = data.nodes.filter(
    (node) => edgeIds.has(node.id) && !(node.type === 'Paper' && papersWithTargets.has(node.id)),
  );
  const ids = new Set(baseNodes.map((node) => node.id));
  const edges = researchEdges.filter((edge) => ids.has(edge.source) && ids.has(edge.target));
  const years = baseNodes.flatMap((node) => (typeof node.year === 'number' ? [node.year] : []));
  const minYear = years.length ? Math.min(...years) : undefined;
  const lanes = [...new Set(baseNodes.map((node) => node.fields?.[0] || '기타'))].sort((a, b) =>
    a.localeCompare(b),
  );
  const nodes = baseNodes
    .map((node) => {
      const lane = node.fields?.[0] || '기타';
      return {
        ...node,
        paperTitles: introducedBy.get(node.id),
        position: {
          x:
            typeof node.year === 'number' && minYear !== undefined
              ? (node.year - minYear) * 160
              : -160,
          y: lanes.indexOf(lane) * 140,
        },
      };
    })
    .sort(
      (a, b) =>
        a.position.x - b.position.x || a.position.y - b.position.y || a.name.localeCompare(b.name),
    );
  return { nodes, edges, lanes, minYear };
}

export type DagreNode = {
  id: string;
  position?: { x: number; y: number };
  width?: number;
  height?: number;
};
export type DagreEdge = { source: string; target: string };

export function dagreLayout<T extends DagreNode>(
  nodes: T[],
  edges: DagreEdge[],
  direction: 'TB' | 'LR' = 'TB',
): Array<T & { position: { x: number; y: number } }> {
  const graph = new graphlib.Graph();
  graph.setGraph({ rankdir: direction, nodesep: 36, ranksep: 72 });
  graph.setDefaultEdgeLabel(() => ({}));
  for (const node of nodes)
    graph.setNode(node.id, { width: node.width || 180, height: node.height || 52 });
  for (const edge of edges)
    if (graph.hasNode(edge.source) && graph.hasNode(edge.target))
      graph.setEdge(edge.source, edge.target);
  layout(graph);
  return nodes.map((node) => {
    const positioned = graph.node(node.id) as {
      x: number;
      y: number;
      width: number;
      height: number;
    };
    const width = node.width || 180;
    const height = node.height || 52;
    return { ...node, position: { x: positioned.x - width / 2, y: positioned.y - height / 2 } };
  });
}

export type EdgeStyle = {
  dash?: string;
  markerEnd?: boolean;
  markerMiddle?: boolean;
  label?: string;
  strokeWidth: number;
  muted?: boolean;
  badge?: string;
  warning?: boolean;
  hidden?: boolean;
};

export function edgeStyle(predicate = '', status = 'verified'): EdgeStyle {
  if (hiddenStatuses.has(status)) return { strokeWidth: 0, hidden: true };
  const style: EdgeStyle = { strokeWidth: 1.5, markerEnd: true };
  if (predicate === 'COMPARED_WITH' || predicate === 'RECOMMENDED_BEFORE') {
    style.dash = '7 4';
    style.markerEnd = predicate !== 'COMPARED_WITH';
    style.label = predicate === 'RECOMMENDED_BEFORE' ? '권장' : undefined;
  }
  if (predicate === 'ADAPTS') {
    style.markerMiddle = true;
    style.label = 'NLP→CV';
  }
  if (predicate === 'IMPROVES_ON') style.strokeWidth = 3;
  if (predicate === 'ADDRESSES') style.dash = '2 4';
  if (predicate === 'CITES') {
    style.strokeWidth = 1;
    style.muted = true;
  }
  if (status === 'proposed') {
    style.dash = '2 4';
    style.badge = '미검증';
  }
  if (status === 'disputed') {
    style.warning = true;
    style.label = `⚠ ${style.label || ''}`.trim();
  }
  return style;
}
