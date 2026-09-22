# Artifact validation record

Finalized-performance revision **0.3.0**, validated **2026-09-21** with Python **3.14.4**, uv **0.11.12**, Matplotlib **3.10.8**, Tectonic **0.16.9** and cffconvert **2.0.0** on macOS.

Evidence source: Cascadia commit **3189a189fe3428f5a6315a7eb67b13148ec314e2** on `autolab/inkling-fleet-perf`.

Completed checks:

- Reconstructed all **35 finalized-survey records** from raw event traces: **1,605 requests and 204,192 token events**, including pilots. Every request's token count matches final API usage; every common-interval and whole-phase rate matches its source record.
- Reconstructed the **15-point paired concurrency curve**, phase-rate means and pooled TTFT quantiles. Verified the 88-stream means of **60.286375 decode tokens/s** and **46.874876 whole-phase tokens/s** and fifteen-stream median TTFT of **6.052471 s**.
- Verified the report's survey totals excluding pilots: **33 phases, 1,592 requests and 203,776 output tokens**.
- Independently matched all **34** survey phases with available sampled idle brackets to server token-counter deltas; the audit records the remaining phase's absent sampled bracket separately.
- Confirmed that all twelve single-stream prompt/output pairs are text-identical through their complete 128-token outputs, consistent with the retained output hashes.
- Verified all **417** evidence hashes and byte sizes and recomputed all **125 historical phase rates** within storage rounding.
- Matched the historical **21,549-token** server-counter delta independently to client accounting.
- Reconstructed dense-operator, prefill and draft tables and checked physical-device/pipeline-role identity. Confirmed that runtime files linked in the code map are unchanged between the prior and current evidence commits.
- Generated **four paper charts** and one supporting counter chart as PDF/PNG, plus the in-document architecture diagram.
- Resolved all **29 manuscript citations** within the **33-source literature ledger** and validated current report-document links.
- Validated strict JSON and scanned text/compressed archives for the specified private-address, home-path, MAC and credential patterns.
- Built the **14-page PDF** with resolved references and no overfull boxes; visually inspected the new performance table and chart in the rendered pages. Tectonic's `inputenc` warning reflects its UTF-8 engine.
- Validated `CITATION.cff` against schema 1.2.0 and confirmed that the GitHub repository remains private.

The revision retains the paper's contribution-based organization and incorporates the finalized performance survey. Complete-phase throughput, common-interval decode throughput, operator timings and offline draft agreement have distinct definitions in the manuscript and claim map.
