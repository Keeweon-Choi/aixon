export type RecordMap = Record<string, unknown>;
export interface GraphData {
  raw: RecordMap; entities: Record<string, RecordMap>; types: Record<string, string>;
  claims: Record<string, RecordMap>; sources: Record<string, RecordMap>;
  fields: Record<string, RecordMap>; parents: Record<string, string[]>;
  memberships: Record<string, string[]>; claimsBySubject: Record<string, RecordMap[]>;
  claimsByObject: Record<string, RecordMap[]>; introYears: Record<string, number>;
  prerequisites: Record<string, RecordMap[]>; build: 'preview' | 'public';
}
