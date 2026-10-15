import {
  Background,
  Controls,
  MarkerType,
  ReactFlow,
  type Edge,
  type Node,
  type ReactFlowInstance,
} from '@xyflow/react';
import { useEffect, useMemo, useState } from 'react';
import {
  atlasVisible,
  dagreLayout,
  edgeStyle,
  localNeighbourhood,
  parseNodeAnchor,
  traceLayout,
  type GraphEdge,
  type GraphNode as GraphDataNode,
  type GraphViewData,
} from '../lib/graph/view';
import ClaimEdge, { type ClaimEdgeData } from './graph/ClaimEdge';
import GraphNode, { type FlowNodeData } from './graph/GraphNode';
import '@xyflow/react/dist/style.css';
import '../styles/graph.css';

type Mode = 'atlas' | 'local' | 'trace';
type TopField = { id: string; name: string; url?: string };
type FlowGraphNode = Node<FlowNodeData, 'graph'>;
type FlowGraphEdge = Edge<ClaimEdgeData, 'claim'>;

const nodeTypes = { graph: GraphNode };
const edgeTypes = { claim: ClaimEdge };

function fallbackFields(topFields: TopField[]) {
  return (
    <ul className="graph-fallback-fields">
      {topFields.map((field) => (
        <li key={field.id} data-node-id={field.id}>
          {field.url ? <a href={field.url}>{field.name}</a> : field.name}
        </li>
      ))}
    </ul>
  );
}

function expandableFields(data: GraphViewData, selectedId: string): Set<string> {
  const byId = new Map(data.nodes.map((node) => [node.id, node]));
  const expanded = new Set<string>();
  const revealField = (fieldId: string) => {
    const field = byId.get(fieldId);
    if (!field || field.type !== 'ResearchField') return;
    for (const parent of field.parents || []) {
      revealField(parent);
      expanded.add(parent);
    }
  };
  const selected = byId.get(selectedId);
  if (!selected) return expanded;
  if (selected.type === 'ResearchField') revealField(selected.id);
  for (const field of selected.fields || []) {
    revealField(field);
    expanded.add(field);
  }
  return expanded;
}

function edgeLabel(edge: GraphEdge): string {
  const style = edgeStyle(edge.predicate, edge.status);
  const review = edge.status === 'verified' && !edge.reviewed ? ' ○' : '';
  return `${style.badge || style.label || edge.predicate || '관계'}${review}`;
}

function nodeRow(node: GraphDataNode, select: (id: string) => void, expanded?: Set<string>) {
  return (
    <tr
      key={node.id}
      data-node-id={node.id}
      aria-expanded={expanded && node.type === 'ResearchField' ? expanded.has(node.id) : undefined}
      aria-label={`${node.type} ${node.name} ${node.status || 'active'}`}
      tabIndex={0}
      onClick={() => select(node.id)}
      onKeyDown={(event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          select(node.id);
        }
      }}
    >
      <td>{node.url ? <a href={node.url}>{node.name}</a> : node.name}</td>
      <td>{node.type}</td>
      <td>{node.status || 'active'}</td>
      <td>{node.year || '연도 미상'}</td>
    </tr>
  );
}

