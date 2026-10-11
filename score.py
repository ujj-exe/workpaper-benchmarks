"""Recompute the Sandbox Burst TTI score from a harness result file.

usage: python3 score.py sandbox-burst-tti/2026-10-11/result.json

Formula (ComputeSDK): drop the slowest and fastest 5%, take median, p95, p99,
score each as 100 * (1 - t / 10 s), weight 0.6 / 0.25 / 0.15, multiply by success rate.
"""
import json, sys

def pct(xs, p):  # linear interpolation between closest ranks
    k = (len(xs) - 1) * p / 100
    lo = int(k); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)

def score(times_ms, ok, total):
    t = sorted(times_ms)
    cut = int(len(t) * 0.05)
    t = t[cut:len(t) - cut] if cut else t
    m, p95, p99 = pct(t, 50), pct(t, 95), pct(t, 99)
    s = lambda ms: max(0.0, 100 * (1 - ms / 10_000))
    return m, p95, p99, (0.6 * s(m) + 0.25 * s(p95) + 0.15 * s(p99)) * ok / total

if __name__ == "__main__":
    r = json.load(open(sys.argv[1]))["results"][0]
    its = r["iterations"]
    times = [i["ttiMs"] for i in its if "ttiMs" in i]
    m, p95, p99, sc = score(times, len(times), len(its))
    print(f"{r['provider']}: {len(times)}/{len(its)} ok, median {m:.0f} ms, p95 {p95:.0f} ms, p99 {p99:.0f} ms, score {sc:.2f}")
    print(f"harness reported: score {r['compositeScore']}, median {r['summary']['ttiMs']['median']} ms")
