/**
 * Ground truth for the tests: the graph YAML and wiki frontmatter read straight from disk.
 * Nothing here imports application code, so a bug in src/ cannot hide itself.
 */
import fs from 'node:fs';
import { parse } from 'yaml';
import { GRAPH_FILES, WIKI_DIR } from './env';

export interface Evidence {
  source?: string;
  locator?: Record<string, string | number>;
  quote?: string;
  rationale?: string;
  type: string;
  stance: 'supports' | 'contradicts' | 'qualifies';
}

export interface Review {
  by: string;
  at: string;
  decision: string;
  note?: string;
}

export interface Entity {
  id: string;
  name?: string;
  title?: string;
  summary?: string;
  summary_by?: string;
  summary_review?: Review;
  fields?: string[];
  parents?: string[];
  aliases?: string[];
  earliest_public_date?: string;
  fulltext_url?: string;
  url?: string;
  paper?: string;
  [key: string]: unknown;
}

export interface Claim extends Entity {
  predicate: string;
  subject: string;
  object: string;
  status: string;
  evidence?: Evidence[];
  qualifiers?: Record<string, string>;
  review?: Review | null;
  rejected_reason?: string;
}

export interface AssessmentItem extends Entity {
  kind: string;
  prompt: string;
  choices?: string[];
  answer: number;
  tolerance?: number;
  lab?: string;
}

