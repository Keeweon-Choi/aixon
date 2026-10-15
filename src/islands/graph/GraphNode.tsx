import { Handle, Position, type Node, type NodeProps } from '@xyflow/react';
import type { KeyboardEvent } from 'react';
import { memo } from 'react';
import type { GraphNode as GraphNodeData } from '../../lib/graph/view';

export type FlowNodeData = {
  node: GraphNodeData;
  expanded: boolean;
  activate: (id: string) => void;
};

export type FlowNode = Node<FlowNodeData, 'graph'>;

function GraphNode({ data, selected }: NodeProps<FlowNode>) {
  const { node } = data;
  const field = node.type === 'ResearchField';
  const activate = (event: KeyboardEvent<HTMLButtonElement>) => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    event.preventDefault();
    data.activate(node.id);
  };
  return (
    <div className={`aixon-flow-node ${selected ? 'is-selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <button
        type="button"
        className="nodrag nopan"
        data-node-id={node.id}
        data-year={node.year}
        aria-label={`${node.type} ${node.name} ${node.status || 'active'}`}
        aria-expanded={field ? data.expanded : undefined}
        onClick={() => data.activate(node.id)}
        onKeyDown={activate}
      >
        <span>{node.name}</span>
        {node.year && <small>{node.year}</small>}
        {node.synthetic && <small>펼쳐서 계속 보기</small>}
      </button>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export default memo(GraphNode);
