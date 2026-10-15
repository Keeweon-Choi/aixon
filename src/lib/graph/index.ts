import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';
import type { BuildMode, GraphData, RecordMap, VisibleKind, WikiRecord } from './types';

const sections: Record<string, string> = {
  fields: 'ResearchField',
  problems: 'ResearchProblem',
  concepts: 'Concept',
  methods: 'Method',
  models: 'Model',
  papers: 'Paper',
  datasets: 'Dataset',
  metrics: 'Metric',
  benchmarks: 'Benchmark',
  objectives: 'LearningObjective',
  resources: 'LearningResource',
  assessment_items: 'AssessmentItem',
  labs: 'LabExperiment',
  sources: 'Source',
  claims: 'Claim',
};
const arraySections = Object.keys(sections);
const entityTypes = new Set(
  Object.values(sections).filter((type) => !['Claim', 'Source'].includes(type)),
);
const asArray = (value: unknown): unknown[] => (Array.isArray(value) ? value : []);
const str = (value: unknown): string => (typeof value === 'string' ? value : '');
const record = (value: unknown): RecordMap =>
  value && typeof value === 'object' && !Array.isArray(value) ? (value as RecordMap) : {};
const sha256 = (filename: string): string =>
  crypto.createHash('sha256').update(fs.readFileSync(filename)).digest('hex');

interface PublicGate {
  graph_files: unknown;
  inputs: unknown;
  entities: unknown;
  claims: unknown;
  wiki: unknown;
  sources: unknown;
}

function stringSet(value: unknown, label: string): Set<string> {
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string'))
    throw new Error(`invalid public gate: ${label}`);
  return new Set(value);
}
function exactArray(actual: unknown, expected: string[]): void {
  if (
    !Array.isArray(actual) ||
    actual.length !== expected.length ||
    actual.some((item, index) => item !== expected[index])
  )
    throw new Error('stale public gate: run python tools/public_gate.py');
}
function readMode(build?: BuildMode): BuildMode {
  const mode = build ?? process.env.AIXON_BUILD;
  if (mode !== 'preview' && mode !== 'public')
    throw new Error('AIXON_BUILD must be exactly preview or public');
  return mode;
}
function readWikis(wikiDir: string): WikiRecord[] {
  if (!fs.existsSync(wikiDir)) return [];
  return fs
    .readdirSync(wikiDir)
    .filter((filename) => filename.endsWith('.mdx'))
    .sort()
    .map((filename) => {
      const full = path.join(wikiDir, filename);
      const match = fs.readFileSync(full, 'utf8').match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
      const metadata = record(match ? parse(match[1]) : {});
      return {
        ...metadata,
        id: str(metadata.id),
        entity: str(metadata.entity),
        status: str(metadata.status),
        filename: full,
      };
    })
    .filter((wiki) => wiki.id && wiki.entity);
}
function validatePublicGate(paths: string[], wikis: WikiRecord[]): PublicGate {
  const gatePath = process.env.AIXON_PUBLIC_GATE || '.aixon/public-gate.json';
  if (!fs.existsSync(gatePath))
    throw new Error('stale public gate: run python tools/public_gate.py');
  let gate: PublicGate;
  try {
    gate = JSON.parse(fs.readFileSync(gatePath, 'utf8')) as PublicGate;
  } catch {
    throw new Error('stale public gate: run python tools/public_gate.py');
  }
  exactArray(gate.graph_files, paths);
  const inputs = record(gate.inputs);
  const expected = [...paths, ...wikis.map((wiki) => wiki.filename)];
  const sortedExpected = [...expected].sort();
  const keys = Object.keys(inputs).sort();
  if (
    keys.length !== sortedExpected.length ||
    keys.some((key, index) => key !== sortedExpected[index])
  )
    throw new Error('stale public gate: run python tools/public_gate.py');
  for (const input of expected) {
    if (
      typeof inputs[input] !== 'string' ||
      !fs.existsSync(input) ||
      inputs[input] !== sha256(input)
    )
      throw new Error('stale public gate: run python tools/public_gate.py');
  }
  stringSet(gate.entities, 'entities');
  stringSet(gate.claims, 'claims');
  stringSet(gate.wiki, 'wiki');
  stringSet(gate.sources, 'sources');
  return gate;
}

export function graphPaths(env: Record<string, string | undefined> = process.env): string[] {
  return (env.AIXON_GRAPH || 'data/seed/seed_graph.yaml,data/graph/atlas.yaml')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}
