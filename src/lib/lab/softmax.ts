export function mulberry32(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = ((t + Math.imul(t ^ (t >>> 7), 61 | t)) >>> 0) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export function gaussian(r: () => number) {
  const u1 = 1 - r(),
    u2 = r();
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}
export function softmax(z: number[], T = 1) {
  const scaled = z.map((x) => x / T),
    max = Math.max(...scaled),
    e = scaled.map((x) => Math.exp(x - max)),
    sum = e.reduce((a, b) => a + b, 0);
  return e.map((x) => x / sum);
}
export function entropy(p: number[]) {
  return -p.reduce((s, x) => s + (x ? x * Math.log(x) : 0), 0);
}
export function jacobianFro(p: number[]) {
  return Math.sqrt(
    p.reduce(
      (s, x, i) => s + p.reduce((t, y, j) => t + (x * (i === j ? 1 : 0) - x * y) ** 2, 0),
      0,
    ),
  );
}
export function sdpaStats(
  dk: number,
  nKeys: number,
  samples: number,
  scaled: boolean,
  seed: number,
) {
  const r = mulberry32(seed),
    values: number[] = [],
    maxes: number[] = [],
    jacs: number[] = [];
  for (let i = 0; i < samples; i++) {
    const q = Array.from({ length: dk }, () => gaussian(r));
    const logits = Array.from({ length: nKeys }, () =>
      Array.from({ length: dk }, () => gaussian(r)).reduce((s, k, j) => s + k * q[j], 0),
    );
    values.push(logits[0]);
    const p = softmax(scaled ? logits.map((x) => x / Math.sqrt(dk)) : logits);
    maxes.push(Math.max(...p));
    jacs.push(jacobianFro(p));
  }
  const mean = (a: number[]) => a.reduce((s, x) => s + x, 0) / a.length,
    m = mean(values);
  return {
    d_k: dk,
    n_keys: nKeys,
    samples,
    scaled,
    seed,
    var_qk: mean(values.map((x) => (x - m) ** 2)),
    mean_max_weight: mean(maxes),
    mean_jacobian_fro: mean(jacs),
  };
}
