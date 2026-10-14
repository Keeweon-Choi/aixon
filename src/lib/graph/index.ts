import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';
import type { GraphData, RecordMap } from './types';

const sections: Record<string, string> = {
  fields: 'ResearchField', problems: 'ResearchProblem', concepts: 'Concept', methods: 'Method', models: 'Model', papers: 'Paper', datasets: 'Dataset', metrics: 'Metric', benchmarks: 'Benchmark', objectives: 'LearningObjective', resources: 'LearningResource', assessment_items: 'AssessmentItem', labs: 'LabExperiment', sources: 'Source', claims: 'Claim',
};
const arraySections = Object.keys(sections);
const asArray = (v: unknown) => Array.isArray(v) ? v : [];
const str = (v: unknown) => typeof v === 'string' ? v : '';
const record = (v: unknown): RecordMap => v && typeof v === 'object' && !Array.isArray(v) ? v as RecordMap : {};

export function graphPaths(env: Record<string, string | undefined> = process.env): string[] {
  return (env.AIXON_GRAPH || 'data/seed/seed_graph.yaml,data/graph/atlas.yaml').split(',').map(x => x.trim()).filter(Boolean);
}

export function loadGraph(paths = graphPaths(), build = (process.env.AIXON_BUILD === 'public' ? 'public' : 'preview') as GraphData['build']): GraphData {
  const raw: RecordMap = {}; for (const section of arraySections) raw[section] = [];
  for (const input of paths) {
    const filename = path.resolve(input);
    if (!fs.existsSync(filename)) { console.warn(`[aixon] graph file skipped: ${input}`); continue; }
    const part = record(parse(fs.readFileSync(filename, 'utf8')));
    for (const section of arraySections) (raw[section] as unknown[]).push(...asArray(part[section]));
  }
  const entities: Record<string, RecordMap> = {}, types: Record<string, string> = {};
  for (const section of arraySections) for (const item of asArray(raw[section])) {
    const value = record(item), id = str(value.id); if (!id) continue;
    if (entities[id]) throw new Error(`duplicate graph id: ${id}`);
    entities[id] = value; types[id] = sections[section];
  }
  const claims = Object.fromEntries(Object.entries(entities).filter(([id]) => types[id] === 'Claim'));
  const sources = Object.fromEntries(Object.entries(entities).filter(([id]) => types[id] === 'Source'));
  const allowed = (c: RecordMap) => build === 'public' ? record(c.review).decision === 'approve' : !['rejected', 'deprecated'].includes(str(c.status));
  const visibleClaims = Object.fromEntries(Object.entries(claims).filter(([, c]) => allowed(c)));
  const claimsBySubject: Record<string, RecordMap[]> = {}, claimsByObject: Record<string, RecordMap[]> = {}, prerequisites: Record<string, RecordMap[]> = {};
  for (const c of Object.values(visibleClaims)) { const s = str(c.subject), o = str(c.object); (claimsBySubject[s] ||= []).push(c); (claimsByObject[o] ||= []).push(c);
    if (['PREREQUISITE_OF', 'RECOMMENDED_BEFORE'].includes(str(c.predicate)) && str(c.status) === 'verified') (prerequisites[`${o}@${str(record(c.qualifiers).for_dimension) || 'explain'}`] ||= []).push(c);
  }
  const fields: Record<string, RecordMap> = {}, parents: Record<string, string[]> = {}, memberships: Record<string, string[]> = {};
  for (const [id, item] of Object.entries(entities)) { if (types[id] === 'ResearchField') { fields[id] = item; parents[id] = asArray(item.parents).map(str); } for (const f of asArray(item.fields).map(str)) (memberships[f] ||= []).push(id); }
  const introYears: Record<string, number> = {};
  for (const c of Object.values(visibleClaims)) if (c.predicate === 'INTRODUCES' && c.status === 'verified') { const date = str(entities[str(c.subject)]?.earliest_public_date); const y = Number(date.slice(0, 4)); if (Number.isFinite(y)) { const o = str(c.object); introYears[o] = Math.min(introYears[o] ?? y, y); } }
  return { raw, entities, types, claims: visibleClaims, sources, fields, parents, memberships, claimsBySubject, claimsByObject, introYears, prerequisites, build };
}

let cached: GraphData | undefined;
export function getGraph() { return cached ||= loadGraph(); }
export function entityPath(id: string, graph = getGraph()): string { const [prefix, slug] = id.split(':'); return prefix === 'field' ? `fields/${slug}/` : `e/${prefix}/${slug}/`; }
export function claimPath(id: string): string { return `claims/${id.replace(/^clm:/, '')}/`; }
