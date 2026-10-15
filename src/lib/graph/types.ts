export type RecordMap = Record<string, unknown>;

export type BuildMode = 'preview' | 'public';
export type VisibleKind = 'entity' | 'claim' | 'wiki' | 'source';

export interface WikiRecord {
  id: string;
  entity: string;
  filename: string;
  status: string;
  [key: string]: unknown;
}

export interface GraphData {
  raw: RecordMap;
  entities: Record<string, RecordMap>;
  allEntities: Record<string, RecordMap>;
  types: Record<string, string>;
  claims: Record<string, RecordMap>;
  emittedClaims: Record<string, RecordMap>;
  allClaims: Record<string, RecordMap>;
  sources: Record<string, RecordMap>;
  wikis: Record<string, WikiRecord>;
  fields: Record<string, RecordMap>;
  parents: Record<string, string[]>;
  memberships: Record<string, string[]>;
  claimsBySubject: Record<string, RecordMap[]>;
  claimsByObject: Record<string, RecordMap[]>;
  introYears: Record<string, number>;
  prerequisites: Record<string, RecordMap[]>;
  build: BuildMode;
  isVisible: (kind: VisibleKind, id: string) => boolean;
  wikiFor: (entityId: string) => WikiRecord | undefined;
  visibleClaimsOf: (entityId: string) => RecordMap[];
}
