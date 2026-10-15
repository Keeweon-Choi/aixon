import { describe, expect, it } from 'vitest';
import { coverageRows } from '../../src/lib/coverage';

const graph: any = {
  fields: {
    'field:root': { name: 'Root' },
    'field:left': {},
    'field:right': {},
    'field:shared': {},
  },
  parents: {
    'field:left': ['field:root'],
    'field:right': ['field:root'],
    'field:shared': ['field:left', 'field:right'],
  },
  memberships: { 'field:shared': ['method:one'], 'field:right': ['paper:two'] },
  entities: { 'method:one': {}, 'paper:two': {} },
  types: { 'method:one': 'Method', 'paper:two': 'Paper' },
  claims: {
    'clm:one': { subject: 'method:one', object: 'paper:two', status: 'verified', verification: {} },
  },
  wikiFor: (id: string) => (id === 'method:one' ? { status: 'draft' } : undefined),
};
describe('coverage aggregation', () => {
  it('deduplicates a shared DAG descendant and counts missing wiki and endpoint claims', () => {
    const { rows } = coverageRows(graph);
    const root = rows.find((row) => row.fieldId === 'field:root')!;
    expect(root.entities).toBe(2);
    expect(root.wiki.draft).toBe(1);
    expect(root.wiki.missing).toBe(1);
    expect(root.citedClaims).toBe(1);
  });
});