export function loadGraph(paths = graphPaths(), build?: BuildMode): GraphData {
  const mode = readMode(build);
  const raw: RecordMap = {};
  for (const section of arraySections) raw[section] = [];
  for (const input of paths) {
    if (!fs.existsSync(input)) throw new Error(`graph file missing: ${input}`);
    const part = record(parse(fs.readFileSync(input, 'utf8')));
    for (const section of arraySections)
      (raw[section] as unknown[]).push(...asArray(part[section]));
  }
  const records: Record<string, RecordMap> = {};
  const types: Record<string, string> = {};
  for (const section of arraySections)
    for (const item of asArray(raw[section])) {
      const value = record(item);
      const id = str(value.id);
      if (!id) continue;
      if (records[id]) throw new Error(`duplicate graph id: ${id}`);
      records[id] = value;
      types[id] = sections[section];
    }
  const allEntities = Object.fromEntries(
    Object.entries(records).filter(([id]) => entityTypes.has(types[id])),
  );
  const allClaims = Object.fromEntries(
    Object.entries(records).filter(([id]) => types[id] === 'Claim'),
  );
  const allSources = Object.fromEntries(
    Object.entries(records).filter(([id]) => types[id] === 'Source'),
  );
  const loadedWikis = readWikis(process.env.AIXON_WIKI_DIR || 'src/content/wiki');
  const gate = mode === 'public' ? validatePublicGate(paths, loadedWikis) : undefined;
  const gateIds = (key: keyof Pick<PublicGate, 'entities' | 'claims' | 'wiki' | 'sources'>) =>
    gate ? stringSet(gate[key], key) : undefined;
  const entityIds = gateIds('entities');
  const claimIds = gateIds('claims');
  const wikiIds = gateIds('wiki');
  const sourceIds = gateIds('sources');
  const entities = Object.fromEntries(
    Object.entries(allEntities).filter(([id]) => mode === 'preview' || entityIds?.has(id)),
  );
  const emittedClaims = Object.fromEntries(
    Object.entries(allClaims).filter(([id]) => mode === 'preview' || claimIds?.has(id)),
  );
  const claims = Object.fromEntries(
    Object.entries(emittedClaims).filter(
      ([, claim]) => !['rejected', 'deprecated'].includes(str(claim.status)),
    ),
  );
  const sources = Object.fromEntries(
    Object.entries(allSources).filter(([id]) => mode === 'preview' || sourceIds?.has(id)),
  );
  const wikis = Object.fromEntries(
    loadedWikis
      .filter((wiki) => mode === 'preview' || wikiIds?.has(wiki.id))
      .map((wiki) => [wiki.id, wiki]),
  );
  const isVisible = (kind: VisibleKind, id: string): boolean =>
    kind === 'entity'
      ? Boolean(entities[id])
      : kind === 'claim'
        ? Boolean(emittedClaims[id])
        : kind === 'source'
          ? Boolean(sources[id])
          : Boolean(wikis[id]);
  const wikiFor = (entityId: string): WikiRecord | undefined =>
    Object.values(wikis).find((wiki) => wiki.entity === entityId);
  const visibleClaimsOf = (entityId: string): RecordMap[] =>
    Object.values(claims).filter(
      (claim) => str(claim.subject) === entityId || str(claim.object) === entityId,
    );
  const claimsBySubject: Record<string, RecordMap[]> = {};
  const claimsByObject: Record<string, RecordMap[]> = {};
  const prerequisites: Record<string, RecordMap[]> = {};
  for (const claim of Object.values(claims)) {
    const subject = str(claim.subject);
    const object = str(claim.object);
    (claimsBySubject[subject] ||= []).push(claim);
    (claimsByObject[object] ||= []).push(claim);
    if (
      ['PREREQUISITE_OF', 'RECOMMENDED_BEFORE'].includes(str(claim.predicate)) &&
      str(claim.status) === 'verified'
    ) {
      const dimension = str(record(claim.qualifiers).for_dimension) || 'explain';
      (prerequisites[`${object}@${dimension}`] ||= []).push(claim);
    }
  }
  const fields: Record<string, RecordMap> = {};
  const parents: Record<string, string[]> = {};
  const memberships: Record<string, string[]> = {};
  for (const [id, item] of Object.entries(entities)) {
    if (types[id] === 'ResearchField') {
      fields[id] = item;
      parents[id] = asArray(item.parents)
        .map(str)
        .filter((parent) => Boolean(entities[parent]));
    }
    for (const field of asArray(item.fields).map(str))
      if (types[field] === 'ResearchField' && entities[field]) (memberships[field] ||= []).push(id);
  }
  const introYears: Record<string, number> = {};
  for (const claim of Object.values(claims))
    if (str(claim.predicate) === 'INTRODUCES' && str(claim.status) === 'verified') {
      const paper = entities[str(claim.subject)];
      const year = Number(
        str(paper?.earliest_public_date || paper?.publication_date || paper?.date).slice(0, 4),
      );
      const object = str(claim.object);
      if (Number.isFinite(year)) introYears[object] = Math.min(introYears[object] ?? year, year);
    }
  return {
    raw,
    entities,
    allEntities,
    types,
    claims,
    emittedClaims,
    allClaims,
    sources,
    wikis,
    fields,
    parents,
    memberships,
    claimsBySubject,
    claimsByObject,
    introYears,
    prerequisites,
    build: mode,
    isVisible,
    wikiFor,
    visibleClaimsOf,
  };
}
let cached: GraphData | undefined;
export function getGraph(): GraphData {
  return (cached ||= loadGraph());
}
export function entityPath(id: string, graph = getGraph()): string {
  const [prefix, slug] = id.split(':');
  return graph.types[id] === 'ResearchField' || prefix === 'field'
    ? `fields/${slug}/`
    : `e/${prefix}/${slug}/`;
}
export function claimPath(id: string): string {
  return `claims/${id.replace(/^clm:/, '')}/`;
}
