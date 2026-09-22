# Contribution and quantitative claim map

This map follows the manuscript's contribution-based organization. Experiment identifiers are source selectors, not the paper's narrative structure. The supporting evidence is frozen at Cascadia commit `3189a189fe3428f5a6315a7eb67b13148ec314e2`.

Evidence types: **R** — retained structured/raw measurement; **J** — retained load-check or research summary; **C** — inspected implementation/configuration; **V** — model/vendor primary source; **D** — arithmetic derived from those inputs. These types describe provenance, not statistical confidence. [AUDIT.md](AUDIT.md) defines the metrics and reconstruction rules.

## C1. Resident execution across shared-memory accelerators

| Claim | Source and selector | Evidence / interpretation |
|---|---|---|
| Inkling: 975B total / 41B active parameters | `inkling` and `inklingcard` in [source ledger](../research/sources.json) | V; model identity |
| Eleven nominal 64 GB machines; 704 GB nominal aggregate | [Hardware table](results/hardware.json); [source deployment description](evidence/source/autolab/README.md) | R/J/D; separate machine address spaces |
| Core Ultra X7 358H: 4P + 8E + 4LPE, 16 threads; Arc B390 with 12 Xe cores and Xe3; up to 9600 MT/s, NPU 50 INT8 TOPS | `intel358h`, `intelxe3` in [source ledger](../research/sources.json) | V; hardware capability; execution uses CPU and iGPU |
| Usable memory 62757/62615 MiB; kernel 7.0.0-31-generic; eight USB NCM and three PCIe-style interfaces at 1000 Mb/s | [hardware.json](results/hardware.json), all 11 entries, reconstructed from [long-run telemetry](evidence/telemetry/011b_long_generation.jsonl.gz) | R; 61.286/61.147 GiB per machine |
| OpenVINO 2026.3.1 and default 1024 sequence positions | [runtime record](evidence/source/autolab/experiments/029_decode_kernels_exact/verdict.md); [fleet defaults](evidence/source/deploy/inkling-fleet/fleet.env) | J/C |
| 66 layers; first 2 dense 24576, remaining 64 MoE width 3072; hidden 6144; top 6 of 256 routed plus 2 shared | [architecture notes](evidence/source/docs/architectures/inkling.md), [code map](CODE_MAP.md), model-card source | C/V |
| Six consecutive layers per role, FP32 residuals, 24,576 bytes/row, direct sampled-ID return | [code map](CODE_MAP.md), `layer_split`, `hidden_to_tensor`, `send_stream_decode`, `send_tokens_reply` | C/D; payload 6144×4, before protocol metadata |
| Group 32 INT4 experts; INT8 projections/head; FP16 fused arithmetic; approximately 52 GiB GPU page budget | [resident configuration](evidence/source/autolab/experiments/008b_all_fused/verdict.md); [fused path notes](evidence/source/autolab/research/fused_moe_f16.md) and experiment overrides | J/C; normal placement, with observable fallback counters |
| Dense-to-eight-slice representation, all slices active with unit weights | [dense implementation record](evidence/source/autolab/experiments/027_rank0_dense_as_moe/verdict.md), [code map](CODE_MAP.md); `mlpmoe`/`moefication` references | C/J; real-arithmetic identity with prior attribution |
| Dense layer 0: 8.15→4.51 ms; layer 1: 8.11→4.45 ms; reductions 44.7%/45.1%; relative differences 5.7e-4/5.9e-4 | [dense.csv](results/dense.csv), rows=1; parsed from the preceding load-check table | J/D; two FP16 execution paths |
| Two-row dense calls 8.41 ms each versus 4.47/4.48 ms | [dense.csv](results/dense.csv), rows=2 | J; operator measurements |
| Role 0 computation 51.9→43.7 ms/frame | [profiles.csv](results/profiles.csv),026/027 `mix15a`, role 0: 51.8881988/43.6808835 | R; stage-profile measurements, distinct from fleet rates |
| Logical bytes per unshared token: experts 16.76 GB, attention 8.59 GB, dense 0.52 GB, head 1.24 GB; total≈27.1 GB | [weight-size accounting](evidence/source/autolab/PHYSICS.md):64×8×32.74 MB +66×130.1 MB +2×262 MB +1.235694528 GB | J/D; logical bytes, not measured DRAM traffic |

