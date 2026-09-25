# Contributions and relationship to prior work

The paper's research claim is **resident serving of a nearly trillion-parameter sparse model on an eleven-machine integrated-GPU fleet, with an execution architecture, streaming runtime and evaluation method designed for that deployment**. Its contributions are architectural, implementation-level and empirical.

This assessment uses the [36-source primary literature ledger](sources.json), reviewed through 2026-09-22. The [annotated bibliography](RELATED_WORK.md) and [search scope](SEARCH_SCOPE.md) record the sources and depth of inspection. The work does not depend on an absolute priority or cross-platform performance-record claim.

## 1. A custom resident MoE engine for shared-memory accelerators

**What we contributed.** A model-specific execution engine for Inkling's 975B decoder across eleven 64 GB Panther Lake devices. Six consecutive layers reside on each machine. The exporter, routing interface, numerical range management and layer runtime connect Inkling's computation to OpenVINO's compressed fused-MoE primitives.

The exporter preserves packed INT4 groups and constructs expert-major graphs that match OpenVINO's existing MoE lowering pattern. Rust computes Inkling's sigmoid/bias-based top-six routing and normalization, then supplies IDs and weights as graph inputs. The two shared experts occupy the same stack and are always selected. Thus the model's routing rules remain explicit while the expert computation uses the accelerated backend.

Numerical range is managed at two levels. A layer's up-projection scales can be attenuated by a power of two, recorded in graph metadata. Each row's routing weights are normalized by a separate power of two so their absolute sum is at most one. The host restores both factors in FP32 before state updates. The paper gives the real-arithmetic identity and distinguishes it from finite-precision behavior.

The resident runtime materializes graph constants for compilation, retains compiled layer models and reusable inference requests, handles row shapes, and coordinates CPU attention/convolution state with iGPU execution. Dense blocks reuse the expert representation through eight all-active slices aligned to the existing quantization groups. Their measured calls decrease from approximately **8.1 to 4.5 ms**, with the FP16 path difference reported.

