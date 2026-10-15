import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { loadGraph } from '../../src/lib/graph';

const original = {
  build: process.env.AIXON_BUILD,
  gate: process.env.AIXON_PUBLIC_GATE,
  wiki: process.env.AIXON_WIKI_DIR,
};
const digest = (filename: string) =>
  crypto.createHash('sha256').update(fs.readFileSync(filename)).digest('hex');

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'aixon-graph-'));
  const graph = path.join(root, 'graph.yaml');
  const wikiDir = path.join(root, 'wiki');
  const wiki = path.join(wikiDir, 'alpha.mdx');
  fs.mkdirSync(wikiDir);
  fs.writeFileSync(
    graph,
    `fields:\n  - id: field:ml\n    name: ML\nmethods:\n  - id: method:alpha\n    name: Alpha\n    aliases: [알파]\n    fields: [field:ml]\n  - id: method:beta\n    name: Beta\n    fields: [field:ml]\npapers:\n  - id: paper:old\n    name: Old\n    earliest_public_date: 2017-06-01\n  - id: paper:new\n    name: New\n    earliest_public_date: 2018-01-01\nsources:\n  - id: src:test\n    name: Test source\nclaims:\n  - id: clm:intro-old\n    subject: paper:old\n    predicate: INTRODUCES\n    object: method:alpha\n    status: verified\n  - id: clm:intro-new\n    subject: paper:new\n    predicate: INTRODUCES\n    object: method:alpha\n    status: verified\n  - id: clm:prereq\n    subject: method:beta\n    predicate: PREREQUISITE_OF\n    object: method:alpha\n    status: verified\n    qualifiers: {for_dimension: derive}\n  - id: clm:rejected\n    subject: method:alpha\n    predicate: EXTENDS\n    object: method:beta\n    status: rejected\n  - id: clm:approved-looking\n    subject: method:alpha\n    predicate: EXTENDS\n    object: method:beta\n    status: verified\n    review: {decision: approve}\n`,
  );
  fs.writeFileSync(
    wiki,
    `---\nid: wiki:alpha\nentity: method:alpha\ntitle: Alpha\nstatus: published\n---\nAlpha\n`,
  );
  return { root, graph, wikiDir, wiki };
}

function writeGate(
  paths: { graph: string; wiki: string; root: string },
  changes: Record<string, unknown> = {},
) {
  const gate = path.join(paths.root, 'gate.json');
  const data = {
    graph_files: [paths.graph],
    inputs: { [paths.graph]: digest(paths.graph), [paths.wiki]: digest(paths.wiki) },
    entities: ['field:ml', 'method:alpha', 'method:beta', 'paper:old', 'paper:new'],
    claims: ['clm:intro-old', 'clm:prereq'],
    wiki: ['wiki:alpha'],
    sources: ['src:test'],
    ...changes,
  };
  fs.writeFileSync(gate, JSON.stringify(data));
  return gate;
}

afterEach(() => {
  process.env.AIXON_BUILD = original.build;
  process.env.AIXON_PUBLIC_GATE = original.gate;
  process.env.AIXON_WIKI_DIR = original.wiki;
});

describe('graph loader', () => {
  it('fails closed for missing or unknown build mode', () => {
    const data = fixture();
    delete process.env.AIXON_BUILD;
    expect(() => loadGraph([data.graph])).toThrow('AIXON_BUILD');
    process.env.AIXON_BUILD = 'staging';
    expect(() => loadGraph([data.graph])).toThrow('AIXON_BUILD');
  });

  it('requires a current public gate', () => {
    const data = fixture();
    process.env.AIXON_WIKI_DIR = data.wikiDir;
    process.env.AIXON_PUBLIC_GATE = path.join(data.root, 'missing.json');
    expect(() => loadGraph([data.graph], 'public')).toThrow('stale public gate');
    process.env.AIXON_PUBLIC_GATE = writeGate({ ...data });
    fs.writeFileSync(data.graph, `${fs.readFileSync(data.graph, 'utf8')}\n`);
    expect(() => loadGraph([data.graph], 'public')).toThrow('stale public gate');
  });

  it('uses exactly gate ids in public and excludes approved-looking extras', () => {
    const data = fixture();
    process.env.AIXON_WIKI_DIR = data.wikiDir;
    process.env.AIXON_PUBLIC_GATE = writeGate({ ...data });
    const graph = loadGraph([data.graph], 'public');
    expect(Object.keys(graph.entities)).toEqual([
      'field:ml',
      'method:alpha',
      'method:beta',
      'paper:old',
      'paper:new',
    ]);
    expect(Object.keys(graph.emittedClaims)).toEqual(['clm:intro-old', 'clm:prereq']);
    expect(graph.isVisible('claim', 'clm:approved-looking')).toBe(false);
    expect(graph.wikiFor('method:alpha')?.id).toBe('wiki:alpha');
  });

  it('keeps rejected claim pages only in preview lists', () => {
    const data = fixture();
    const graph = loadGraph([data.graph], 'preview');
    expect(graph.isVisible('claim', 'clm:rejected')).toBe(true);
    expect(graph.visibleClaimsOf('method:alpha').map((claim) => claim.id)).not.toContain(
      'clm:rejected',
    );
  });

  it('rejects duplicate ids and derives introductions and dimensions', () => {
    const data = fixture();
    const graph = loadGraph([data.graph], 'preview');
    expect(graph.introYears['method:alpha']).toBe(2017);
    expect(graph.prerequisites['method:alpha@derive']).toHaveLength(1);
    const duplicate = path.join(data.root, 'duplicate.yaml');
    fs.writeFileSync(duplicate, 'methods:\n  - id: method:alpha\n');
    expect(() => loadGraph([data.graph, duplicate], 'preview')).toThrow('duplicate graph id');
  });

  it('makes wiki visibility mode-dependent', () => {
    const data = fixture();
    process.env.AIXON_WIKI_DIR = data.wikiDir;
    const preview = loadGraph([data.graph], 'preview');
    expect(preview.wikiFor('method:alpha')?.id).toBe('wiki:alpha');
    process.env.AIXON_PUBLIC_GATE = writeGate({ ...data }, { wiki: [] });
    const publicGraph = loadGraph([data.graph], 'public');
    expect(publicGraph.wikiFor('method:alpha')).toBeUndefined();
  });
});