## C2. Streaming service across resident layer shards

| Claim | Source and selector | Evidence / interpretation |
|---|---|---|
| Stream-local KV/convolution state, group admission, short engine steps, direct return | [code map](CODE_MAP.md), engine and stage/attention functions; recorded mechanisms in 001,002a,005,006 | C; integrated runtime design |
| Eight-row prefill windows and CPU row-parallel attention | [window configuration](evidence/source/autolab/experiments/024_prefill_windows/verdict.md), [attention configuration](evidence/source/autolab/experiments/011_parallel_attention/verdict.md) | C/J |
| Full-chain readiness before admission | [readiness record](evidence/source/autolab/experiments/035_chain_readiness/verdict.md) | C/J; completed serving/runtime feature |
| Finalized survey: 33 phases, 1,592 requests, 203,776 tokens; two additional pilots | [survey_audit.json](results/survey_audit.json), [measurements](evidence/source/autolab/experiments/046_final_performance/measurements.json) | R/D; thirty mixed phases and three explanation-family phases; 35 records including pilots |
| Paired curve at 1,2,4,6,8,11,15,22,32,48,64,88,96,128,176 streams | [concurrency.csv](results/concurrency.csv), reconstructed by [analyze_survey.py](scripts/analyze_survey.py) | R/D; arithmetic means of two phase rates; pooled request TTFT quantiles |
| Highest measured paired mean at 88 streams: 60.286375 shared decode, 46.874876 whole-phase tokens/s | Same curve, concurrency=88; [raw events](evidence/requests/046_final_performance/) | R/D; common interval uses latest first event and earliest last event in each cohort |
| 88-stream phases: 11,264 tokens each; shared rates 58.860866/61.711884; whole-phase 46.026388/47.723364 | [survey_phases.csv](results/survey_phases.csv), `mixed_a_c088`, `mixed_b_c088` | R/D; shared token counts 8,538/8,550; eight streams per each of eleven groups |
| 176 streams: 57.715692 shared decode, 45.242551 whole-phase tokens/s | [concurrency.csv](results/concurrency.csv), concurrency=176 | R/D; final paired survey definition |
| 15 streams: 24.604266 shared decode, 22.116880 whole-phase; pooled TTFT median 6.052471 s, p95 10.113574 s | Same curve, concurrency=15 | R/D; thirty requests across two phases |
| Single-stream first/repeated pass: 5.676968/10.243011 shared decode; 5.194607/8.765184 whole-phase | [survey_phases.csv](results/survey_phases.csv), `mixed_a_c001`, `mixed_b_c001`; [text comparisons](evidence/source/autolab/experiments/046_final_performance/single-stream-comparison.json) | R/D; all 12 prompt/output pairs identical through 128 tokens; active phrase history and differing capture/order |
| Survey protocol: fixed release 1790016660; INT4 group 32 experts; INT8 attention/head; 128 tokens; temperature 0; 15 ms arrival spacing | [performance harness](evidence/source/autolab/bench/performance_sweep.py), [survey data](evidence/source/autolab/experiments/046_final_performance/measurements.json), [protocol record](evidence/source/autolab/experiments/046_final_performance/report.md) | C/R; binary SHA-256 `9084392040688eaa6aa9ff6cf6d222f84e24e119e528d91920d12ddd106563c2`; ascent/reverse pairs plus 88 refinement |
| Phrase learning active; capture writes on ascending 1–15, off thereafter; 79 unique prompts at 88 streams | [survey_phases.csv](results/survey_phases.csv), source harness and phase records | C/R/D; request history is part of the measured system |
| Windowed 15-request burst: 1,920 tokens, 22.521 whole-phase, median TTFT 6.91 s | [024 phases](evidence/source/autolab/experiments/024_prefill_windows/phases.json), `mix15a` | R; earlier supporting configuration comparison |
| Staggered 15-request median TTFT 2.48 s | Same phases, `stag15` | R; approximately one-second arrivals and 96-token output cap |
| Reference 15-request medians 31.52/31.23 s and whole-phase 15.678/17.005 | [019 phases](evidence/source/autolab/experiments/019_baseline_15_streams/phases.json), `mix15a/b`; [prefill.csv](results/prefill.csv) | R; observational configuration comparison |
| Approximately 4.5-fold median TTFT reduction | Reference 31.23–31.52 divided by 6.91 | D; different prompt tags |
| Event multiplicities agree with API usage; short prefix/known-answer checks | [finalized harness](evidence/source/autolab/bench/performance_sweep.py), [historical harness](evidence/source/autolab/bench/lab.py); [code map](CODE_MAP.md) | C/R; first-token events include structural/reasoning tokens; functional checks are not a quality benchmark |

