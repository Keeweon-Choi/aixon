/** Build an internal URL while preserving Astro's deployment base. */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL || '/';
  const clean = String(path).replace(/^\/+/, '');
  return clean ? `${base.replace(/\/$/, '/')}${clean}` : base;
}

export function nodeAnchor(id: string): string {
  return `node-${id.replace(/:/g, '~')}`;
}
