# A 975B Mixture-of-Experts Model on Eleven AI PCs

**Memory, Scheduling, and Numerical Limits of Integrated-GPU Inference**

Research manuscript by **Tate Berenbaum**, **Matias Parij** (Community Labs), and **Muthaiah Venkatachalam** (Intel Corporation). Private author-review draft, September 2026.

[Read the paper (PDF)](main.pdf) · [LaTeX source](main.tex) · [Novelty assessment](research/NOVELTY.md) · [Evidence and corrections](reproduction/AUDIT.md) · [Claim map](reproduction/CLAIMS.md)

This paper examines Cascadia serving Inkling's text decoder on eleven Intel Core Ultra X7 358H machines, each with nominal 64 GB memory, Arc B390 integrated graphics and gigabit Ethernet. It extends the [Cascadia architecture manuscript](https://github.com/labscommunity/cascadia-architecture-paper) and [pipeline-shard paper](https://arxiv.org/abs/2608.19147) with a large-MoE deployment study.

The evidence snapshot contains **49 experiment directories, 125 phase records, 34 scrubbed telemetry archives and 357 hashed source/evidence files**. It includes unsuccessful and unfinished work. No new fleet experiments were run while preparing this retrospective artifact.

## What the evidence supports

| Observation | Result | Interpretation |
|---|---|---|
| 176 concurrent requests, output cap 128 | 21,549 generated tokens in 371.9 s: **57.948 tokens/s** over the entire phase | Independently matched by the server token counter. The sum of individual decode rates is **70.235 tokens/s**, a different metric. |
| Fifteen concurrent requests | Baseline median TTFT 31.23–31.52 s; eight-row prefill windows 6.91 s | Substantial observed admission improvement; most phases are not identical-prompt randomized comparisons. |
| Dense layers mapped to fused expert operations | Approximately 8.1 → 4.5 ms per dense layer | A useful backend optimization with close prior art; fleet gain is only about 0.63% in the recorded comparison. |
| Output-head batching | Head time 11.62 → 7.32 ms/frame; summed decode rates **regress 2.71%** | Local work savings do not guarantee service gains in an autoregressive pipeline. Mechanistic attribution remains qualified. |
| Shipped draft head | CPU-reference first-draft agreement 72.6%; fleet-state agreement **66.81%**, deployment grids **64.36%** | The later fleet study misses the 70% qualification bar; offline acceptance is not live speed. |

The strongest candidate contribution is a measured systems characterization: memory residency and fallback behavior, the gap between stage optimization and fleet service, and draft qualification on the actual deployed numerical path. Distributed inference, dense-to-expert algebra, prefill chunking and speculative decoding all have prior art. [The literature review](research/RELATED_WORK.md) contains 33 primary sources and distinguishes papers, official documentation, companion work and an earlier same-model deployment report.

## Reproduce the report

The checked-in PDF and figures can be read without installing anything. To regenerate the analysis from the included evidence:

```sh
make data       # Python 3.10+ standard library; no fleet/model/network needed
make verify     # Evidence, metrics, citations, artifact links and privacy checks
make figures    # uv + pinned matplotlib; first use downloads dependencies
make            # Tectonic, or pdflatex + BibTeX; first Tectonic use may download TeX packages
```

See [reproduction/README.md](reproduction/README.md) for exact scope and provenance. These commands regenerate reported results; they do not reproduce inference without model assets and hardware. Archived operator scripts are evidence, not instructions to deploy.

## Reading guide

- [All 49 experiment dispositions](reproduction/EXPERIMENTS.md)
- [Hardware: installed configuration versus vendor capabilities](reproduction/HARDWARE.md)
- [Runtime architecture and code anchors](reproduction/CODE_MAP.md)
- [Every quantitative claim and its source](reproduction/CLAIMS.md)
- [Corrections to the autolab summaries](reproduction/AUDIT.md)
- [Literature-search scope](research/SEARCH_SCOPE.md) and [publication plan](research/PUBLICATION_PLAN.md)
- [Machine-readable results](reproduction/results/) and [evidence hashes](reproduction/evidence/manifest.json)

Before submission, the highest-value additions are controlled repeated A/B measurements, a held-out model-quality evaluation, and complete hardware/model manifests. The manuscript already makes those limitations explicit. Repository creation does not submit the paper or make its artifact public.

## Authors

- Tate Berenbaum — Community Labs — tb@communitylabs.com
- Matias Parij — Community Labs — mparij@communitylabs.com
- Muthaiah Venkatachalam — Intel Corporation — muthaiah.venkatachalam@intel.com

Author order follows the authors' requested order; contact information follows the companion Cascadia papers. No contribution-role, employer-endorsement or conflict-of-interest declarations are inferred.