## C3. Draft evaluation aligned with deployed inference

| Claim | Source and selector | Evidence / interpretation |
|---|---|---|
| FP32 residual capture with emitted IDs and input/response alignment | [capture record](evidence/source/autolab/experiments/037_fleet_state_capture/verdict.md), [validation](evidence/source/autolab/experiments/037_fleet_state_capture/validation.json), [capture matches](evidence/source/autolab/experiments/039_mtp_fleet_rescore/capture_matches.json) | R/J/C; evaluated FP32 corpus |
| Sampled pre-final-normalization magnitude 4272968 | Same capture record | J; motivates FP32 state representation |
| 36 sequences, 3 per 12 families,160 generated positions, 5760 tokens, 5724 first-draft labels | [fleet rescore](evidence/source/autolab/experiments/039_mtp_fleet_rescore/results.json), [rescore record](evidence/source/autolab/experiments/039_mtp_fleet_rescore/verdict.md) | R/J; token IDs emitted by serving path are labels |
| Eight modules, each with attention and convolution history; teacher/self-fed replay | [MTP implementation description](evidence/source/autolab/research/mtp_offline/README.md), [scoring implementation](evidence/source/autolab/research/mtp_offline/mtp_score.py), rescore protocols | C/J |
| Full-head agreement 0.6680642907; original 65k 0.6453529001; quantized 65k 0.6436058700 | [rescore JSON](evidence/source/autolab/experiments/039_mtp_fleet_rescore/results.json), `original_a1`, `prefix.65536`, `quantized_a1` | R; matched states/labels, offline FP32 arithmetic |
| Vocabulary difference 2.271139 pp; incremental quantization 0.174703 pp | [derived.json](results/derived.json), `mtp_vocabulary_difference_pp`, `mtp_incremental_quantization_loss_pp` | D; percentage points, not relative percentages |
| Deployment-grid family agreement: code 0.746331, arithmetic 0.748428, story 0.482180 | [mtp_families.csv](results/mtp_families.csv) | R; three sequences per family |
| Expected accepted drafts across eight modules 2.128 true-token/2.007 self-fed | [fleet rescore record](evidence/source/autolab/experiments/039_mtp_fleet_rescore/verdict.md) and protocol summary data | J/R; descriptive offline chain result, not runtime speed |

## Artifact and related work

The [manifest](evidence/manifest.json) records 417 evidence-file hashes. The reconstruction enumerates 160 phase records in 50 source directories, 35 fleet telemetry archives and 36 request/stat archives. Figures are generated from the derived CSV files by `scripts/plot.py`; the four paper charts are `concurrency`, `dense`, `prefill` and `mtp`. A supporting `counter` chart accompanies the data audit.

The [contribution assessment](../research/NOVELTY.md) maps the three contributions to the closest primary literature. The bibliography ledger contains 33 sources; the manuscript selects the sources relevant to its stated contributions.
