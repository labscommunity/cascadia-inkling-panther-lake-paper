# Metric and evidence audit

The manuscript reports implemented designs and measured capabilities. This document defines the measurements connecting those claims to the preserved evidence.

## Finalized concurrency survey

The evidence snapshot pins Cascadia commit `3189a189fe3428f5a6315a7eb67b13148ec314e2`. The survey uses serving release `1790016660` and binary SHA-256 `9084392040688eaa6aa9ff6cf6d222f84e24e119e528d91920d12ddd106563c2`. The model and binary remain fixed across its phases. The [collection record](evidence/source/autolab/experiments/046_final_performance/collection-environment.json) records the eleven-device, eleven-group, 66-layer configuration.

The [35 survey records](results/survey_phases.csv) comprise thirty mixed-workload phases, three explanation-family phases and two pilots. Excluding pilots, the totals are **33 phases, 1,592 requests and 203,776 generated tokens**. The [concurrency curve](results/concurrency.csv) uses only the thirty mixed phases: two phases at each of fifteen levels from 1 to 176 streams. Explanation-family measurements cover 1, 15 and 64 streams; they are retained separately from the mixed curve.

Every measured request uses temperature zero and an output cap of 128 tokens, with 15 ms arrival spacing within each cohort. At low concurrency, whole cohorts provide at least twelve requests per mixed phase. Family proportions vary slightly with cohort rounding. The deterministic prompt templates recur across passes; finite pools also produce repeated inputs within large cohorts (79 distinct prompts among 88 requests).

Phrase learning remains active throughout. The main sweep proceeds upward and then downward, with 88 streams measured as a later refinement pair. Residual-capture writes are on for the ascending 1–15-stream phases and off thereafter. Other generation between measured phases can contribute phrase history, while phase counter checks isolate measured traffic. The two phases characterize this stateful service under the recorded order and instrumentation settings.

## Metric reconstruction and accounting

For each cohort, the common decode interval starts at its latest first-token event and ends at its earliest last-token event. Tokens are counted over the open-left, closed-right interval. **Aggregate decode throughput** divides the sum of these token counts by the sum of these interval durations across cohorts. Dividing by concurrency gives the mean contribution per stream over common intervals.

**Whole-phase throughput** divides all generated tokens by the unrounded phase duration, including admission, prefill, queueing and drain. Recorded capacity backoff remains part of request TTFT and phase time. Table/figure rates are arithmetic means of the two phase rates, while TTFT quantiles pool individual requests from both phases. Shading shows the observed phase range, rather than a confidence interval.

The client checks token-event multiplicities against final API completion-token usage. [analyze_survey.py](scripts/analyze_survey.py) independently reconstructs all 35 records from their raw event traces: **1,605 requests and 204,192 token events**, including pilots. It checks complete-cohort membership, 128-token completion for measured requests, TTFT, request decode rate and each common-interval and whole-phase rate. Two pilots use their recorded shorter output caps.

The original collector checks token and request counters around each phase. An additional reconstruction from periodically sampled API statistics finds idle brackets within ten seconds around **34 of 35** records, all with exact token-counter matches. The sampled series supplies no such bracket for `mixed_b_c128`; its request events and final usage still reconstruct exactly. [survey_audit.json](results/survey_audit.json) distinguishes an absent sampled bracket from a counter disagreement.

The highest paired mean on the measured grid is **60.286375 decode tokens/s** and **46.874876 whole-phase tokens/s**, both at 88 streams. At fifteen streams, pooled median TTFT is **6.052471 s**. TTFT counts the first emitted model-token event, including reasoning and structural tokens.

The twelve single-stream prompt/output pairs are text-identical through all 128 measured tokens. Their first/repeated phase decode rates are **5.676968/10.243011 tokens/s**. Active phrase history, pass order and differing capture state are part of those observations; the measurements do not isolate a kernel improvement or unseen-prompt performance.

## Speculative decoding scenarios and comparisons

[analyze_speculation.py](scripts/analyze_speculation.py) reconstructs Section 4.3 from existing frozen records. The main table now uses the [twelve final fused-iGPU prompt pairs](results/speculation_gpu.csv). The script also emits [six GPU phrase-transfer comparisons](results/speculation_phrase_transfer.csv), [structured-family rates](results/speculation_families.csv), [complete comparison inputs](results/speculation_audit.json) and the manuscript's generated table.

- **Final fused-iGPU per-prompt gains:** `mixed_a_c001` and `mixed_b_c001` use the same binary and model, with speculation enabled in both. The full twelve-row table reports one request per family per pass, all with identical prompts and complete 128-token outputs. Tips improves from **3.554646 to 11.656693 tokens/s (3.279284×, +227.928%)**; explanation from **5.086206 to 14.698023 (2.889781×)**; table generation from **3.760441 to 8.656464 (2.301981×)**. Each row's rates are checked against both the retained comparison and survey request metrics, whose events are independently reconstructed by `analyze_survey.py`. The first study pass already has history; subsequent phrase learning, order and differing capture writes accompany these repeated-prompt gains. They are not a speculation off/on ablation or an isolated GPU-versus-CPU comparison.
- **Final-engine phase-level ratios:** rates over the twelve serial requests give **1.804310× decode** and **1.687362× whole-phase**. These duration-weighted phase observations differ from an arithmetic mean of the individual speedups.
- **GPU phrase-history transfer:** `038_phrase_transfer/phases-baseline.json` and `phases.json` record the same six previously seen 128-token prompts around the verified merge. The [summary](evidence/source/autolab/experiments/038_phrase_transfer/verdict.md) records **24,453→194,299 contexts** and no binary change. Code rises from **5.225 to 10.600 tokens/s (2.028708×)**; true/false from **4.909 to 10.767 (2.193318×)**. Repeated requests also train the table, and capture was disabled with transfer. The before/after rates therefore include those influences; they are not an isolated transfer effect. Full output equality is established for the finalized twelve pairs above, not inferred for these six pairs from their abbreviated previews.
- **GPU explanation-family rates:** `family_00_a_c001` contains three 128-token requests, with median **11.268345 tokens/s** and fastest **15.041537 tokens/s**. These are absolute request rates in an additional phase, with no disabled-speculation counterpart.
- **Structured GPU continuations:** `015c_ensemble` records six completed 128-token single-request examples using the hybrid table/model proposer with related-family history. Translation, arithmetic and true/false decode rates are **6.597, 8.194 and 10.951 tokens/s**. These are absolute rates on distinct prompts.

