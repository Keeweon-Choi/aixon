import { useMemo, useState } from 'react';
import { entropy, sdpaStats, softmax } from '../lib/lab/softmax';

const number = (n: number) => n.toFixed(4);
// `items`: lab_prediction assessment items from the graph (quiz UI: task B).
export default function SoftmaxTemperatureLab(_props: { items?: Record<string, unknown>[] }) {
  const [logits, setLogits] = useState([3, 1, 0.2, -1, 2.5]),
    [T, setT] = useState(1),
    [dk, setDk] = useState(64),
    [scaled, setScaled] = useState(true),
    [seed, setSeed] = useState(42),
    [stats, setStats] = useState(() => sdpaStats(64, 8, 1000, true, 42));
  const p = useMemo(() => softmax(logits, T), [logits, T]);
  const edit = (i: number, v: string) =>
    setLogits((x) => x.map((n, j) => (j === i ? Number(v) || 0 : n)));
  return (
    <section aria-label="Softmax Temperature Lab">
      <h2>Softmax Temperature Lab</h2>
      <fieldset>
        <legend>모드 A · 온도</legend>
        {logits.map((v, i) => (
          <label key={i}>
            logit {i}
            <input
              aria-label={`logit ${i}`}
              type="number"
              value={v}
              onChange={(e) => edit(i, e.target.value)}
            />
          </label>
        ))}
        <label>
          T{' '}
          <input
            aria-label="temperature"
            type="range"
            min="0.05"
            max="5"
            step="0.05"
            value={T}
            onChange={(e) => setT(Number(e.target.value))}
          />
          {T.toFixed(2)}
        </label>
        <p className="katex">pᵢ = exp(zᵢ/T) / Σⱼ exp(zⱼ/T)</p>
        {p.map((v, i) => (
          <div key={i}>
            p{i} <progress value={v} max="1" />{' '}
            <output data-testid={`prob-${i}`}>{number(v)}</output>
          </div>
        ))}
        <p>
          최대 확률 <output data-testid="max-prob">{number(Math.max(...p))}</output> · 엔트로피{' '}
          <output data-testid="entropy">{number(entropy(p))}</output>
        </p>
      </fieldset>
      <fieldset>
        <legend>모드 B · Scaled Dot-Product</legend>
        <label>
          d_k{' '}
          <select aria-label="d_k" value={dk} onChange={(e) => setDk(Number(e.target.value))}>
            {[1, 4, 16, 64, 256, 512, 1024].map((x) => (
              <option key={x}>{x}</option>
            ))}
          </select>
        </label>
        <label>
          <input
            aria-label="scaling"
            type="checkbox"
            checked={scaled}
            onChange={(e) => setScaled(e.target.checked)}
          />{' '}
          scaling
        </label>
        <label>
          seed{' '}
          <input
            aria-label="seed"
            type="number"
            value={seed}
            onChange={(e) => setSeed(Number(e.target.value) || 0)}
          />
        </label>
        <button onClick={() => setStats(sdpaStats(dk, 8, 1000, scaled, seed))}>계산</button>
        <p>
          Var(q·k) <output data-testid="var-qk">{number(stats.var_qk)}</output> · mean max{' '}
          <output data-testid="mean-max-weight">{number(stats.mean_max_weight)}</output> · Jacobian{' '}
          <output data-testid="jac">{number(stats.mean_jacobian_fro)}</output>
        </p>
      </fieldset>
    </section>
  );
}
