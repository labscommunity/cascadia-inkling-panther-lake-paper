# Cascadia: Performance Summary
### 975B MoE (Inkling) resident inference across 11 Intel Panther Lake AI PCs (64GB each)

---

## Batch Size (Concurrent Streams) → Throughput
| Streams | Aggregate tok/s | Per-stream tok/s |
|---:|---:|---:|
| 1   | 7.96  | 7.96 |
| 15  | 24.60 | 1.64 |
| 32  | 38.31 | 1.20 |
| 64  | 53.60 | 0.84 |
| **88** | **60.29** | 0.69 |
| 128 | 50.10 | 0.39 |
| 176 | 57.72 | 0.33 |

**Peak aggregate throughput at 88 concurrent streams**; per-stream efficiency drops monotonically with batch size.

---

## TTFT (Time-to-First-Token)
- 1 stream: **2.18s** median → 176 streams: **76.8s** median (p95: 165s)
- Windowed admission (8-row prefill) vs. reference: **6.91s vs 31.5s** median TTFT @ 15-request burst

---

## TPOT / Decode Rate vs. Context Length
| Context (tokens) | First-token | Decode tok/s |
|---:|---:|---:|
| 1k  | 22s | 4.73 |
| 16k | 7.8min | 2.71 |
| 32k | 27.2min | 1.51 |
| 64k | 109.7min | 0.82 |

- Speculative decoding (phrase/model hybrid proposer) boosts single-stream decode **up to 3.28×** 

---

## Context Window Scaling
- Supports up to 64k tokens
- Practical interactive limit: **~4k tokens** (22–76s TTFT); 8–16k usable with 3–8 min wait

---

## Scaling Takeaway
Cascadia achieves **resident, shared-memory serving of a ~975B-parameter MoE model on consumer-grade AI PCs** — trading per-request latency for fleet-wide throughput