export default function GraphView({
  mode,
  focus,
  topFields = [],
}: {
  mode: Mode;
  focus?: string;
  topFields?: TopField[];
}) {
  const [data, setData] = useState<GraphViewData>();
  const [failed, setFailed] = useState(false);
  const [list, setList] = useState(false);
  const [selected, setSelected] = useState(focus || '');
  const [expanded, setExpanded] = useState(new Set<string>());
  const [enabledTypes, setEnabledTypes] = useState<Set<string>>();
  const [verifiedOnly, setVerifiedOnly] = useState(false);
  const [showCites, setShowCites] = useState(false);
  const [flow, setFlow] = useState<ReactFlowInstance<FlowGraphNode, FlowGraphEdge>>();

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${import.meta.env.BASE_URL}graph.json`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`graph.json: ${response.status}`);
        return response.json() as Promise<GraphViewData>;
      })
      .then((result) => {
        setData(result);
        setEnabledTypes(new Set(result.nodes.map((node) => node.type)));
        const hashSelection = parseNodeAnchor(location.hash);
        const initialSelection = hashSelection || focus || '';
        if (initialSelection) {
          setSelected(initialSelection);
          if (mode === 'atlas') setExpanded(expandableFields(result, initialSelection));
        }
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') return;
        setFailed(true);
      });
    setList(matchMedia('(max-width: 700px)').matches);
    return () => controller.abort();
  }, [focus, mode]);

  const projection = useMemo(() => {
    if (!data) return { nodes: [], edges: [] };
    if (mode === 'atlas')
      return atlasVisible(data, expanded, { types: enabledTypes, verifiedOnly });
    if (mode === 'local') return localNeighbourhood(data, focus || selected, { showCites });
    return traceLayout(data, { showCites });
  }, [data, enabledTypes, expanded, focus, mode, selected, showCites, verifiedOnly]);

  function selectNode(id: string) {
    setSelected(id);
    if (mode === 'atlas') {
      const node = data?.nodes.find((item) => item.id === id);
      if (node?.type === 'ResearchField')
        setExpanded((current) => {
          const next = new Set(current);
          if (next.has(id)) next.delete(id);
          else next.add(id);
          return next;
        });
    }
    history.replaceState(null, '', `#node-${id.replace(/:/g, '~')}`);
  }

  const flowNodes = useMemo((): FlowGraphNode[] => {
    const positioned =
      mode === 'trace'
        ? projection.nodes
        : dagreLayout(
            projection.nodes.map((node) => ({ ...node, width: 180, height: 54 })),
            projection.edges,
          );
    return positioned.map((node) => ({
      id: node.id,
      type: 'graph',
      position: node.position || { x: 0, y: 0 },
      data: { node, expanded: expanded.has(node.id), activate: selectNode },
      selected: node.id === selected,
      focusable: true,
    }));
  }, [expanded, mode, projection.edges, projection.nodes, selected]);

  const flowEdges = useMemo((): FlowGraphEdge[] => {
    const output: FlowGraphEdge[] = [];
    for (const edge of projection.edges) {
      const style = edgeStyle(edge.predicate, edge.status);
      if (style.hidden) continue;
      output.push({
        id: edge.id,
        type: 'claim',
        source: edge.source,
        target: edge.target,
        data: { edge, style, label: edgeLabel(edge) },
        markerEnd: style.markerEnd ? { type: MarkerType.ArrowClosed } : undefined,
        focusable: false,
      });
    }
    return output;
  }, [projection.edges]);

  useEffect(() => {
    if (!selected || !flow || !flowNodes.some((node) => node.id === selected)) return;
    requestAnimationFrame(() =>
      flow.fitView({ nodes: [{ id: selected }], duration: 0, padding: 0.5 }),
    );
  }, [flow, flowNodes, selected]);

  const selectedNode =
    projection.nodes.find((node) => node.id === selected) ||
    data?.nodes.find((node) => node.id === selected);
  const trace =
    mode === 'trace' ? traceLayout(data || { nodes: [], edges: [] }, { showCites }) : undefined;
  const fieldName = (id: string) => data?.nodes.find((node) => node.id === id)?.name || id;
  // Field path from a top field down to `id` (first parent at each step; the field graph is a DAG).
  const fieldPath = (id: string): string => {
    const chain = [id];
    for (
      let parent = data?.nodes.find((node) => node.id === id)?.parents?.[0];
      parent && !chain.includes(parent);
    ) {
      chain.unshift(parent);
      parent = data?.nodes.find((node) => node.id === parent)?.parents?.[0];
    }
    return chain.map(fieldName).join(' › ');
  };
  const allTypes = data ? [...new Set(data.nodes.map((node) => node.type))].sort() : [];

  return (
    <section className="graph-view" data-testid="graph-view" data-mode={mode}>
      <div className="graph-controls">
        <button
          type="button"
          data-testid="list-toggle"
          onClick={() => setList((current) => !current)}
        >
          {list ? '그래프 보기' : '목록 보기'}
        </button>
        {mode === 'atlas' &&
          allTypes.map((type) => (
            <label key={type}>
              <input
                type="checkbox"
                data-testid={`type-filter-${type}`}
                checked={enabledTypes?.has(type) || false}
                onChange={() =>
                  setEnabledTypes((current) => {
                    const next = new Set(current);
                    if (next.has(type)) next.delete(type);
                    else next.add(type);
                    return next;
                  })
                }
              />
              {type}
            </label>
          ))}
        {mode === 'atlas' && (
          <label>
            <input
              type="checkbox"
              data-testid="verified-only"
              checked={verifiedOnly}
              onChange={(event) => setVerifiedOnly(event.target.checked)}
            />
            검증된 관계만
          </label>
        )}
        {(mode === 'local' || mode === 'trace') && (
          <label>
            <input
              type="checkbox"
              checked={showCites}
              onChange={(event) => setShowCites(event.target.checked)}
            />
            인용 관계 보기
          </label>
        )}
      </div>

      {!data && !failed && <p>그래프를 불러오는 중…</p>}
      {failed && (
        <div role="alert">
          <p>그래프를 불러오지 못했습니다</p>
          {fallbackFields(topFields)}
        </div>
      )}
      {data &&
        (list ? (
          <table data-testid="graph-list">
            <thead>
              <tr>
                <th>노드</th>
                <th>유형</th>
                <th>상태</th>
                <th>도입 연도</th>
              </tr>
            </thead>
            <tbody>
              {projection.nodes.map((node) =>
                nodeRow(node, selectNode, mode === 'atlas' ? expanded : undefined),
              )}
            </tbody>
            <tbody>
              {projection.edges
                .filter((edge) => edge.kind === 'claim')
                .map((edge) => (
                  <tr key={edge.id} data-claim-id={edge.id}>
                    <td colSpan={2}>{edge.source}</td>
                    <td>{edge.predicate}</td>
                    <td>{edge.url && <a href={edge.url}>근거 보기</a>}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        ) : (
          <div className={`graph-canvas graph-canvas-${mode}`}>
            {trace && (
              <div className="graph-trace-labels" aria-hidden="true">
                <span>연도 미상</span>
                {[...new Set(trace.nodes.flatMap((node) => (node.year ? [node.year] : [])))].map(
                  (year) => (
                    <span key={year}>{year}</span>
                  ),
                )}
                {trace.lanes.map((lane) => (
                  <span key={lane}>{lane.replace(/^field:/, '')}</span>
                ))}
              </div>
            )}
            <ReactFlow<FlowGraphNode, FlowGraphEdge>
              nodes={flowNodes}
              edges={flowEdges}
              nodeTypes={nodeTypes}
              edgeTypes={edgeTypes}
              onInit={setFlow}
              nodesFocusable
              edgesFocusable={false}
              nodesDraggable={false}
              fitView
            >
              <Background />
              <Controls />
            </ReactFlow>
          </div>
        ))}

      {selectedNode && !selectedNode.synthetic && (
        <aside data-testid="node-panel" className="node-panel">
          <h2>{selectedNode.name}</h2>
          <p>{selectedNode.type}</p>
          <p className="badge">{selectedNode.status || 'active'}</p>
          <p>{selectedNode.summary || '준비 중'}</p>
          <p>도입 연도: {selectedNode.year || '연도 미상'}</p>
          {!!selectedNode.fields?.length && (
            <p>분야: {selectedNode.fields.map(fieldPath).join(', ')}</p>
          )}
          {!!selectedNode.paperTitles?.length && (
            <p>소개 논문: {selectedNode.paperTitles.join(', ')}</p>
          )}
          {selectedNode.url && (
            <a data-testid="panel-entity-link" href={selectedNode.url}>
              항목 상세 보기
            </a>
          )}
          {selectedNode.hasWiki && selectedNode.wikiUrl && (
            <a data-testid="panel-wiki-link" href={selectedNode.wikiUrl}>
              Wiki 읽기
            </a>
          )}
          {selectedNode.type === 'ResearchField' && mode === 'atlas' && (
            <button type="button" onClick={() => selectNode(selectedNode.id)}>
              {expanded.has(selectedNode.id) ? '접기' : '펼치기'}
            </button>
          )}
        </aside>
      )}
    </section>
  );
}
