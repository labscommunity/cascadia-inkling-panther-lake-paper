# Annotated primary sources

Initial search: 2026-09-21; custom-engine attribution extended 2026-09-22. Summaries are interpretive notes, not quotations. Citation metadata follows the version explicitly identified below.

## inkling: Inkling: Our Open-Weights Model

[model author announcement](https://thinkingmachines.ai/news/introducing-inkling/) · 2026

Model identity and parameter counts; no third-party capability scores adopted.

975B total and 41B active parameters; this study evaluates the text path only.

## inklingcard: Inkling Model Card

[model author model card](https://huggingface.co/thinkingmachines/Inkling) · 2026

Architecture and license sections inspected.

66 layers, six routed of 256 plus two shared experts; base model is multimodal. This does not establish multimodal support in Cascadia's exported path.

## intel358h: Intel Core Ultra X7 Processor 358H: Specifications

[vendor specification](https://www.intel.com/content/www/us/en/products/sku/245527/intel-core-ultra-x7-processor-358h-18m-cache-up-to-4-80-ghz/specifications.html) · 2026

CPU, memory, GPU and NPU specification tables inspected.

16 cores/threads (4P+8E+4LPE), Arc B390 with 12 Xe cores, 50 INT8 NPU TOPS, LPDDR5X up to 9600 MT/s. These are SKU capabilities, not measured fleet frequencies or inference rates.

## intelptl: Intel Technology Tour 2025: Panther Lake Recap

[vendor architecture presentation](https://cdrdv2-public.intel.com/866361/ITT_2025_Panther_Lake_Recap1.pdf) · 2025

Architecture presentation located; Xe3 family attribution corroborated by Intel's edge white paper.

Panther Lake combines CPU, Xe3 graphics and NPU; heterogeneous accelerators share a client platform, not independent HBM banks.

## intelxe3: Industrial and Robotics Innovation with Intel Core Ultra Processors (Series 3)

[vendor architecture white paper](https://builders.intel.com/docs/networkbuilders/industrial-and-robotics-innovation-with-intel-core-ultra-processors-series-3-1767869217.pdf) · 2026

Primary vendor description of Xe3 graphics inspected through indexed document text.

Corroborates Xe3 architecture, CPU/GPU/NPU integration; do not substitute generic platform maxima for the installed machines.

## shards: Pre-Compiled Pipeline Shards for Distributed LLM Inference on Intel AI PC Fleets

[companion preprint](https://arxiv.org/abs/2608.19147) · 2026

Local LaTeX and reproduction files plus public arXiv v1 HTML inspected. Public and local numerical revisions differ; no old speedup imported.

Pipeline shards, Intel iGPU execution, speculative decoding and microbatching are existing Cascadia work. New paper must establish the large-MoE measurement contribution separately.

## architecture: Cascadia: A Control-Plane-Free Alternative to Hyperconverged AI Infrastructure

[companion repository manuscript](https://github.com/labscommunity/cascadia-architecture-paper) · 2026

Local main.tex, claims/reproduction conventions and author information inspected; no publication status inferred.

Supplies Cascadia system context and evidence-map conventions. Its mesh, receipt and availability claims are not measurements of this fixed eleven-stage fleet.

## petals: Petals: Collaborative Inference and Fine-tuning of Large Models

[research preprint](https://arxiv.org/abs/2209.01188) · 2023

Primary abstract and companion citation inspected.

Consumer-device pipeline inference predates this study; pooling insufficient individual memories is not new.

## prima: PRIMA.CPP: Speeding Up 70B-Scale LLM Inference on Low-Resource Everyday Home Clusters

[research preprint](https://arxiv.org/abs/2504.08791v1) · 2025

v1 full HTML, piped-ring design, assignment model and evaluation inspected; later project publication has a different author list, so this citation is explicitly v1.

Ring execution, CPU/GPU layer placement and OS-sensitive memory behavior are prior art. Cascadia measures a resident, much larger sparse model at multiple concurrency regimes.

## tpi: TPI-LLM: Serving 70B-scale LLMs Efficiently on Low-resource Edge Devices

[research preprint](https://arxiv.org/abs/2410.00531) · 2024

Primary abstract inspected.

Already distinguishes pipeline's single-user limitations from tensor-parallel communication costs; no claim to invent this tradeoff.

## exo: exo: Run Frontier AI Locally

[official software repository](https://github.com/exo-explore/exo) · 2026

Official repository inspected as a contemporary system lead; no benchmark comparison inferred.

Distributed local inference is a populated software category. Hardware, model format and workload would need matched measurements for a speed comparison.

## edgemoe: EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices

[research preprint](https://arxiv.org/abs/2308.14352v2) · 2025

Primary metadata and abstract inspected; v1 2023, revised v2 2025.

Sparse-model deployment under edge memory limits is established; the specific resident iGPU fleet remains the empirical distinction.

## powerinfer: PowerInfer: Fast Large Language Model Serving with a Consumer-grade GPU

[research preprint](https://arxiv.org/abs/2312.12456) · 2023

Primary abstract inspected.

CPU/GPU exploitation of sparsity on consumer hardware is prior art, though a discrete GPU/host split differs from shared LPDDR memory.

## klotski: Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline

[research preprint](https://arxiv.org/abs/2502.06888) · 2025

Full primary HTML and multi-batch offload framing inspected.

Expert-aware batching and pipeline bubbles are existing problems. Our limited gains from additional rows are measurements of this backend, not an inherent no-reuse law for MoE.

## megascale: MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism

[research preprint](https://arxiv.org/abs/2504.02263) · 2025

Full primary HTML and attention/FFN disaggregation design inspected.

Independent scaling of attention and experts and communication-hiding microbatches predate this work; datacenter interconnect assumptions differ.

## ec2moe: EC2MoE: Adaptive End-Cloud Pipeline Collaboration Enabling Scalable Mixture-of-Experts Inference

[research preprint](https://arxiv.org/abs/2508.06024) · 2025

Primary abstract inspected.

Heterogeneous edge/cloud MoE scheduling and routing are prior art. No first distributed edge MoE claim is supportable.

## hybrid2026: Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design

[research preprint (OSDI 2026 accepted per authors)](https://arxiv.org/abs/2606.10493) · 2026

Primary abstract, authors, hardware and submission date inspected.

A contemporary CPU/discrete-GPU MoE system already addresses concurrency and prefill/decode overlap. Neither cheap local MoE nor overlap is a unique contribution here.

## sparkinkling: Inkling-NVFP4 (975B) on Eight DGX Spark Systems

[first-person deployment report; not peer reviewed](https://forums.developer.nvidia.com/t/inkling-nvfp4-975b-on-8x-dgx-spark/380049) · 2026

Full post inspected; first posted 2026-08-13. TP=8, 128 GB UMA/node, CX-7, NVFP4 and MTP; workload 128 input/128 output, ten rounds per level.

Earlier deployment of the same 975B model on a small UMA cluster defeats broad first-model/first-UMA-cluster claims. Reported C=1 27.3 tok/s and about 62 aggregate at C=4 cannot be compared directly to our different precision/network/concurrency.

## orca: Orca: A Distributed Serving System for Transformer-Based Generative Models

[OSDI paper](https://www.usenix.org/conference/osdi22/presentation/yu) · 2022

Primary proceedings abstract inspected.

Iteration-level scheduling and selective batching are prior art; the admission bug is an implementation finding.

## sarathi: SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills

[research preprint](https://arxiv.org/abs/2308.16369) · 2023

Primary abstract inspected, including pipeline uniformity argument.

Chunked prefill and uniform-work batches already address pipeline imbalance. Eight-row windows are a hardware-specific application, not a new scheduling invention.

## sarathiserve: Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

[OSDI paper](https://www.usenix.org/conference/osdi24/presentation/agrawal) · 2024

Primary proceedings page inspected.

Latency/throughput tradeoffs in chunked-prefill serving are established; compare mechanisms rather than unrelated speedups.

## specdecode: Fast Inference from Transformers via Speculative Decoding

[ICML paper](https://proceedings.mlr.press/v202/leviathan23a.html) · 2023

Primary arXiv abstract and proceedings PDF inspected.

Exact speculative sampling is prior art. Our temperature-zero verification only supports claims about preserving the chosen serving path's greedy output.

## eagle: EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty

[research preprint](https://arxiv.org/abs/2401.15077) · 2024

Primary abstract inspected.

Feature-based drafting and MoE evaluation are established. A proposed fleet-trained feature head is future work, not a result.

## mtp: Better and Faster Large Language Models via Multi-token Prediction

[research preprint](https://arxiv.org/abs/2404.19737) · 2024

Primary abstract inspected.

Multi-token heads and their inference use predate Inkling; measuring the shipped head is characterization, not inventing MTP.

## moesd: MoESD: Unveil Speculative Decoding's Potential for Accelerating Sparse MoE

[research preprint](https://arxiv.org/abs/2505.19645) · 2025

Full primary HTML, target-efficiency and moderate-batch analysis inspected.

Already shows acceptance alone is insufficient and verification cost depends on active experts and batch size. The general speculation argument is not novel.

## moespec: MoE-Spec: Expert Budgeting for Efficient Speculative Decoding

[research preprint](https://arxiv.org/abs/2602.16052) · 2026

Primary full HTML and expert-budget motivation inspected.

Additional speculative branches activate experts and increase bandwidth pressure. Its expert dropping changes the comparison to the present full top-six path.

## specmoe: SpecMoE: A Fast and Efficient Mixture-of-Experts Inference via Self-Assisted Speculative Decoding

[research preprint](https://arxiv.org/abs/2604.10152) · 2026

Primary abstract inspected.

Self-assisted speculation for memory-constrained MoE is prior art; our shipped-head study adds a negative deployment qualification result.

## moefication: MoEfication: Transformer Feed-forward Layers are Mixtures of Experts

[ACL Findings paper](https://aclanthology.org/2022.findings-acl.71/) · 2022

Primary publication page inspected.

Dense feed-forward decomposition into experts is established. Preserve all active slices here and describe only the compiler/backend realization as the implementation distinction.

## mlpmoe: MLPMoE: Zero-Shot Architectural Metamorphosis of Dense LLM MLPs into Static Mixture-of-Experts

[research preprint](https://arxiv.org/abs/2511.21089) · 2025

Primary abstract explicitly describes deterministic tensor slicing and summation; HTML unavailable.

Particularly close prior art to the all-active algebra. Do not claim a novel mathematical transformation or first dense-to-MoE mapping.

## tunedlens: Eliciting Latent Predictions from Transformers with the Tuned Lens

[research preprint](https://arxiv.org/abs/2303.08112) · 2023

Primary metadata inspected.

Intermediate-state vocabulary probes and affine corrections are prior art. Failed early-boundary probes are specific to this study and training protocol.

## cdc: Linux cdc_ncm sysfs ABI

[official kernel documentation](https://github.com/torvalds/linux/blob/v7.0/Documentation/ABI/testing/sysfs-class-net-cdc_ncm) · 2026

v7.0 documentation inspected; timer API predates this study by years.

Aggregation timer tuning is an existing interface. Measured RTT improvement and workload consequences are the empirical result.

## ovoptions: OpenVINO Intel GPU Runtime Configuration Options

[official runtime source](https://github.com/openvinotoolkit/openvino/blob/master/src/plugins/intel_gpu/include/intel_gpu/runtime/options.inl) · 2026

MoE GEMV threshold and grouped GEMM options inspected. Master is mutable; use local hashed 2026.3.1 evidence for the defect claim.

Decode/prefill dispatch is a backend configuration choice, not a new kernel introduced by this work.

## roofline: Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures

[author-institution research archive](https://escholarship.org/uc/item/5tz795vq) · 2009

Primary archive located for bandwidth-model attribution.

Byte/time bounds are established performance analysis, and require measured or explicitly assumed bandwidth.

## ovmoe: OpenVINO 2026.3.1: Compressed Fused Three-GEMM MoE Primitive

[official GPU plugin source, pinned release](https://github.com/openvinotoolkit/openvino/blob/2026.3.1/src/plugins/intel_gpu/include/intel_gpu/primitives/moe_3gemm_fused_compressed.hpp) · 2026 · inspected 2026-09-22

Release-tagged primitive interface inspected alongside the Cascadia exporter and runtime call path.

OpenVINO supplies the compressed fused-MoE primitive. Cascadia contributes model-specific graph construction, routing interface, numerical range handling and the resident distributed runtime.

## ovmoelowering: OpenVINO 2026.3.1: Tiled MoE Graph Lowering

[official graph transformation source, pinned release](https://github.com/openvinotoolkit/openvino/blob/2026.3.1/src/common/transformations/src/transformations/common_optimizations/convert_tiled_moe_block_to_gather_matmuls.cpp) · 2026 · inspected 2026-09-22

Release-tagged graph matcher inspected against build_layer in the pinned Inkling exporter.

Tiled MoE graph recognition and lowering are upstream mechanisms. Cascadia constructs a matching graph with external Inkling routing and an expert-major compressed representation.

## smoothquant: SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models

[ICML paper](https://proceedings.mlr.press/v202/xiao23c.html) · 2023 · inspected 2026-09-22

Primary proceedings abstract and bibliographic metadata inspected; broader equivalent-rescaling precedent, not an assertion of identical routing treatment.

Equivalent transformations for numerical range and quantization have prior art. SmoothQuant migrates activation outliers into weights for W8A8; Cascadia uses per-row routing normalization and per-layer up-projection attenuation with FP32 restoration for fused FP16 MoE execution.
