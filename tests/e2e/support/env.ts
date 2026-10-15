/** Which build the E2E suite runs against, and where its servers and data live. */

export type Target = 'fixture' | 'seed';

export const BASE_PATH = '/aixon/';
export const SITE = 'http://127.0.0.1:4329';
export const PORTS = { fixture: 4329, seed: 4330, public: 4331 } as const;
export const DIST = { fixture: 'dist-e2e', seed: 'dist-seed', public: 'dist-public-e2e' } as const;

export const target: Target = process.env.AIXON_E2E_TARGET === 'seed' ? 'seed' : 'fixture';
export const isSeed = target === 'seed';

export const origin = `http://127.0.0.1:${PORTS[target]}`;
export const publicOrigin = `http://127.0.0.1:${PORTS.public}`;

/** The graph and wiki sources the running build was made from (used to compute expectations). */
export const GRAPH_FILES = isSeed
  ? ['data/seed/seed_graph.yaml', 'data/graph/atlas.yaml']
  : ['tests/fixtures/graph/site_graph.yaml'];
export const WIKI_DIR = isSeed ? 'src/content/wiki' : 'tests/fixtures/wiki';

/**
 * Quick-search queries. "어텐션" is the query of CONTENT_VALIDATION_PLAN E2E-1: it matches many attention
 * nodes, and nodes with a wiki rank first among equal scores, so SDPA stays in the top 8 on the real seed.
 * "어텐" is the 2-character query that must still find nodes.
 */
export const QUICK_QUERY = { main: '어텐션', short: '어텐' };

/** A word that only the draft SDPA fixture document contains (Pagefind and public-gate tests). */
export const FIXTURE_UNIQUE_WORD = '픽스처어텐션';