**Relationship to earlier work.** The [OpenVINO 2026.3.1 primitive](https://github.com/openvinotoolkit/openvino/blob/2026.3.1/src/plugins/intel_gpu/include/intel_gpu/primitives/moe_3gemm_fused_compressed.hpp) and [graph lowering pass](https://github.com/openvinotoolkit/openvino/blob/2026.3.1/src/common/transformations/src/transformations/common_optimizations/convert_tiled_moe_block_to_gather_matmuls.cpp) establish the underlying fused computation and compiler recognition. Cascadia contributes the model-specific representation and execution contract around them. Targeted plugin compatibility patches are supporting backend engineering; the paper's contribution does not depend on claiming a new fused-MoE kernel algorithm.

[SmoothQuant](https://proceedings.mlr.press/v202/xiao23c.html) establishes relevant broader precedent for equivalent rescaling, specifically migration of activation magnitude into weights for W8A8 quantization. Cascadia's layer/row factors address the FP16 expert and FP32 residual boundary. We present the concrete implementation and rationale without asserting priority for numerical scaling generally or attributing this particular routing treatment to SmoothQuant.

MoEfication and MLPMoE establish dense-to-expert decompositions. Cascadia's distinction is the compressed fused-operator realization on Arc B390, group-preserving weight slicing and measured operator benefit inside the resident deployment. Petals, TPI-LLM, prima.cpp, exo and the companion Cascadia papers establish distributed client inference; EdgeMoE and CPU/GPU hybrid work establish sparse execution and placement. The strongest research claim is the combined resident engine architecture and its demonstrated behavior at nearly trillion-parameter scale on this client fleet.

**Evidence.** Four [frozen implementation files](../reproduction/CODE_MAP.md), [dense operator measurements](../reproduction/results/dense.csv), [hardware](../reproduction/results/hardware.json), [concurrency measurements](../reproduction/results/concurrency.csv), and contribution C1 in the [claim map](../reproduction/CLAIMS.md). The manuscript explains the engine in Section 3 and attributes upstream primitives alongside the custom components.

## 2. Streaming service across resident layer shards

**What we contributed.** A serving runtime that coordinates per-stream KV and convolution state, balanced group admission, eight-row prefill windows, parallel CPU attention and direct sampled-token replies across eleven resident stages. The design supports both staggered arrivals and highly concurrent requests using the same stream/state abstraction.

The finalized paired curve spans fifteen concurrency levels from 1 to 176 streams. Its highest mean occurs at 88 streams, eight per pipeline group: **60.29 aggregate decode tokens/s and 46.87 whole-phase tokens/s**. Fifteen streams yield **6.05 s median TTFT**. Throughput varies nonmonotonically with further concurrency while admission latency grows, providing an empirical operating envelope for the resident eleven-stage design. The eight-row alignment describes the measured operating point; isolating row padding, routing and scheduling would require a controlled comparison. Earlier windowed-admission measurements provide supporting configuration evidence.

Section 4.3 develops the lone-stream case: proposals enter as asynchronous frames, target replies verify successive inputs, and a mismatch restores KV and convolution history on every stage. Confident request/shared history and a small CPU draft model supply proposals in the target token space. An earlier CPU-expert same-binary on/off comparison records **6.8–32.8%** gains across three short prompts. The final fused-engine first/repeated observations give **1.80× decode** and **1.69× whole-phase** rate ratios, with speculation active in both passes and history/capture differences explicit. These comparisons support the implemented system's behavior; they do not establish a new speculative-decoding algorithm or assign the peak concurrent throughput to speculation.

**Relationship to earlier work.** Orca and SARATHI/Sarathi-Serve establish iteration-level admission and chunked prefill; speculative decoding and Cascadia's earlier pipelined speculation are also established. The contribution is their integration with compressed resident MoE execution, a gigabit layer pipeline, Inkling's convolution/KV state and a direct autoregressive return path. The paper attributes each primitive and evaluates the resulting system.

**Evidence.** [Paired concurrency curve](../reproduction/results/concurrency.csv), [raw-event reconstruction](../reproduction/results/survey_audit.json), [prefill comparison](../reproduction/results/prefill.csv), and contribution C2 in the [claim map](../reproduction/CLAIMS.md). The fixed-binary survey uses repeated prompt templates with phrase learning active; capture state and pass order are recorded in the methods. The earlier prefill contrast uses distinct prompt tags and is described as an observational configuration comparison.

## 3. Draft evaluation aligned with deployed inference

**What we contributed.** A capture and replay method that evaluates Inkling's shipped MTP head on the distributed model's actual residuals and emitted token IDs. The format uses FP32 residuals, verifies response/input alignment, and preserves each draft module's attention and convolution history. The evaluation covers 36 sequences and 5,724 first-draft prediction targets.

The matched-state analysis distinguishes two numerical design choices. Original/full-head agreement is 66.81%; restricting the original vocabulary to 65,536 entries gives 64.54%; applying INT4/INT8 weight grids at that vocabulary gives 64.36%. Vocabulary selection accounts for 2.271 percentage points of the difference and additional quantization for 0.175 percentage points. This is a deployment-specific empirical result that would be obscured by changing the target trajectories between comparisons.

**Relationship to earlier work.** MTP, EAGLE and speculative decoding establish draft architectures and verification. MoESD, MoE-Spec and SpecMoE connect drafting to sparse-model execution costs. The present contribution connects draft analysis to the distributed quantized serving path through captured states, actual emitted labels and matched-state vocabulary/weight comparisons. These are offline agreement measurements, distinct from the paper's live serving measurements.

**Evidence.** [Capture validation](../reproduction/evidence/source/autolab/experiments/037_fleet_state_capture/validation.json), [fleet rescore](../reproduction/evidence/source/autolab/experiments/039_mtp_fleet_rescore/results.json), [family results](../reproduction/results/mtp_families.csv), and contribution C3 in the [claim map](../reproduction/CLAIMS.md).

## Positioning against the closest same-model deployment

The [earlier Inkling-NVFP4 report on eight DGX Sparks](https://forums.developer.nvidia.com/t/inkling-nvfp4-975b-on-8x-dgx-spark/380049) uses larger-memory devices, tensor parallelism, a different network and MTP. It is relevant same-model context. The present paper contributes the resident Intel iGPU architecture and measurements under its own numerical formats, workloads and communication design; it does not derive a hardware speed comparison from the two reports.

## How the manuscript presents novelty

Each contribution follows **design → implementation → measured result → relationship to prior work**. Experiment numbers and operational chronology are provenance in the claim map. The abstract and introduction identify the completed contributions; the conclusion states the resulting capabilities. The supporting record preserves the data needed to assess each numerical claim.
