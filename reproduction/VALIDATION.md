# Artifact validation record

GPU speculative-decoding revision **0.5.1**, validated **2026-09-25** with Python **3.14.4**, uv **0.11.12**, Tectonic **0.16.9** and cffconvert **2.0.0** on macOS. Existing charts retain their validated Matplotlib **3.10.8** renderings.

Evidence source: Cascadia commit **3189a189fe3428f5a6315a7eb67b13148ec314e2** on `autolab/inkling-fleet-perf`.

Completed checks:

- Reconstructed all **35 finalized-survey records** from raw event traces: **1,605 requests and 204,192 token events**, including pilots. Every request's token count matches final API usage; every common-interval and whole-phase rate matches its source record.
- Reconstructed the **15-point paired concurrency curve**, phase-rate means and pooled TTFT quantiles. Verified the 88-stream means of **60.286375 decode tokens/s** and **46.874876 whole-phase tokens/s** and fifteen-stream median TTFT of **6.052471 s**.
- Verified the report's survey totals excluding pilots: **33 phases, 1,592 requests and 203,776 output tokens**.
- Independently matched all **34** survey phases with available sampled idle brackets to server token-counter deltas; the audit records the remaining phase's absent sampled bracket separately.
- Confirmed that all twelve single-stream prompt/output pairs are text-identical through their complete 128-token outputs, consistent with the retained output hashes.
- Reconstructed the full twelve-row fused-iGPU first/repeated table from paired-output records and survey request rates. Verified the largest ratio, **3.279284×** for tips, and explanation's **2.889781×** ratio and **14.698023 tokens/s** repeated rate.
- Reconstructed all six GPU phrase-transfer comparisons, including code's **2.028708×** and true/false's **2.193318×** ratios. Verified the separate three-request explanation phase's **11.268345 tokens/s median / 15.041537 fastest**.
- Reconstructed the three earlier same-binary speculation off/on observations from their gate records and configuration difference: **6.811%, 13.962% and 32.813%** decode-rate gains. Confirmed all recorded reference checks are exact and labeled their CPU-expert execution configuration.
- Reconstructed six completed structured-family examples, the final **1.804310× decode / 1.687362× whole-phase** first/repeated ratios, and the copy-task illustration (**2.800385 tokens/s** predicted from retained summary inputs versus **2.793** measured).
- Verified all **421** evidence hashes and byte sizes and recomputed all **125 historical phase rates** within storage rounding.
- Matched the historical **21,549-token** server-counter delta independently to client accounting.
- Reconstructed dense-operator, prefill and draft tables and checked physical-device/pipeline-role identity. Confirmed that runtime files linked in the code map are unchanged between the prior and current evidence commits.
- Retained the four validated paper charts and supporting counter chart as PDF/PNG. Built the fleet architecture, custom-engine/OpenVINO boundary and new speculative-scenario diagrams from the LaTeX source.
- Checked the graph/routing, layer/row scaling, constant materialization and dense-slicing descriptions against the four frozen implementation files; attributed upstream mechanisms separately from Cascadia's custom engine.
- Resolved all **32 manuscript citations** within the **36-source literature ledger** and validated current report-document links.
- Validated strict JSON and scanned text/compressed archives for the specified private-address, home-path, MAC and credential patterns.
- Built the **17-page PDF** with resolved references and no overfull boxes; visually inspected Section 4.3's scenario diagram, latency equation, full GPU comparison table and supporting GPU results. Tectonic's `inputenc` warning reflects its UTF-8 engine.
- Validated `CITATION.cff` against schema 1.2.0 and confirmed that the GitHub repository remains private.

This revision makes the fused-iGPU deployment the central performance evidence in Section 4.3. The table includes all twelve final GPU prompt pairs; the text adds GPU phrase-transfer comparisons, structured requests and explanation-family rates. Earlier CPU-expert on/off observations and the historical copy-model check remain in the supporting artifact. All new calculations use the existing 421-file frozen evidence snapshot; no fleet execution or new inference measurements were performed. Repeated-prompt behavior, concurrent throughput and offline draft agreement retain their distinct scopes. The supporting code map links the proposer, target-token encoding, asynchronous verification and state rewind at the pinned commit.
