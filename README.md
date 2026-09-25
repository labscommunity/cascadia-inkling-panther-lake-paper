# Cascadia: Resident 975B MoE Inference on Eleven AI PCs

Research manuscript by **Tate Berenbaum**, **Matias Parij** (Community Labs), and **Muthaiah Venkatachalam** (Intel Corporation). Private author-review draft, September 2026.

[Read the paper (PDF)](main.pdf) · [LaTeX source](main.tex) · [Contributions and prior work](research/NOVELTY.md) · [Claim map](reproduction/CLAIMS.md)

The paper presents Cascadia's execution of Inkling's 975B text decoder on eleven Intel Core Ultra X7 358H machines, each with nominal 64 GB memory, Arc B390 integrated graphics and gigabit Ethernet. It develops three contributions:

1. **A custom resident MoE engine for shared-memory accelerators.** Cascadia builds Inkling-specific compressed graphs, retains its routing rules in Rust, and manages FP16 expert computation with FP32 output restoration around OpenVINO's fused iGPU primitives. Layer residency and reusable inference requests fit this execution into each machine's shared memory. Dense layers use eight all-active expert slices, reducing measured calls from about **8.1 ms to 4.5 ms**.
2. **A streaming pipeline for concurrent serving.** Per-stream KV/convolution state, balanced admission, eight-row prefill windows and a direct token-return path coordinate generation. Paired measurements from **1 to 176 streams** reach **60.29 aggregate decode tokens/s** and **46.87 whole-phase tokens/s** at **88 streams**, eight per pipeline group. At fifteen streams, median TTFT is **6.05 s**.
3. **Draft evaluation using deployed states.** FP32 residual capture, emitted token IDs and stateful draft replay enable matched-state numerical comparisons. Vocabulary restriction accounts for **2.271 percentage points** of first-draft agreement difference; further quantization at that vocabulary accounts for **0.175 percentage points**.

The contribution is the architecture, implementation and empirical findings of this integrated system. [The prior-work assessment](research/NOVELTY.md) explains how it extends the [Cascadia architecture manuscript](https://github.com/labscommunity/cascadia-architecture-paper), [pipeline-shard paper](https://arxiv.org/abs/2608.19147) and related research. Established algebra and scheduling primitives are credited where used.

## Custom engine contribution

Section 3 explains the exporter, routing interface, resident runtime and numerical range management, with a diagram showing Cascadia's responsibilities and OpenVINO's execution boundary. The engine preserves existing INT4 groups, treats routed and shared experts through one interface, and uses per-layer up-projection attenuation plus per-row routing normalization with FP32 restoration. Dense and sparse blocks share the fused representation.

OpenVINO supplies the compressed MoE primitive and graph lowering. The paper attributes those mechanisms and the prior art for equivalent rescaling and dense-to-expert decomposition; its contribution is the implemented engine and measured results in this deployment. [Implementation anchors](reproduction/CODE_MAP.md) and the [novelty assessment](research/NOVELTY.md) connect that claim to source evidence.

## Speculative decoding scenarios

Section 4.3 illustrates matching proposals, partial agreement and target-only progress, explains how in-flight verification reduces pipeline latency, and reports measured gains. A same-binary speculation off/on comparison in the earlier CPU-expert configuration records **6.8%, 14.0% and 32.8%** decode-rate gains on three short prompts, with all responses recorded as exact reference matches. The finalized fused-engine survey records **1.80× decode** and **1.69× whole-phase** first/repeated-prompt rate ratios across twelve identical output pairs. Both final passes enable speculation; their contrast includes accumulated history and differing capture settings.

The [speculation audit](reproduction/AUDIT.md#speculative-decoding-scenarios-and-comparisons), [derived measurements](reproduction/results/speculation_audit.json) and [runtime anchors](reproduction/CODE_MAP.md) distinguish measured on/off gains, repeated-prompt behavior and the illustrative latency model.

## Finalized performance measurements

The fixed-binary survey measures fifteen concurrency levels twice, using twelve prompt families and 128 output tokens per request. Selected operating points:

| Concurrent streams | Aggregate decode tokens/s | Whole-phase tokens/s | Median TTFT | p95 TTFT |
|---:|---:|---:|---:|---:|
| 1 | 7.96 | 6.98 | 2.18 s | 2.41 s |
| 15 | 24.60 | 22.12 | 6.05 s | 10.11 s |
| 32 | 38.31 | 32.48 | 13.44 s | 21.90 s |
| 64 | 53.60 | 42.41 | 25.10 s | 46.41 s |
| 88 | 60.29 | 46.87 | 34.61 s | 64.75 s |
| 128 | 50.10 | 41.61 | 55.11 s | 108.73 s |
| 176 | 57.72 | 45.24 | 76.83 s | 165.34 s |

Decode throughput counts tokens over intervals when every request in a cohort is decoding; whole-phase throughput includes admission, prefill, queueing and drain. Rates average two phases; latency quantiles pool their requests. Phrase learning remains active across repeated prompts, and the [measurement protocol](reproduction/AUDIT.md) records ordering and capture state. The highest paired mean on the measured grid occurs at 88 streams.

![Finalized concurrency curve](figures/concurrency.png)

The [full curve](reproduction/results/concurrency.csv) and [raw-event reconstruction](reproduction/results/survey_audit.json) accompany the paper. The complete survey comprises **33 measured phases, 1,592 requests and 203,776 output tokens**, with two additional pilot records preserved separately. Earlier windowed-admission measurements support the configuration analysis.

## Build and data

The included evidence supports offline reconstruction of the reported measurements:

```sh
make data       # Reconstruct tables with Python 3.10+ standard library
make figures    # Generate paper charts with pinned Matplotlib through uv
make            # Build the PDF with Tectonic or pdfLaTeX + BibTeX
make verify     # Check evidence, metrics, citations and report links
```

The [evidence snapshot](reproduction/evidence/manifest.json) covers 50 source experiment directories, 160 phase records, 35 fleet telemetry archives, 36 request/stat archives and 421 hashed evidence files. [Measurement documentation](reproduction/README.md) describes the reconstruction; [CLAIMS.md](reproduction/CLAIMS.md) connects each paper contribution to its records. The preserved source archive supplies provenance independently of the paper's contribution-based organization.

## Supporting material

- [Hardware and capability](reproduction/HARDWARE.md)
- [Runtime architecture and code anchors](reproduction/CODE_MAP.md)
- [Metric and evidence audit](reproduction/AUDIT.md)
- [Annotated primary sources](research/RELATED_WORK.md) and [search scope](research/SEARCH_SCOPE.md)
- [Derived result tables](reproduction/results/) and [validation record](reproduction/VALIDATION.md)

## Authors

- Tate Berenbaum — Community Labs — tb@communitylabs.com
- Matias Parij — Community Labs — mparij@communitylabs.com
- Muthaiah Venkatachalam — Intel Corporation — muthaiah.venkatachalam@intel.com
