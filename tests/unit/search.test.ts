import { describe, expect, it } from 'vitest';
import { searchNodes } from '../../src/lib/search';

const nodes = [
  {
    id: 'method:scaled-dot-product-attention',
    name: 'Scaled Dot-Product Attention',
    aliases: ['스케일드 닷 프로덕트 어텐션'],
    type: '방법',
    url: '/one/',
  },
  { id: 'method:attention', name: '어텐션', aliases: ['Attention'], type: '방법', url: '/two/' },
  { id: 'concept:scale', name: '스케일', aliases: [], type: '개념', url: '/three/' },
];
describe('node quick search', () => {
  it('matches Korean substrings and aliases', () => {
    expect(searchNodes(nodes, '어텐').map((node) => node.id)).toContain('method:attention');
    expect(searchNodes(nodes, '스케일드')[0].id).toBe('method:scaled-dot-product-attention');
  });
  it('ranks exact/prefix before id matches', () => {
    expect(searchNodes(nodes, 'attention')[0].id).toBe('method:attention');
  });
});
