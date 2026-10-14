"""Golden fixtures for the Softmax Temperature / Scaled Dot-Product Lab (docs/05 §5.4).

numpy float64 is the reference; the browser (TS) implementation must reproduce these values.
PRNG = mulberry32 (bit-exact port of the common JS one-liner), normals = Box-Muller (cos branch only).
Run:  python3 tools/gen_lab_fixtures.py > data/seed/lab_fixtures/softmax_temperature.json
"""
import json
import math
import sys

import numpy as np

M32 = 0xFFFFFFFF


def imul(a, b):
    return ((a & M32) * (b & M32)) & M32


def mulberry32(seed):
    a = seed & M32

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & M32
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & M32) ^ t
        return ((t ^ (t >> 14)) & M32) / 4294967296

    return nxt


def gaussian(rand):
    u1 = 1.0 - rand()  # (0, 1], avoids log(0)
    u2 = rand()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def softmax(z, T=1.0):
    z = np.asarray(z, dtype=np.float64) / T
    e = np.exp(z - z.max())  # max-subtraction for stability (L3)
    return e / e.sum()


def sdpa_stats(d_k, n_keys, samples, scaled, seed):
    rand = mulberry32(seed)
    var_acc, maxw, jac = [], [], []
    for _ in range(samples):
        q = np.array([gaussian(rand) for _ in range(d_k)])
        K = np.array([[gaussian(rand) for _ in range(d_k)] for _ in range(n_keys)])
        logits = K @ q
        var_acc.append(logits[0])
        if scaled:
            logits = logits / math.sqrt(d_k)
        p = softmax(logits)
        maxw.append(p.max())
        jac.append(np.linalg.norm(np.diag(p) - np.outer(p, p)))  # Frobenius norm of softmax Jacobian
    return {
        "d_k": d_k, "n_keys": n_keys, "samples": samples, "scaled": scaled, "seed": seed,
        "var_qk": float(np.var(var_acc)),            # population variance of q·k_0 (unscaled)
        "mean_max_weight": float(np.mean(maxw)),
        "mean_jacobian_fro": float(np.mean(jac)),
    }


def main():
    rand = mulberry32(42)
    prng = [rand() for _ in range(5)]
    rand = mulberry32(42)
    normals = [gaussian(rand) for _ in range(5)]
    cases = [([2, 1, 0], 1.0), ([2, 1, 0], 0.1), ([2, 1, 0], 5.0), ([2, 0], 2.0), ([2, 0], 0.5),
             ([1000, 0], 1.0), ([-1000, 0], 1.0), ([3, 1, 0.2, -1, 2.5], 0.05), ([0, 0, 0, 0], 1.0)]
    out = {
        "generator": "tools/gen_lab_fixtures.py", "numpy": np.__version__,
        "mulberry32_seed42_first5": prng,
        "gaussian_seed42_first5": normals,
        "softmax": [{"z": z, "T": T, "p": softmax(z, T).tolist()} for z, T in cases],
        "sdpa": [sdpa_stats(d, 8, 1000, s, 42) for d in (4, 64, 512) for s in (False, True)],
        "variance_check": sdpa_stats(64, 1, 10000, False, 42),  # L6: Var(q·k) ≈ d_k
    }
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
