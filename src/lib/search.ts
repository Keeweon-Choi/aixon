export interface SearchNode {
  id: string;
  name: string;
  aliases: string[];
  type: string;
  url: string;
  hasWiki?: boolean;
}

function words(value: string): string[] {
  return value
    .toLocaleLowerCase()
    .split(/[\s\-_/.:]+/)
    .filter(Boolean);
}

function score(node: SearchNode, query: string[]): number | undefined {
  const name = node.name.toLocaleLowerCase();
  const aliases = node.aliases.map((alias) => alias.toLocaleLowerCase());
  const id = node.id.toLocaleLowerCase();
  const corpus = [name, ...aliases];
  let best = 0;
  for (const term of query) {
    const exact = corpus.some((value) => value === term);
    const prefix = corpus.some((value) => words(value).some((word) => word.startsWith(term)));
    const substring = name.includes(term);
    const idMatch = id.includes(term);
    if (!exact && !prefix && !substring && !idMatch) return undefined;
    best += exact ? 400 : prefix ? 300 : substring ? 200 : 100;
  }
  return best;
}

export function searchNodes(nodes: SearchNode[], rawQuery: string): SearchNode[] {
  const query = rawQuery.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  if (!query.length) return [];
  return nodes
    .map((node) => ({ node, score: score(node, query) }))
    .filter((match): match is { node: SearchNode; score: number } => match.score !== undefined)
    .sort(
      (a, b) =>
        b.score - a.score ||
        Number(Boolean(b.node.hasWiki)) - Number(Boolean(a.node.hasWiki)) ||
        a.node.name.length - b.node.name.length ||
        a.node.name.localeCompare(b.node.name, 'ko'),
    )
    .slice(0, 8)
    .map((match) => match.node);
}
