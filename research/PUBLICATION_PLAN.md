# Publication preparation

## Current deliverable

A complete research manuscript with architecture, methods, measured results, failure/negative-result analysis, related work, limitations, bibliography, figures and an offline data artifact. It is suitable for author review and further research development; the current dataset is exploratory and does not establish the controlled evaluation expected of a strong systems-performance claim.

The natural positioning is a systems measurement/case-study paper about practical sparse-model serving on client hardware. Keep the contribution grounded in the observed interaction of memory, numerics and scheduling. A new scheduling-algorithm paper would require a new algorithm and controlled evaluation beyond what exists here.

## Priority measurements before a stronger submission

| Priority | Measurement | What it resolves |
|---|---|---|
| 1 | Frozen baseline/prefill/dense/head variants; same prompt set; randomized order; several independent runs per condition | Separates intervention effects from workload, warm-up, history and thermal variation. Choose repetition count from pilot variance; do not manufacture confidence from correlated tokens. |
| 1 | Per-request token IDs, first/last and every-token timestamps; synchronized server counters | Enables real simultaneous throughput, TTFT and inter-token tail distributions, and robust count semantics. |
| 1 | Original-model versus deployed-path held-out quality evaluation | Establishes the effect of INT4/INT8, FP16 fusion, scaling fixes and any canary quantization changes. |
| 2 | Frame-level tracing under output-head batching | Distinguishes convoy, delayed reply, head amortization and role idle time; directly tests the proposed explanation. |
| 2 | Per-box firmware, GPU driver, OpenVINO commit/plugin hash, memory timing, limits and model artifact hashes | Makes execution reproduction precise rather than only data reconstruction. |
| 2 | Fallback traces with allocation/residency counters | Quantifies duplicate-cache memory pressure and tests a bounded/fail-closed fallback policy. |
| 3 | Held-out fleet-trained drafting, then actual GPU cost and live serving | Replaces optimistic offline projection with measured benefit, if qualification succeeds. |
| Conditional | Wall power and matched alternative hardware/backend | Required only if adding energy, cost or cross-platform superiority claims. |

No new fleet access, experiments, purchases, deployment or public submission are implied by this list.

## Author decisions at release

- Confirm author order/contact details and add any required contribution, funding and conflict declarations. Current affiliations came from companion papers; no endorsement statement is inferred.
- Review model-output samples and source-artifact licensing before a public data release. This repository is private; public artifact availability is not promised as already achieved.
- Choose a venue and refresh related work to its submission date. Do not infer current calls, deadlines or venue suitability from this document.
- Decide whether to publish the exploratory case study first or extend it with the priority measurements. Keep the limitations in either version.
