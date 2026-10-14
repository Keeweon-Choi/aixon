/** Reference numbers of the Lab, read from the committed numpy fixture (never from application code). */
import fs from 'node:fs';

interface SoftmaxCase {
  z: number[];
  T: number;
  p: number[];
}

interface SdpaCase {
  d_k: number;
  n_keys: number;
  samples: number;
  scaled: boolean;
  seed: number;
  var_qk: number;
  mean_max_weight: number;
  mean_jacobian_fro: number;
}

const FIXTURE_FILE = 'data/seed/lab_fixtures/softmax_temperature.json';

function load(): { softmax: SoftmaxCase[]; sdpa: SdpaCase[] } {
  return JSON.parse(fs.readFileSync(FIXTURE_FILE, 'utf8'));
}

export function softmaxCase(z: number[], T: number): SoftmaxCase {
  const found = load().softmax.find(
    (entry) => entry.T === T && entry.z.length === z.length && entry.z.every((v, i) => v === z[i]),
  );
  if (!found) throw new Error(`no softmax fixture entry for z=${z} T=${T}`);
  return found;
}

export function sdpaCase(dK: number, scaled: boolean): SdpaCase {
  const found = load().sdpa.find(
    (entry) =>
      entry.d_k === dK && entry.scaled === scaled && entry.seed === 42 && entry.n_keys === 8,
  );
  if (!found) throw new Error(`no sdpa fixture entry for d_k=${dK} scaled=${scaled}`);
  return found;
}

/** The Lab renders every number with four decimals. */
export function fmt4(value: number): string {
  return value.toFixed(4);
}

/** Entropy in nats of a probability vector (computed here, independently of the application). */
export function entropy(p: number[]): number {
  return -p.reduce((sum, x) => sum + (x > 0 ? x * Math.log(x) : 0), 0);
}
