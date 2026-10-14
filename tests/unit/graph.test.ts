import { describe, expect, it } from 'vitest';
import { loadGraph } from '../../src/lib/graph';
import { url } from '../../src/lib/url';
describe('graph loader', () => {
  it('indexes introductions and prerequisites', () => { const g = loadGraph(['data/seed/seed_graph.yaml']); expect(g.introYears['method:scaled-dot-product-attention']).toBe(2017); expect(g.prerequisites['method:scaled-dot-product-attention@explain']).toHaveLength(1); });
  it('filters unapproved public claims', () => { const g = loadGraph(['data/seed/seed_graph.yaml'], 'public'); expect(Object.keys(g.claims)).toContain('clm:intro-sdpa'); });
  it('uses a base helper', () => expect(url('atlas/')).toContain('atlas/'));
});
