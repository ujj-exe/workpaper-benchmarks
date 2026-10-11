# Workpaper benchmarks

Raw results behind [workpaper.co/benchmark](https://workpaper.co/benchmark).

## Sandbox Burst TTI, 11 October 2026

[ComputeSDK's Sandbox Burst TTI](https://www.computesdk.com/benchmarks/sandboxes) requests 100 sandboxes at the same instant and times each one from `create()` until its first command, `node -v`, succeeds.

| | Result |
|---|---|
| Started | **100 / 100** |
| Median | **952 ms** |
| p95 | 999 ms |
| p99 | 1,003 ms |
| Score | **90.3** |

90.3 would sit between Tenki (91.1, #13) and Beam (90.2, #14) on ComputeSDK's board of 9 October 2026.

**This is a self-run, not an official ComputeSDK listing.** It ran on a single-node test deployment, not Workpaper's production capacity.

### Files

| File | What it is |
|---|---|
| [`sandbox-burst-tti/2026-10-11/result.json`](sandbox-burst-tti/2026-10-11/result.json) | The harness's result file, unedited: all 100 per-sandbox times and the score it computed (`compositeScore: 90.29`) |
| [`sandbox-burst-tti/2026-10-11/harness-output.txt`](sandbox-burst-tti/2026-10-11/harness-output.txt) | The harness's console output for the run, with timestamps, and the runner's location |
| [`score.py`](score.py) | Recomputes the score from a result file, no dependencies |

```sh
python3 score.py sandbox-burst-tti/2026-10-11/result.json
# workpaper: 100/100 ok, median 952 ms, p95 998 ms, p99 1001 ms, score 90.29
```

(p95 and p99 differ from the harness by about 1 ms because of percentile interpolation; the score matches.)

### Method

- **Harness:** [computesdk/benchmarks](https://github.com/computesdk/benchmarks) (MIT), `benchmarks/sandbox/tti.bench.ts`, unmodified apart from a `workpaper` provider entry.
- **Command:** `--provider workpaper --iterations 100 --concurrency 100`, the same flags as ComputeSDK's daily run.
- **Runner:** GitHub Actions, San Antonio, Texas. Run on 11 October 2026 at 15:06 UTC.
- **Score:** drop the fastest and slowest 5%, then `0.6 × median + 0.25 × p95 + 0.15 × p99`, each scored as `100 × (1 − t / 10 s)`, times the share of sandboxes started.

### How the deployment was set up

- **Pre-booted pool.** Create requests claim an already-running computer close to the caller, and a replacement boots behind it. Pool computers are warmed with `true`, not with the benchmark's `node -v`.
- **Large memory pages.** Computers resume from snapshots backed by large pages, so a fresh computer's first command takes about 8 ms instead of about 300 ms.
- **Admission queue.** Bursts wait in a fair queue instead of being rejected, so all 100 start.

### Limits

- **One node.** All 100 computers ran on a single machine.
- **Distance.** The runner was in Texas and the node was in Europe, so every first command crossed the Atlantic. On the node itself, the same burst of 100 took 0.36 s median.
- **Test deployment.** Production capacity today is smaller and hosted in India.
- **Self-run.** ComputeSDK's official daily runs use their own runners, so treat the placing as an estimate.

## Try Workpaper

```sh
curl -fsSL https://workpaper.co/install | sh
```

60 free minutes, no account needed. [workpaper.co](https://workpaper.co) · [docs](https://docs.workpaper.co)
