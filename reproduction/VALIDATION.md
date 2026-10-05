# Artifact validation record

Context-length revision **0.6.0**, validated **2026-10-05** with Python **3.14.4**, uv **0.11.12**, Tectonic **0.16.9** and cffconvert **2.0.0** on macOS. Tables and Matplotlib **3.10.8** charts were regenerated from the frozen evidence and checked by the artifact verifier.

Evidence source: Cascadia commit **eb7fb6381e62c1a33ec7038422bf6e8c52c77416** on `autolab/inkling-fleet-perf`.

Completed checks:

- Reconstructed the seven context-length operating points from 19 completed requests and the synthetic cache/decode probe from eleven machines. Rebuilt the context figure and checked the rendered section, table and figure. The 1M admission result includes the probe's 3 GiB memory reserve; potential parallel-attention gains are identified as future work.

- Matched the companion architecture paper's author-block layout and line-breaking tolerance; the two papers use identical `arxiv.sty` files. Removed author email addresses from the manuscript, README and citation metadata; set Tate Berenbaum and Matias Parij's affiliation to **Not Community Labs Inc.** Added explicit PDF title/author metadata and inspected the rendered title page.
- Reconstructed all **35 finalized-survey records** from raw event traces: **1,605 requests and 204,192 token events**, including pilots. Every request's token count matches final API usage; every common-interval and whole-phase rate matches its source record.
- Reconstructed the **15-point paired concurrency curve**, phase-rate means and pooled TTFT quantiles. Verified the 88-stream means of **60.286375 decode tokens/s** and **46.874876 whole-phase tokens/s** and fifteen-stream median TTFT of **6.052471 s**.
- Verified the report's survey totals excluding pilots: **33 phases, 1,592 requests and 203,776 output tokens**.
- Independently matched all **34** survey phases with available sampled idle brackets to server token-counter deltas; the audit records the remaining phase's absent sampled bracket separately.
- Confirmed that all twelve single-stream prompt/output pairs are text-identical through their complete 128-token outputs, consistent with the retained output hashes.
- Reconstructed the full twelve-row fused-iGPU first/repeated table from paired-output records and survey request rates. Verified the largest ratio, **3.279284×** for tips, and explanation's **2.889781×** ratio and **14.698023 tokens/s** repeated rate.
- Reconstructed all six GPU phrase-transfer comparisons, including code's **2.028708×** and true/false's **2.193318×** ratios. Verified the separate three-request explanation phase's **11.268345 tokens/s median / 15.041537 fastest**.
- Reconstructed the three earlier same-binary speculation off/on observations from their gate records and configuration difference: **6.811%, 13.962% and 32.813%** decode-rate gains. Confirmed all recorded reference checks are exact and labeled their CPU-expert execution configuration.
- Reconstructed six completed structured-family examples, the final **1.804310× decode / 1.687362× whole-phase** first/repeated ratios, and the copy-task illustration (**2.800385 tokens/s** predicted from retained summary inputs versus **2.793** measured).
- Verified all **440** evidence hashes and byte sizes and recomputed all **125 historical phase rates** within storage rounding.
- Matched the historical **21,549-token** server-counter delta independently to client accounting.
- Reconstructed dense-operator, prefill and draft tables and checked physical-device/pipeline-role identity. The code map distinguishes the original survey commit from the later context-study evidence commit.
- Retained the five validated paper charts and supporting counter chart as PDF/PNG. Built the fleet architecture, custom-engine/OpenVINO boundary and new speculative-scenario diagrams from the LaTeX source.
- Checked the graph/routing, layer/row scaling, constant materialization and dense-slicing descriptions against the four frozen implementation files; attributed upstream mechanisms separately from Cascadia's custom engine.
- Resolved all **32 manuscript citations** within the **36-source literature ledger** and validated current report-document links.
- Validated strict JSON and scanned text/compressed archives for the specified private-address, home-path, MAC and credential patterns.
- Built the **19-page PDF** with resolved references and no overfull boxes; visually inspected Section 4.3's scenario diagram, latency equation, full GPU comparison table and supporting GPU results. Tectonic's `inputenc` warning reflects its UTF-8 engine.
- Validated `CITATION.cff` against schema 1.2.0 and confirmed that the GitHub repository remains private.

This revision incorporates PR #1's context-length measurements and performance summary. It rebuilds the paper from the combined source, updates evidence/version metadata, and keeps the GPU speculative-serving results and companion-paper author formatting. No fleet execution was performed.
