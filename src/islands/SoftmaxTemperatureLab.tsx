import katex from 'katex';
import { useMemo, useState } from 'react';
import { entropy, sdpaStats, softmax } from '../lib/lab/softmax';

type Item = Record<string, unknown>;
const number = (value: number) => value.toFixed(4);
const logTemperature = (value: number) => Math.log(value);
const fromLogTemperature = (value: number) => Math.exp(value);

function Quiz({ item }: { item: Item }) {
  const [answer, setAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const slug = String(item.id || '').replace(/^ai:/, '');
  const choices = Array.isArray(item.choices) ? item.choices.map(String) : [];
  const expected = Number(item.answer);
  const tolerance = Number(item.tolerance || 0);
  const correct = choices.length
    ? Number(answer) === expected
    : Math.abs(Number(answer) - expected) <= tolerance;
  return (
    <section data-testid={`quiz-${slug}`}>
      <h3>{String(item.prompt || item.question || '예측')}</h3>
      {choices.length ? (
        choices.map((choice, index) => (
          <label key={choice}>
            <input
              type="radio"
              name={slug}
              value={index}
              checked={answer === String(index)}
              onChange={(event) => setAnswer(event.target.value)}
            />
            {choice}
          </label>
        ))
      ) : (
        <input
          aria-label={`${slug} 답`}
          type="number"
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
        />
      )}
      <button data-testid={`quiz-submit-${slug}`} onClick={() => setSubmitted(true)}>
        제출
      </button>
      {submitted && (
        <p data-testid={`quiz-result-${slug}`}>
          {correct ? '정답' : '오답'} · {String(item.rationale || item.explanation || '')}
        </p>
      )}
    </section>
  );
}

export default function SoftmaxTemperatureLab({
  items = [],
  varianceClaim,
}: {
  items?: Item[];
  varianceClaim?: Item;
}) {
  const [logits, setLogits] = useState([3, 1, 0.2, -1, 2.5]);
  const [temperature, setTemperature] = useState(1);
  const [dk, setDk] = useState(64);
  const [scaled, setScaled] = useState(true);
  const [seed, setSeed] = useState(42);
  const [stats, setStats] = useState(() => sdpaStats(64, 8, 1000, true, 42));
  const probabilities = useMemo(() => softmax(logits, temperature), [logits, temperature]);
  const formula = katex.renderToString(
    `p_i = \\frac{e^{z_i/${temperature}}}{\\sum_j e^{z_j/${temperature}}}`,
    { throwOnError: false, displayMode: true },
  );
  const editLogit = (index: number, value: string) =>
    setLogits((current) =>
      current.map((logit, position) =>
        position === index ? (Number.isFinite(Number(value)) ? Number(value) : 0) : logit,
      ),
    );
  const evidence = Array.isArray(varianceClaim?.evidence)
    ? (varianceClaim.evidence[0] as Item | undefined)
    : undefined;
  return (
    <section aria-label="Softmax Temperature Lab">
      <h2>Softmax Temperature Lab</h2>
      <fieldset>
        <legend>모드 A · 온도</legend>
        {logits.map((value, index) => (
          <label key={index}>
            logit {index}
            <input
              aria-label={`logit ${index}`}
              type="number"
              value={value}
              onChange={(event) => editLogit(index, event.target.value)}
            />
          </label>
        ))}
        <label>
          T{' '}
          <input
            aria-label="temperature slider"
            type="range"
            min={logTemperature(0.05)}
            max={logTemperature(5)}
            step="0.001"
            value={logTemperature(temperature)}
            onChange={(event) => setTemperature(fromLogTemperature(Number(event.target.value)))}
          />
        </label>
        <input
          data-testid="temperature"
          aria-label="temperature"
          type="number"
          min="0.05"
          max="5"
          step="any"
          value={temperature}
          onChange={(event) => {
            const value = Number(event.target.value);
            if (Number.isFinite(value) && value >= 0.05 && value <= 5) setTemperature(value);
          }}
        />
        <div dangerouslySetInnerHTML={{ __html: formula }} />
        {probabilities.map((value, index) => (
          <div key={index}>
            p{index} <progress value={value} max="1" />{' '}
            <output data-testid={`prob-${index}`}>{number(value)}</output>
          </div>
        ))}
        <p>
          최대 확률 <output data-testid="max-prob">{number(Math.max(...probabilities))}</output> ·
          엔트로피 <output data-testid="entropy">{number(entropy(probabilities))}</output>
        </p>
      </fieldset>
      <fieldset>
        <legend>모드 B · Scaled Dot-Product</legend>
        <label>
          d_k{' '}
          <select
            data-testid="dk"
            aria-label="d_k"
            value={dk}
            onChange={(event) => setDk(Number(event.target.value))}
          >
            {[1, 4, 16, 64, 256, 512, 1024].map((value) => (
              <option key={value}>{value}</option>
            ))}
          </select>
        </label>
        <label>
          <input
            data-testid="scaling"
            aria-label="scaling"
            type="checkbox"
            checked={scaled}
            onChange={(event) => setScaled(event.target.checked)}
          />{' '}
          scaling
        </label>
        <label>
          seed{' '}
          <input
            data-testid="seed"
            aria-label="seed"
            type="number"
            value={seed}
            onChange={(event) => setSeed(Number(event.target.value) || 0)}
          />
        </label>
        <button
          data-testid="compute"
          onClick={() => setStats(sdpaStats(dk, 8, 1000, scaled, seed))}
        >
          계산
        </button>
        <p>
          Var(q·k) <output data-testid="var-qk">{number(stats.var_qk)}</output> · mean max{' '}
          <output data-testid="mean-max-weight">{number(stats.mean_max_weight)}</output> · Jacobian{' '}
          <output data-testid="jac">{number(stats.mean_jacobian_fro)}</output>
        </p>
        {varianceClaim && (
          <blockquote lang="en">
            {String(evidence?.quote || evidence?.rationale || '')}{' '}
            <a href={`/claims/${String(varianceClaim.id).replace(/^clm:/, '')}/`}>근거 보기</a>
          </blockquote>
        )}
      </fieldset>
      {items.map((item) => (
        <Quiz key={String(item.id)} item={item} />
      ))}
    </section>
  );
}
