import fixture from '../../data/seed/lab_fixtures/softmax_temperature.json';
import { describe, expect, it } from 'vitest';
import { mulberry32, sdpaStats, softmax } from '../../src/lib/lab/softmax';

describe('softmax lab primitives', () => {
  it('matches softmax fixtures and remains stable', () => {
    for (const item of fixture.softmax) {
      const actual = softmax(item.z, item.T);
      expect(actual.reduce((sum, value) => sum + value, 0)).toBeCloseTo(1, 12);
      actual.forEach((value, index) => expect(value).toBeCloseTo(item.p[index], 12));
    }
    expect(softmax([2, 1, 0], 1)).toEqual(softmax([1002, 1001, 1000], 1));
    expect(softmax([1000, 0], 0.05).every(Number.isFinite)).toBe(true);
    expect(softmax([-1000, 0], 0.05).every(Number.isFinite)).toBe(true);
  });
  it('has deterministic random and SDPA statistics', () => {
    const random = mulberry32(42);
    expect([random(), random(), random(), random(), random()]).toEqual(
      fixture.mulberry32_seed42_first5,
    );
    const variance = sdpaStats(64, 1, 10000, false, 42);
    expect(Math.abs(variance.var_qk - 64) / 64).toBeLessThan(0.05);
    expect(variance.var_qk).toBeCloseTo(fixture.variance_check.var_qk, 9);
    for (const item of fixture.sdpa) {
      const actual = sdpaStats(item.d_k, item.n_keys, item.samples, item.scaled, item.seed);
      expect(actual.var_qk).toBeCloseTo(item.var_qk, 9);
      expect(actual.mean_max_weight).toBeCloseTo(item.mean_max_weight, 9);
      expect(actual.mean_jacobian_fro).toBeCloseTo(item.mean_jacobian_fro, 9);
    }
  });
});
