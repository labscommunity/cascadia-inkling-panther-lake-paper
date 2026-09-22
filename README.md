# Cascadia: Resident 975B MoE Inference on Eleven AI PCs

Research manuscript by **Tate Berenbaum**, **Matias Parij** (Community Labs), and **Muthaiah Venkatachalam** (Intel Corporation). Private author-review draft, September 2026.

[Read the paper (PDF)](main.pdf) · [LaTeX source](main.tex) · [Contributions and prior work](research/NOVELTY.md) · [Claim map](reproduction/CLAIMS.md)

The paper presents Cascadia's execution of Inkling's 975B text decoder on eleven Intel Core Ultra X7 358H machines, each with nominal 64 GB memory, Arc B390 integrated graphics and gigabit Ethernet. It develops three contributions:

1. **Resident execution on shared-memory accelerators.** Layer partitioning, operator-specific compression and CPU/iGPU placement distribute the model across the fleet. A common fused-expert representation supports both dense and sparse feed-forward blocks; the measured dense-layer call takes about **4.5 ms**, compared with **8.1 ms** for three compressed matrix operations.
2. **A streaming pipeline for concurrent serving.** Per-stream KV/convolution state, balanced admission, eight-row prefill windows and a direct token-return path coordinate generation. The fleet serves **176 concurrent requests at 57.948 whole-phase tokens/s**. A fifteen-request burst records **6.91 s median TTFT**, compared with **31.23–31.52 s** in the reference configuration.
3. **Draft evaluation using deployed states.** FP32 residual capture, emitted token IDs and stateful draft replay enable matched-state numerical comparisons. Vocabulary restriction accounts for **2.271 percentage points** of first-draft agreement difference; further quantization at that vocabulary accounts for **0.175 percentage points**.

The contribution is the architecture, implementation and empirical findings of this integrated system. [The prior-work assessment](research/NOVELTY.md) explains how it extends the [Cascadia architecture manuscript](https://github.com/labscommunity/cascadia-architecture-paper), [pipeline-shard paper](https://arxiv.org/abs/2608.19147) and related research. Established algebra and scheduling primitives are credited where used.

## Demonstrated serving configurations

| Workload | Requests | Output cap | Whole-phase tokens/s | Sum of request decode rates | Median TTFT |
|---|---:|---:|---:|---:|---:|
| Long-generation burst | 176 | 128 | 57.948 | 70.235 | — |
| Windowed burst | 15 | 128 | 22.521 | 24.626 | 6.91 s |
| Windowed staggered | 15 | 96 | 20.148 | 24.169 | 2.48 s |
| Isolated request A | 1 | 48 | 3.961 | 4.628 | 1.96 s |
| Isolated request B | 1 | 48 | 3.488 | 4.035 | 2.11 s |

Every request in these rows completed. The long-generation run produced **21,549 tokens in 371.9 s**, independently matched by the server counter; its retained TTFT summary is a mean of **50.52 s**. The sum of request decode rates uses differing request intervals and is distinct from simultaneous aggregate throughput. Configuration comparisons describe the recorded workloads; prompt tags and arrival patterns are documented in the claim map.

## Build and data

The included evidence supports offline reconstruction of the reported measurements:

```sh
make data       # Reconstruct tables with Python 3.10+ standard library
make figures    # Generate paper charts with pinned Matplotlib through uv
make            # Build the PDF with Tectonic or pdfLaTeX + BibTeX
make verify     # Check evidence, metrics, citations and report links
```

The [evidence snapshot](reproduction/evidence/manifest.json) covers 49 source experiment directories, 125 phase records, 34 scrubbed telemetry archives and 357 hashed evidence files. [Measurement documentation](reproduction/README.md) describes the reconstruction; [CLAIMS.md](reproduction/CLAIMS.md) connects each paper contribution to its records. The preserved source archive supplies provenance independently of the paper's contribution-based organization.

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
