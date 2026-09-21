# Literature-search scope and limits

Search and inspection date: **2026-09-21**. There are **33 source entries**, not 33 peer-reviewed papers. The collection includes research papers/preprints, official vendor and software documentation, two companion manuscripts, a model card/announcement, a project repository and a first-person deployment report.

The search followed the measured mechanisms rather than searching only for the exact machine name. It covered these question families:

| Question | Search concepts and follow-up sources |
|---|---|
| Has this model already run on a small unified-memory cluster? | Inkling 975B distributed inference, DGX Spark, NVFP4, multi-node deployment; the first-person eight-Spark report and model author's announcement/card. |
| Is consumer-device pipeline inference new? | Distributed/edge/home-cluster LLM inference, Petals, TPI-LLM, prima.cpp, exo; companion Cascadia manuscript and public pipeline-shard v1. |
| Is resident sparse inference on client memory new? | MoE memory bandwidth, CPU/GPU hybrid, expert placement, EdgeMoE, PowerInfer, Klotski, MegaScale-Infer, EC2MoE and 2026 hybrid-serving work. |
| Is dense-to-fused-expert decomposition new? | Dense MLP splitting, static/all-active experts, MoEfication, MLPMoE. The last is particularly close to the algebra used here. |
| Are chunked prefill and pipeline scheduling novel? | Orca, SARATHI, Sarathi-Serve, pipeline uniformity, admission and latency/throughput tradeoffs. |
| Is the drafting argument new? | Speculative decoding, MTP, EAGLE, MoESD, MoE-Spec, SpecMoE, intermediate-state probes and Tuned Lens. |
| What hardware is actually specified? | Intel's 358H SKU table, Panther Lake architecture presentation and Series 3 edge white paper. Fleet telemetry remains the source for installed configuration. |
| Are backend/network controls established? | Official Linux v7.0 `cdc_ncm` sysfs documentation and OpenVINO runtime option source. Local pinned artifacts govern claims about the tested plugin. |

This table records search coverage, not an exact reproducible browser-query transcript. Search results were followed to primary sources; secondary summaries are not technical evidence in the manuscript. The `review` field in [sources.json](sources.json) identifies whether inspection covered full HTML, a publication abstract, documentation, indexed PDF text or only source location/metadata. Do not represent an abstract-only inspection as a full-paper review. In particular, MLPMoE's primary abstract explicitly supports the slicing/summation overlap; its HTML was unavailable.

The companion pipeline paper's public arXiv v1 and local working manuscript differ. We cite its architectural lineage, without importing a local draft number as a published benchmark. The architecture manuscript is cited as a repository manuscript; publication acceptance is not assumed.

Mutable model cards, vendor tables and repository `master` URLs were inspected as available on the search date. The bibliography carries access dates. That does not create immutable source snapshots: a public artifact release should archive permissible metadata or pin revisions. The local experiment evidence, in contrast, is content-hashed at an explicit commit.

Coverage is sufficient to reject several broad novelty claims and identify a plausible empirical contribution. It is not a systematic review with a preregistered inclusion protocol, exhaustive forward/backward citation graph, independent double screening or proof of absence. Relevant work after the cutoff is outside this assessment. Search should be refreshed before public submission.