The frozen artifact also retains earlier CPU-expert observations as supporting protocol evidence:

- **Speculation off/on:** `002a_return_link` and `002b_speculation` use binary `6bad6fd8` and identical non-comment override lines except the appended `CASCADIA_STREAMS_SPEC=1`. This earlier configuration uses **CPU experts**, with iGPU attention projections and output head. The retained gates cover the same sky, capital and arithmetic prompts with a 32-token cap and one request per prompt per condition. Their rates are 1.659→1.772, 1.676→1.910 and 1.600→2.125 tokens/s: **6.811%, 13.962% and 32.813%** observed gains. Each gate records `exact=true` and complete character agreement with its reference; the saved text field itself is a truncated preview. Rates use `(tokens−1)/(last_event−first_event)`. These sequential observations are neither randomized repetitions nor an on/off comparison of the finalized fused engine.

The latency equation is an illustrative model, not another timing measurement. An earlier CPU-expert numerical check remains in the artifact: the `002b_speculation` summary reports **47 of 96** copying-task output positions benefiting from correct inputs already in flight, an interval **T=58.5 ms** and **11 stages**. Substituting `a=47/96` and `L=11T` into `1/(aT+(1−a)L)` predicts **2.800385 tokens/s**, compared with the structured phase's measured **2.793 tokens/s**. The fraction is useful in-flight positions per generated token, not accepted proposals per attempt. The model excludes extra drafting, queueing and rewind costs. There is no paired disabled copy timing from which to claim an empirical copy speedup.

The [runtime anchors](CODE_MAP.md) establish asynchronous verification of successive frames, preference for confident history matches, draft-text retokenization, and restoration of KV plus convolution state. This path applies to a lone stream; the high-concurrency throughput curve and offline MTP agreement remain separate findings.

## Supporting configuration and operator measurements

For all 125 historical phase records, recomputing `aggregate_tok_s` from token counts and unrounded timestamps matches storage rounding. Historical `sum_stream_tok_s` sums per-request rates over differing intervals; it is distinct from the finalized common-interval decode metric. The historical 176-request workload records 57.948 whole-phase tokens/s and 70.235 summed request rates. Its server counter independently matches all 21,549 tokens. These records remain available as supporting evidence.

The reference and windowed fifteen-request configurations use the same 128-token cap but distinct prompt tags. Their comparison is observational: median TTFT changes from 31.23–31.52 s to 6.91 s. The staggered fifteen-request workload uses approximately one-second arrivals and a 96-token cap, yielding 2.48 s median TTFT.

Dense-layer times come from retained one-/two-row load checks. `dense.csv` computes reductions of 44.7%/45.1% for one row, with FP16 path differences of 5.7e-4/5.9e-4. The role 0 profile comparison is a separate stage measurement; operator savings are not an isolated fleet-throughput multiplier.

## Custom engine attribution and numerical identities

Four implementation files are frozen at the same Cascadia evidence commit: the exporter, Rust gate, fused layer runtime and C++ bridge. [CODE_MAP.md](CODE_MAP.md) and [CLAIMS.md](CLAIMS.md) identify the functions supporting the expanded engine description. OpenVINO's primitive and graph-lowering references are pinned to release 2026.3.1.

The layer/row scaling equation describes a real-arithmetic identity. The absolute routing-weight sum is bounded by one after row normalization; multiplying the GPU output by the layer and row factors restores magnitude in FP32. FP16 conversion, subnormal scales and reduction rounding remain distinct numerical effects. The paper presents these mechanisms as implemented range management, with equivalent-rescaling prior art attributed; it does not infer a new fleet-throughput multiplier from the identity.

## Profiles and numerical labels

Profile windows are deduplicated and aligned using receipt age on the operator clock. Physical device identity and pipeline role are separate. Stage times are frame-weighted software-profile averages; GPU timings retain associated fallback counters.

Draft evaluation uses actual emitted fleet IDs as labels. Vocabulary and weight-format comparisons use the same 36 captured sequences and 5,724 prediction targets. The **2.271139** and **0.174703 percentage-point** differences reconstruct from raw agreement values. The quantized calculation uses FP32 arithmetic offline, so draft agreement remains distinct from live throughput.

Short serial/concurrent prefixes and twelve known-answer questions support functional validation. They are not a general model-quality benchmark.

## Evidence integrity

The snapshot contains **421 hashed evidence files**, **160 phase records** across **50 source directories**, **35 fleet telemetry archives** and **36 request/stat archives**. The [claim map](CLAIMS.md) selects the measurements supporting each contribution.

Import scrubs device/network identities and home paths, normalizes nonfinite JSON numbers to `null`, and retains original/stored hashes. `null` is distinct from measured zero. `make data` reconstructs the tables; `make verify` checks the frozen artifact and derived results.