const SECTIONS: Record<string, string> = {
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

/** Research predicates that the Trace view may draw (docs/05 section 4.3). */
export const RESEARCH_PREDICATES = [
  'INTRODUCES',
  'EXTENDS',
  'ADAPTS',
  'IMPROVES_ON',
  'ADDRESSES',
  'MITIGATES',
  'COMPARED_WITH',
];

export class GraphData {
  readonly entities = new Map<string, Entity>();
  readonly types = new Map<string, string>();

  constructor(files: string[]) {
    for (const file of files) {
      const document = parse(fs.readFileSync(file, 'utf8')) as Record<string, Entity[]>;
      for (const [section, type] of Object.entries(SECTIONS)) {
        for (const record of document[section] ?? []) {
          this.entities.set(record.id, record);
          this.types.set(record.id, type);
        }
      }
    }
  }

  get claims(): Claim[] {
    return this.ofType('Claim') as Claim[];
  }

  ofType(type: string): Entity[] {
    return [...this.entities.values()].filter((entity) => this.types.get(entity.id) === type);
  }

  entity(id: string): Entity {
    const found = this.entities.get(id);
    if (!found) throw new Error(`unknown graph id in test data: ${id}`);
    return found;
  }

  claim(id: string): Claim {
    return this.entity(id) as Claim;
  }

  name(id: string): string {
    const entity = this.entity(id);
    return String(entity.name ?? entity.title);
  }

  source(id: string): Entity {
    return this.entity(id);
  }

  /** Items of a lab, in the order the lab lists them. */
  labItems(labId: string): AssessmentItem[] {
    const lab = this.entity(labId) as Entity & { items: string[] };
    return lab.items.map((id) => this.entity(id) as AssessmentItem);
  }

  /** Verified INTRODUCES claim -> year of the earliest introducing paper. */
  introYear(id: string): number | undefined {
    const years = this.claims
      .filter((c) => c.predicate === 'INTRODUCES' && c.status === 'verified' && c.object === id)
      .map((c) => Number(String(this.entity(c.subject).earliest_public_date).slice(0, 4)));
    return years.length ? Math.min(...years) : undefined;
  }

  introducingPaper(id: string): Entity | undefined {
    const claim = this.claims.find(
      (c) => c.predicate === 'INTRODUCES' && c.status === 'verified' && c.object === id,
    );
    return claim ? this.entity(claim.subject) : undefined;
  }

  /** Verified PREREQUISITE_OF claims into an entity (hard prerequisites). */
  hardPrerequisites(id: string): string[] {
    return unique(
      this.claims
        .filter(
          (c) => c.status === 'verified' && c.predicate === 'PREREQUISITE_OF' && c.object === id,
        )
        .map((c) => c.subject),
    );
  }

  /** Verified RECOMMENDED_BEFORE claims into an entity (soft prerequisites). */
  softPrerequisites(id: string): string[] {
    return unique(
      this.claims
        .filter(
          (c) => c.status === 'verified' && c.predicate === 'RECOMMENDED_BEFORE' && c.object === id,
        )
        .map((c) => c.subject),
    );
  }

  /** Subjects of non-verified prerequisite claims into an entity (must never be listed). */
  unverifiedPrerequisites(id: string): string[] {
    const verified = new Set([...this.hardPrerequisites(id), ...this.softPrerequisites(id)]);
    return unique(
      this.claims
        .filter(
          (c) =>
            c.status !== 'verified' &&
            ['PREREQUISITE_OF', 'RECOMMENDED_BEFORE'].includes(c.predicate) &&
            c.object === id,
        )
        .map((c) => c.subject)
        .filter((subject) => !verified.has(subject)),
    );
  }

  /** Shortest chain of hard prerequisites leading from `from` back to `to` (from, ..., to). */
  prerequisitePath(from: string, to: string): string[] {
    const queue: string[][] = [[from]];
    const seen = new Set([from]);
    while (queue.length) {
      const path = queue.shift() as string[];
      const last = path[path.length - 1];
      if (last === to) return path;
      for (const next of this.hardPrerequisites(last)) {
        if (seen.has(next)) continue;
        seen.add(next);
        queue.push([...path, next]);
      }
    }
    throw new Error(`no prerequisite path from ${from} to ${to} in the test data`);
  }

  /** Fields to expand, outermost first, so that `id` becomes visible in the Atlas. */
  fieldChain(id: string, through?: string): string[] {
    const chains = (this.entity(id).fields ?? []).map((field) => this.ancestry(field, through));
    return chains.find((chain) => !through || chain.includes(through)) ?? chains[0] ?? [];
  }

  /** Chain of fields from a top field down to `field`, preferring the route through `through`. */
  private ancestry(field: string, through?: string): string[] {
    const parents = this.entity(field).parents ?? [];
    if (!parents.length) return [field];
    const preferred = through
      ? parents.find((parent) => this.ancestry(parent, through).includes(through))
      : undefined;
    return [...this.ancestry(preferred ?? parents[0], through), field];
  }
}

export function unique<T>(values: T[]): T[] {
  return [...new Set(values)];
}

let cached: GraphData | undefined;

/** The graph the running build was made from. */
export function graph(): GraphData {
  cached ??= new GraphData(GRAPH_FILES);
  return cached;
}

/** True for a human approval, the only approval the public build honours. */
export function humanApproved(record: { review?: Review | null }): boolean {
  return record.review?.decision === 'approve' && String(record.review?.by).startsWith('human:');
}

/** Frontmatter of a wiki document of the running build. */
export function wikiFrontmatter(slug: string, wikiDir = WIKI_DIR): Record<string, unknown> {
  const text = fs.readFileSync(`${wikiDir}/${slug}.mdx`, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) throw new Error(`no frontmatter in ${slug}.mdx`);
  return parse(match[1]) as Record<string, unknown>;
}

/** URL paths below the base, mirroring docs/CONTENT_SCHEMA.md section 6. */
export function entityPath(id: string): string {
  const [prefix, slug] = id.split(':');
  return prefix === 'field' ? `fields/${slug}/` : `e/${prefix}/${slug}/`;
}

export function claimPath(id: string): string {
  return `claims/${id.replace(/^clm:/, '')}/`;
}

export function wikiPath(slug: string): string {
  return `wiki/${slug}/`;
}

/** `#node-<id with ':' replaced by '~'>`. */
export function nodeAnchor(id: string): string {
  return `#node-${id.replace(/:/g, '~')}`;
}

/** Collapse whitespace the way a browser renders it. */
export function normalize(text: string | null | undefined): string {
  return String(text ?? '')
    .replace(/\s+/g, ' ')
    .trim();
}
