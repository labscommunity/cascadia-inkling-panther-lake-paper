# Contributions and relationship to prior work

The paper's research claim is **resident serving of a nearly trillion-parameter sparse model on an eleven-machine integrated-GPU fleet, with an execution architecture, streaming runtime and evaluation method designed for that deployment**. Its contributions are architectural, implementation-level and empirical.

This assessment uses the [33-source primary literature ledger](sources.json), reviewed through 2026-09-21. The [annotated bibliography](RELATED_WORK.md) and [search scope](SEARCH_SCOPE.md) record the sources and depth of inspection. The work does not depend on an absolute priority or cross-platform performance-record claim.

## 1. Resident execution across shared-memory accelerators

**What we contributed.** An implemented execution path for Inkling's 975B decoder across eleven 64 GB Panther Lake devices. Six consecutive layers reside on each machine. Operator-specific compression and CPU/iGPU placement coordinate compressed experts, attention projections, dense blocks, state and host memory within each shard's shared capacity budget.

A common fused-expert representation accommodates the dense feed-forward layers as eight all-active slices as well as routed/shared MoE layers. The dense-layer load checks measure approximately 8.1 → 4.5 ms, with the finite-precision difference explicitly reported. This unifies the backend path for two kinds of layer in the resident deployment.

**Relationship to earlier work.** Petals, TPI-LLM, prima.cpp and exo establish client-cluster inference. The companion Cascadia paper establishes the project's Intel/OpenVINO pipeline lineage. EdgeMoE, PowerInfer and subsequent hybrid/distributed MoE work establish sparse execution and placement techniques. This paper extends that space with the implemented combination of near-trillion-scale expert residency, 64 GB integrated-GPU devices, operator unification and measured concurrent service.

MoEfication and MLPMoE provide prior art for dense-to-expert decomposition. The contribution here is the compressed fused-operator realization on Arc B390 and its use inside the complete Inkling execution architecture. The algebra receives explicit attribution.

**Evidence.** [Dense operator measurements](../reproduction/results/dense.csv), [hardware](../reproduction/results/hardware.json), [implementation anchors](../reproduction/CODE_MAP.md) and contribution C1 in the [claim map](../reproduction/CLAIMS.md).

## 2. Streaming service across resident layer shards

**What we contributed.** A serving runtime that coordinates per-stream KV and convolution state, balanced group admission, eight-row prefill windows, parallel CPU attention and direct sampled-token replies across eleven resident stages. The design supports both staggered arrivals and highly concurrent requests using the same stream/state abstraction.

The complete 176-request workload generates 21,549 tokens in 371.9 s, for 57.948 whole-phase tokens/s. Fifteen-request bursts record median TTFT of 6.91 s with windowed admission, compared with 31.23–31.52 s in the reference configuration. Staggered arrivals record 2.48 s median TTFT. The rates and latency measurements demonstrate the implemented system at explicit operating points.

**Relationship to earlier work.** Orca and SARATHI/Sarathi-Serve establish iteration-level admission and chunked prefill; speculative decoding is also established. The contribution is their integration with compressed resident MoE execution, a gigabit layer pipeline, Inkling's convolution/KV state and a direct autoregressive return path. The paper attributes each primitive and evaluates the resulting system.

**Evidence.** [Serving configurations](../reproduction/results/serving.csv), [prefill comparison](../reproduction/results/prefill.csv), [independent server-counter check](../reproduction/results/server_counter_audit.json), and contribution C2 in the [claim map](../reproduction/CLAIMS.md). Configuration contrasts use the recorded prompt tags and are described as observational comparisons.

## 3. Draft evaluation aligned with deployed inference

**What we contributed.** A capture and replay method that evaluates Inkling's shipped MTP head on the distributed model's actual residuals and emitted token IDs. The format uses FP32 residuals, verifies response/input alignment, and preserves each draft module's attention and convolution history. The evaluation covers 36 sequences and 5,724 first-draft prediction targets.

The matched-state analysis distinguishes two numerical design choices. Original/full-head agreement is 66.81%; restricting the original vocabulary to 65,536 entries gives 64.54%; applying INT4/INT8 weight grids at that vocabulary gives 64.36%. Vocabulary selection accounts for 2.271 percentage points of the difference and additional quantization for 0.175 percentage points. This is a deployment-specific empirical result that would be obscured by changing the target trajectories between comparisons.

**Relationship to earlier work.** MTP, EAGLE and speculative decoding establish draft architectures and verification. MoESD, MoE-Spec and SpecMoE connect drafting to sparse-model execution costs. The present contribution connects draft analysis to the distributed quantized serving path through captured states, actual emitted labels and matched-state vocabulary/weight comparisons. These are offline agreement measurements, distinct from the paper's live serving measurements.

**Evidence.** [Capture validation](../reproduction/evidence/source/autolab/experiments/037_fleet_state_capture/validation.json), [fleet rescore](../reproduction/evidence/source/autolab/experiments/039_mtp_fleet_rescore/results.json), [family results](../reproduction/results/mtp_families.csv), and contribution C3 in the [claim map](../reproduction/CLAIMS.md).

## Positioning against the closest same-model deployment

The [earlier Inkling-NVFP4 report on eight DGX Sparks](https://forums.developer.nvidia.com/t/inkling-nvfp4-975b-on-8x-dgx-spark/380049) uses larger-memory devices, tensor parallelism, a different network and MTP. It is relevant same-model context. The present paper contributes the resident Intel iGPU architecture and measurements under its own numerical formats, workloads and communication design; it does not derive a hardware speed comparison from the two reports.

## How the manuscript presents novelty

Each contribution follows **design → implementation → measured result → relationship to prior work**. Experiment numbers and operational chronology are provenance in the claim map. The abstract and introduction identify the completed contributions; the conclusion states the resulting capabilities. The supporting record preserves the data needed to assess each numerical claim.
