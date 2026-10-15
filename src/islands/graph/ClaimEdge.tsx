import {
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  type Edge,
  type EdgeProps,
} from '@xyflow/react';
import type { EdgeStyle, GraphEdge } from '../../lib/graph/view';

export type ClaimEdgeData = {
  edge: GraphEdge;
  style: EdgeStyle;
  label: string;
};

type FlowClaimEdge = Edge<ClaimEdgeData, 'claim'>;

export default function ClaimEdge({
  sourceX,
  sourceY,
  sourcePosition,
  targetX,
  targetY,
  targetPosition,
  data,
}: EdgeProps<FlowClaimEdge>) {
  const [path, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });
  if (!data) return null;
  const edgeStyle = {
    stroke: data.style.muted ? 'var(--graph-muted)' : 'var(--graph-edge)',
    strokeDasharray: data.style.dash,
    strokeWidth: data.style.strokeWidth,
  };
  return (
    <>
      <BaseEdge path={path} style={edgeStyle} />
      {data.label && data.edge.url && (
        <EdgeLabelRenderer>
          <a
            className="aixon-edge-label nopan"
            data-claim-id={data.edge.id}
            href={data.edge.url}
            style={{ transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)` }}
          >
            {data.label}
          </a>
        </EdgeLabelRenderer>
      )}
    </>
  );
}
