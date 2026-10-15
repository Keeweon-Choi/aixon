import { describe, expect, it } from 'vitest';
import {
  atlasVisible,
  dagreLayout,
  localNeighbourhood,
  nodeAnchor,
  parseNodeAnchor,
  traceLayout,
  type GraphViewData,
} from '../../src/lib/graph/view';

const node = (id: string, type: string, extra: Partial<GraphViewData['nodes'][number]> = {}) => ({
  id,
  type,
  name: id,
  status: 'active',
  ...extra,
});

const claim = (
  id: string,
  source: string,
  target: string,
  predicate: string,
  status = 'verified',
) => ({
  id,
  kind: 'claim' as const,
  source,
  target,
  predicate,
  status,
  reviewed: true,
  url: `/claims/${id}/`,
});

describe('graph view helpers', () => {
  it('round-trips node anchors including punctuation in ids', () => {
    for (const id of ['model:vit', 'method:scaled-dot-product-attention', 'concept:layer.norm-v2'])
      expect(parseNodeAnchor(nodeAnchor(id))).toBe(id);
    expect(parseNodeAnchor('#not-a-node')).toBeUndefined();
  });

  it('reveals child fields and members only after their field is expanded', () => {
    const data: GraphViewData = {
      nodes: [
        node('field:ai', 'ResearchField', { parents: [] }),
        node('field:vision', 'ResearchField', { parents: ['field:ai'] }),
        node('model:vit', 'Model', { fields: ['field:ai'] }),
      ],
      edges: [],
    };
    expect(atlasVisible(data, new Set(), {}).nodes.map((item) => item.id)).toEqual(['field:ai']);
    expect(atlasVisible(data, new Set(['field:ai']), {}).nodes.map((item) => item.id)).toEqual([
      'field:ai',
      'field:vision',
      'model:vit',
    ]);
  });

  it('caps atlas results and labels the omitted count', () => {
    const members = Array.from({ length: 81 }, (_, index) =>
      node(`model:m${index}`, 'Model', { fields: ['field:ai'] }),
    );
    const data: GraphViewData = {
      nodes: [node('field:ai', 'ResearchField', { parents: [] }), ...members],
      edges: [],
    };
    const result = atlasVisible(data, new Set(['field:ai']), {});
    expect(result.nodes).toHaveLength(81);
    expect(result.hiddenCount).toBe(2);
    expect(result.nodes.at(-1)?.name).toBe('+2개 더');
  });

  it('removes proposed claims with the verified-only filter', () => {
    const data: GraphViewData = {
      nodes: [
        node('field:ai', 'ResearchField', { parents: [] }),
        node('model:a', 'Model', { fields: ['field:ai'] }),
        node('model:b', 'Model', { fields: ['field:ai'] }),
      ],
      edges: [
        claim('clm:verified', 'model:a', 'model:b', 'EXTENDS'),
        claim('clm:proposed', 'model:b', 'model:a', 'ADAPTS', 'proposed'),
      ],
    };
    const result = atlasVisible(data, new Set(['field:ai']), { verifiedOnly: true });
    expect(result.edges.map((edge) => edge.id)).toEqual(['clm:verified']);
  });

  it('keeps research and prerequisite neighbours but omits CITES by default', () => {
    const data: GraphViewData = {
      nodes: [
        node('model:vit', 'Model'),
        node('model:transformer', 'Model'),
        node('paper:vit', 'Paper'),
      ],
      edges: [
        claim('clm:adapt', 'model:vit', 'model:transformer', 'ADAPTS'),
        claim('clm:cites', 'paper:vit', 'model:vit', 'CITES'),
      ],
    };
    expect(localNeighbourhood(data, 'model:vit').nodes.map((item) => item.id)).toEqual([
      'model:vit',
      'model:transformer',
    ]);
  });

  it('keeps ADAPTS ViT ← Transformer without creating influence from CITES', () => {
    const data: GraphViewData = {
      nodes: [
        node('paper:vaswani', 'Paper', { name: 'Transformer paper' }),
        node('model:transformer', 'Model', { fields: ['field:nlp'], year: 2017 }),
        node('model:vit', 'Model', { fields: ['field:vision'], year: 2020 }),
        node('paper:citing', 'Paper', { name: 'Citing paper' }),
        node('paper:cited', 'Paper', { name: 'Cited paper' }),
      ],
      edges: [
        claim('clm:intro-transformer', 'paper:vaswani', 'model:transformer', 'INTRODUCES'),
        claim('clm:vit-adapts-transformer', 'model:vit', 'model:transformer', 'ADAPTS'),
        claim('clm:cites-only', 'paper:citing', 'paper:cited', 'CITES'),
      ],
    };
    const result = traceLayout(data);
    expect(result.edges.map((edge) => edge.id)).toEqual(['clm:vit-adapts-transformer']);
    expect(result.nodes.map((item) => item.id)).toEqual(['model:transformer', 'model:vit']);
    expect(result.nodes[0].paperTitles).toEqual(['Transformer paper']);
  });

  it('orders trace positions by introduction year and puts unknown dates at the left', () => {
    const data: GraphViewData = {
      nodes: [
        node('model:old', 'Model', { fields: ['field:vision'], year: 2017 }),
        node('model:new', 'Model', { fields: ['field:vision'], year: 2020 }),
        node('problem:unknown', 'ResearchProblem', { fields: ['field:problems'] }),
      ],
      edges: [
        claim('clm:extends', 'model:new', 'model:old', 'EXTENDS'),
        claim('clm:addresses', 'model:new', 'problem:unknown', 'ADDRESSES'),
      ],
    };
    const result = traceLayout(data);
    const positions = Object.fromEntries(result.nodes.map((item) => [item.id, item.position.x]));
    expect(positions['problem:unknown']).toBeLessThan(positions['model:old']);
    expect(positions['model:new']).toBeGreaterThan(positions['model:old']);
  });

  it('uses distinct dagre positions for connected nodes', () => {
    const nodes = dagreLayout([{ id: 'a' }, { id: 'b' }], [{ source: 'a', target: 'b' }]);
    expect(nodes[0].position).not.toEqual(nodes[1].position);
  });
});
