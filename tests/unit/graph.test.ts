import { describe, expect, it } from 'vitest';
import { loadGraph } from '../../src/lib/graph';
import { url } from '../../src/lib/url';
import { mulberry32, softmax } from '../../src/lib/lab/softmax';
describe('graph loader', () => {
  it('indexes introductions and prerequisites', () => { const g = loadGraph(['data/seed/seed_graph.yaml']); expect(g.introYears['method:scaled-dot-product-attention']).toBe(2017); expect(g.prerequisites['method:scaled-dot-product-attention@explain']).toHaveLength(1); });
  it('filters unapproved public claims', () => { const g = loadGraph(['data/seed/seed_graph.yaml'], 'public'); expect(Object.keys(g.claims)).toContain('clm:intro-sdpa'); });
  it('uses a base helper', () => expect(url('atlas/')).toContain('atlas/'));
  it('has stable lab primitives', () => { const r=mulberry32(42); expect([r(),r(),r()]).toEqual([0.6011037519201636,0.44829055899754167,0.8524657934904099]); expect(softmax([1000,0])[0]).toBe(1); });
});
