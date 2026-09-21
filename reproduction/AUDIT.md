# Evidence audit and corrections

The current manuscript, generated tables and [claim map](CLAIMS.md) govern report wording. Frozen autolab notes preserve what was believed at the time, including superseded conclusions. They are not silently rewritten to match the paper.

| Issue in the historical narrative | Evidence check and report treatment |
|---|---|
| “70 tokens/s throughput” without a metric | 011b has **57.948 whole-phase tokens/s** and **70.235 sum of request decode rates**. The latter is not simultaneous aggregate throughput. The raw server counter independently matches all **21,549** tokens. |
| Server-counter median presented as stable rate | A specified disjoint five-poll selection yields median **70.6665**, mean **45.8637**, n=14 at ≥170 requests in flight. Prefill is still present. The old ~70.5 median used different binning; neither is a repeated controlled estimate. |
| Historical SSE counting assumed universal | The inspected sparse-MoE backend emits one chunk per token, including speculative output, with explicit token count 1. Structural tokens can have no visible text. Other backends may combine tokens; future harnesses should use explicit counts. |
| “Exact” from output gates | The serial check is a short prefix/validity gate, not full-output equality. Concurrent checks are also limited; twelve known-answer prompts are smoke tests. Quantization and FP16 rounding can alter outputs. |
| Dense-as-MoE described as exact/new | Identity holds in real arithmetic and has close prior art (especially MLPMoE). Two FP16 implementations differ by **5.7e-4/5.9e-4**. Report measured backend mapping, not mathematical novelty or bitwise identity. |
| Dense fleet gain ~0.5% | Raw 026 rates **24.578/24.693** average **24.6355**; 027 rates **24.886/24.694** average **24.790**: **0.6271%** descriptive gain. It is not a significance estimate. |
| Head batching regression ~2.5% | The same 027 mean versus 028 **24.076/24.161** mean **24.1185** gives **−2.70875%**. Paper rounds to **2.71%**. |
| Local head savings imply fleet improvement | Corrected 027/028 role-10 phase-A profiles show head **11.6202 → 7.3154 ms/frame**, alongside worse summed decode. Delayed replies/convoys are plausible, not uniquely identified; prompt tags and group-64 canary removal also differ. |
| Rank-10 timing based on its wall clock | A clock jump causes stale/empty slices. Deduplicate profile windows and place them on the operator clock using receipt age. Recomputed role profiles are in `results/profiles.csv`. |
| Installed rank treated as role after relocation | From 032, installed box 8 runs role 0 and box 0 runs role 8. Physical identity, role and ingress responsibility are separate. |
| Eleven identical USB/power configurations | Static telemetry reports USB NCM on boxes 0–7, PCIe-style names on 8–10, and different platform power-limit fields. Same SKU does not mean identical installation or performance. |
| 8533 MT/s and 136.5 GB/s treated as fleet measurements | 8533 comes from a separate reference host; fleet timing not captured. 136.5 is a nominal 128-bit arithmetic assumption, not measured sustained bandwidth. |
| 60–65 GB/s described as the bus limit | This is a particular CPU kernel's logical byte/time rate. The head reaches ~108 GB/s by similar accounting. Neither number is a hardware bandwidth-counter measurement. |
| Fifteen-stream physical impossibility / exact ceiling | Logical byte counts depend on reuse and frame grouping. Include the final head: ~**45.7 GB/cycle**, versus ~32.1 for a middle stage. At assumed 136.5 GB/s and no inter-frame reuse, byte-only final-stage ceiling is ~45 tokens/s. It is conditional, not universal. |
| Reducing circulating frames predicted to help | 034 directly contradicts the prediction: 176-stream summed decode **67.974 → 64.846**, **−4.60176%**; fifteen-stream results effectively flat. The manuscript preserves the failed hypothesis. |
| All-iGPU execution asserted without exception | Corrected telemetry includes nonfinite fallback calls, including the final role in 026–028. Use “iGPU-backed”/intended placement and discuss fallbacks. |
| 021/022 called GPU crashes | 025 revises the explanation to failed inference → CPU expert fallback while GPU allocations remain → memory/swap exhaustion → OOM kill. This is a version-specific diagnosis, not proof of a present upstream bug. |
| Group-64 canary conflated with unchanged group-32 weights | 026/027 include a group-64 canary. Head batching removes it; these comparisons are not pure single-variable ablations. |
| Small power readings treated as whole-machine energy | Package/platform telemetry and configured PL fields are distinct from measured wall energy. No joules/token or fleet energy-efficiency claim is made. |
| High single-stream numbers treated as general prose speed | 015c ranges by family, from ~3.1–3.4 prose to 10.95 true/false. Phrase history has observed related families. Repeated prompts in 038 are explicitly excluded from unseen-prompt claims. |
| CPU MTP agreement ~0.73 establishes deployment readiness | Later 039 fleet-state first-draft agreement **0.668064**, deployment-grid **0.643606**, both below the **0.70** bar. CPU versus fleet changes both trajectory and numerical path. |
| Most deployment loss attributed to weight quantization | Same-state original 65k head **0.645353** vs quantized **0.643606**: incremental **0.174703 percentage points**; vocabulary restriction explains most of that step's loss. |
| “Code and arithmetic ≥0.75” in 039 verdict | Raw deployment-grid family values are **0.746331** and **0.748428**, slightly below 0.75. Paper uses actual descriptive values. |
| Original-head argmax agreement is a quality score | **0.921181** agreement with emitted fleet token IDs checks numerical-path differences; it does not measure general model quality. |
| Initial FP16 captured states can support rescoring | They overflow. Corrected FP32 captures pass finite and response-text checks for 36 responses; the first failed capture phases remain in the dataset. |
| MTP projection or exported head means live speed | Eight-module offline expected accepted drafts and byte-cost estimates are not live serving rates. Multi-stream MTP was not deployed. |
| Network probe proves full expert parallelism | 018 is a model-idle 100 kB request/reply probe. Only the 30 and 50 MB/s steps include all eleven boxes; full-model expert-parallel serving remains unmeasured here. |
| Readiness/role swap establishes fleet reliability | Short load tests and one retained integration-test account do not establish a repaired entry box, hardware failure cause or long-run availability. |
| 040 expert counts are complete | Interruption record: **41 partial layers, zero completed timed phases**, collection/training incomplete. No distribution or sparsity claim. |
| 041 microbenchmark gain predicts a serving gain | INT4 projection calls improve **39.0–43.2%** on two layers at one/two rows; random-input relative RMS difference **9.6–9.7%**. No end-to-end gain or quality score. |
| Queue/proposal implies accomplished capability | 042–045 are unfinished/proposed. No fleet-trained drafter, INT4 serving canary, CPU-overlap serving or full EP result is claimed. |

## Counts and failures

`make data` verifies 357 source hashes and enumerates 125 phase records in 49 directories, including 34 telemetry archives. All 125 whole-phase rate recomputations match stored rounding. The five records excluded from headline completion claims are:

| Experiment | Phase | Completed / requested |
|---|---|---:|
| 006 | s264 | 251 / 264 |
| 007 | s264 | 251 / 264 |
| 008b | s352 | 251 / 352 |
| 021 | mix11a | 0 / 11 |
| 021 | mix15a | 0 / 15 |

Other experiments can be unsuccessful without a failed phase row: 022 fails before a timed phase, 040 interrupts before one, and a gate may be weak even when a phase completes. “120 complete phase records” must not become “120 scientifically validated successful experiments.”

No raw observations were dropped to improve reported results. Sanitization changes identity fields and nonfinite JSON representation, not finite scientific values. The manifest records transformations and original hashes.
