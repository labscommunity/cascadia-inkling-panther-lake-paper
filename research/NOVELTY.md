# Novelty assessment

Assessment cutoff: **2026-09-21**. This is a bounded prior-art review, not proof of absolute priority. Source keys refer to [sources.json](sources.json), [annotated related work](RELATED_WORK.md) and the paper bibliography. Technical judgments use primary papers, author reports, official documentation and the local frozen evidence.

## Recommended research claim

**An audited case study of a nearly trillion-parameter sparse model on eleven modest-memory integrated-GPU machines, showing how shared-memory residency, finite-precision execution, closed-loop scheduling and deployed-path draft qualification constrain useful service.**

The work is best framed as a systems measurement and implementation paper. It does not currently establish a new inference algorithm, a new queueing law, general model-quality preservation, a cross-platform performance record, or the first client cluster to serve Inkling.

## Claim-by-claim judgment

| Candidate | Closest prior art / existing lineage | What is actually distinctive here | Judgment |
|---|---|---|---|
| 975B Inkling on eleven 64 GB Intel iGPUs | Petals, TPI-LLM, prima.cpp, exo; Cascadia pipeline shards; earlier Inkling on eight DGX Sparks | This resident MoE model, Xe3/client-memory configuration, gigabit chain and measured operating envelope | **Strongest empirical contribution**, with no absolute first claim. Architecture lineage must be explicit. |
| All model shards remain resident in CPU/iGPU shared memory | EdgeMoE, PowerInfer, CPU/GPU hybrid serving | Failure chain where a GPU error invokes CPU expert loading alongside live GPU allocations and exhausts memory | **Useful implementation case and design lesson**; fallback/residency is not an invented general principle. More event-level traces would strengthen it. |
| FP16 fused-path range management and FP32 residual capture | Established finite-range arithmetic; existing quantized inference | Specific overflowing Inkling layers and residual capture failure, corrected on the fleet path | **Reproducible numerical case study**, not a new floating-point technique; gates are insufficient for broad quality claims. |
| Dense SwiGLU decomposed into eight all-active experts | MoEfication; especially MLPMoE's deterministic slicing and summation | Mapping the identity to OpenVINO's compressed fused operator on this GPU; about 8.1 → 4.5 ms/layer | **Mathematical novelty rejected**. Retain as measured backend optimization and cite the close precedent. |
| Faster stage, barely faster service | Ordinary bottleneck/service-demand reasoning; pipeline literature | Role 0 improves by ~8.2 ms/frame while summed fleet decode gains only ~0.63% | **Empirical support for the paper's systems argument**. Sequential trials and a group-64 canary limit causal isolation. |
| Output-head batching reduces work but lowers throughput | Batching, queueing and autoregressive dependencies are established; Sarathi pipeline-balance work | Head 11.62 → 7.32 ms/frame accompanied by a 2.71% summed-rate regression | **Interesting negative result**, not a new universal law. Prompt tags and a canary change confound the contrast; convoy/reply delay is a supported explanation, not uniquely proved. |
| `16 + 19r` stage model and bandwidth ceiling | Roofline and classical service-demand reasoning | Explicit small-frame approximation, corrected head-traffic accounting and a falsified frame-count prediction | **Model novelty rejected**. Report assumptions and failed prediction; do not claim a topology-independent impossibility. |
| Eight-row prefill windows reduce TTFT | Orca, SARATHI, Sarathi-Serve | Large observed latency benefit in this slow gigabit layer pipeline, with actual request admission behavior | **Application of known scheduling**, valuable measured result. Controlled same-prompt repetition remains needed. |
| Balanced admission, direct token replies, short engine steps | Existing scheduling/pipeline engineering and Cascadia lineage | Concrete fixes in this implementation; cumulative high-concurrency trajectory | **Engineering work**, not separately defensible algorithmic novelty. No attribution of an entire speedup to one bundled change. |
| CPU-reference MTP qualification fails on fleet states | MTP, EAGLE; MoESD, MoE-Spec and SpecMoE | 72.6% CPU-reference agreement becomes 66.81% on fleet sequences and 64.36% on deployment grids; vocabulary versus incremental quantization separated | **Strong secondary empirical finding**. The CPU-to-fleet drop changes both trajectory and numerics; the fixed-fleet vocabulary/quantization comparison is more controlled. |
| Deeper draft modules need correct temporal state | Autoregressive attention/convolution and MTP implementation requirements | Eight-module expected accepted drafts fall from 2.128 teacher-context to 0.769 without deeper context | **Implementation qualification**, not a discovery that temporal models require history. No live speed result. |
| Early-layer logit lens fails to qualify | Tuned Lens | Negative result for this model, states and evaluation/cost protocol | **Narrow negative**, not a proof that intermediate states cannot support drafting. |
| Small-model plus phrase-history ensemble | Existing speculative decoding, n-gram/history drafting, Cascadia shard paper | Conditional task rates and retained-history behavior on this fleet | **Known method, workload-specific characterization**. Repeated-prompt rates cannot represent unseen conversational performance. |
| USB NCM timer improves RTT | Linux `cdc_ncm` documented control, predating this study | Observed adapter latency regime and its distinction from all-to-all saturation | **Tuning result**, not networking novelty or proof of expert-parallel feasibility. |
| OOM diagnosis, group-32 kernel patch, lower GPU wait throttle | OpenVINO backend and operating-system behavior | Version-specific causal evidence and negative speed/power tradeoffs | **Concrete implementation findings**. Do not assert an unresolved current upstream defect without checking a newer revision. |
| Readiness across the whole fixed chain | Existing distributed readiness practices | Probe that delays admission until downstream roles are ready | **Operational improvement**. Does not establish decentralized control, node-loss tolerance or long-run availability. |
| INT4 attention / CPU overlap / full expert parallelism | Quantized projections and disaggregated/expert-parallel systems including Klotski, MegaScale-Infer, EC2MoE | Only INT4 projection microbenchmarks exist; other fleet-serving changes are incomplete | **No achieved end-to-end contribution**. Keep as qualified microbenchmark or future experiment. |

## Same-model comparison that changes the positioning

The [August 2026 author report of Inkling-NVFP4 on eight DGX Sparks](https://forums.developer.nvidia.com/t/inkling-nvfp4-975b-on-8x-dgx-spark/380049) predates this experiment snapshot. It reports tensor parallelism, ConnectX networking and MTP on larger-memory devices. It rules out a broad first-small-cluster or first-unified-memory-cluster claim.

It is not a matched speed baseline: numerical format, context, generation length, parallelism, interconnect, memory capacity, concurrency, software and metric differ. Do not divide its rates by this study's rates to claim a hardware advantage. The report is first-person deployment evidence, not peer-reviewed independent validation.

## What would make the argument substantially stronger

1. Repeat a frozen fifteen-stream baseline and each key optimization on identical randomized workloads. Preserve per-token IDs/timestamps, intervention settings, history-table state and numerical fallback counts.
2. Test the proposed head-batching explanation directly: record frame rows, queue arrival, head launch, reply time and idle time at every role, then vary reply delay without changing weights or prompts.
3. Evaluate quality against the original model on a held-out corpus, separating quantization, fused-path rounding, scale repair and speculative verification.
4. Re-score any trained drafter on disjoint fleet-state prompts and measure real GPU cost, context maintenance and accepted tokens per extra expert byte before claiming service gains.
5. Freeze complete hardware/software/model manifests; add wall power only if energy efficiency becomes a claim.

These are additional research measurements, not work reported as completed in this repository.
