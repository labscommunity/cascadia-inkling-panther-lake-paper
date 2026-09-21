# Quantitative and capability claim map

All experiment links below point into the frozen, scrubbed snapshot. Original source commit: `d1ab1abd7387b7f0b83d6d56b7aec2e1a56f9651`. Interpret evidence with [AUDIT.md](AUDIT.md), not a superseded leaderboard conclusion.

Evidence grades: **R** = directly reconstructable from retained structured/raw data; **J** = retained journal/verdict or microbenchmark summary without complete underlying traces; **C** = inspected implementation/configuration; **V** = primary vendor/model source; **D** = derived or conditional analytical estimate; **L** = literature-supported positioning. Grades describe provenance, not statistical confidence.

## Architecture and methods

| ID | Manuscript claim | Evidence and selector | Grade / boundary |
|---|---|---|---|
| H01 | Eleven nominal 64 GB Core Ultra X7 358H machines, 16 logical CPUs | [hardware.json](results/hardware.json); [autolab README](evidence/source/autolab/README.md); [011b telemetry](evidence/telemetry/011b_long_generation.jsonl.gz), `static` and `sys.mem_total` | R/J; nominal installation from operator description |
| H02 | 4P+8E+4LPE, Arc B390/12 Xe, Xe3, 50 NPU TOPS, 9600 MT/s capability | [Source entries](../research/sources.json), `intel358h`, `intelxe3` | V; SKU capability, not exercised rate |
| H03 | OS memory 62757/62615 MiB; kernel; interfaces; power fields | [hardware.json](results/hardware.json), all 11 entries | R; 61.286/61.147 GiB, configuration values not wall power |
| H04 | Fleet frequency not captured; reference 8533 MT/s | [Single-box notes](evidence/source/docs/perf/INKLING_SINGLE_BOX_BENCH.md); [PHYSICS](evidence/source/autolab/PHYSICS.md) | J/D; 136.5 GB/s nominal conditional arithmetic |
| H05 | OpenVINO 2026.3.1; group-size patch is version specific | [029 verdict](evidence/source/autolab/experiments/029_decode_kernels_exact/verdict.md); [022 verdict](evidence/source/autolab/experiments/022_patched_decode_kernel/verdict.md) | J/C; no assertion about newest upstream release |
| H06 | Default sequence limit 1024; NPU and multimodal path unused | [fleet.env](evidence/source/deploy/inkling-fleet/fleet.env); [architecture notes](evidence/source/docs/architectures/inkling.md); [code map](CODE_MAP.md) | C; not maximum demonstrated model capability |
| A01 | 975B total / 41B active | `inkling` model-author source in [bibliography ledger](../research/sources.json) | V; model identity, not derived from fleet allocations |
| A02 | 66 layers; first 2 dense; hidden 6144; dense 24576; expert 3072; 256 routed/top 6 plus 2 shared | [architecture notes](evidence/source/docs/architectures/inkling.md); [code map](CODE_MAP.md); `inklingcard` | C/V |
| A03 | Six consecutive layers per role; FP32 residual payload 24576 bytes/row; direct sampled-token return | [code map](CODE_MAP.md), `layer_split`, `hidden_to_tensor`, `send_stream_decode`, `send_tokens_reply`; [002a](evidence/source/autolab/experiments/002a_return_link/verdict.md) | C/D; 6144 × 4, excludes framing |
| A04 | Group-32 INT4 experts, INT8 attention/head, FP16 fusion; ~52 GiB page budget | [008b](evidence/source/autolab/experiments/008b_all_fused/verdict.md); [fused path research](evidence/source/autolab/research/fused_moe_f16.md); overrides in each experiment | J/C; canary exceptions and fallbacks disclosed |
| M01 | 49 directories, 125 phase records, 34 telemetry archives, 357 evidence files | [manifest](evidence/manifest.json), [inventory](results/inventory.csv), [audit](results/audit.json), `make data` | R; directories include proposals |
| M02 | Two rate definitions; every phase aggregate agrees within rounding | [lab.py](evidence/source/autolab/bench/lab.py); [phases.csv](results/phases.csv), `tokens/(end-start)` | R/C; summed individual rates cannot be recomputed without request traces |
| M03 | First-event/token counting and empty visible text semantics | [code map](CODE_MAP.md); [011b counter audit](results/server_counter_audit.json) | C/R; sparse-MoE backend contract, not generic SSE rule |
| M04 | Burst arrivals ~15 ms; family templates and experiment-tagged prompts | [lab.py](evidence/source/autolab/bench/lab.py) | C; before/after prompts often differ |
| M05 | Gates are prefix/sanity checks; 12-question checks are smoke tests | [lab.py](evidence/source/autolab/bench/lab.py); [007 quality](evidence/source/autolab/experiments/007_fused_f16_all/quality.json); [008b quality](evidence/source/autolab/experiments/008b_all_fused/quality.json) | C/R; no general model-quality guarantee |
| M06 | Clock repair, deduplication, role mapping; five incomplete/failed phase rows | [telemetry_analysis.py](evidence/source/autolab/bench/telemetry_analysis.py); [036](evidence/source/autolab/experiments/036_telemetry_roles/verdict.md); [audit](results/audit.json) | R/C; software profile samples, limited repeats |

## Serving results

| ID | Claim / paper table | Evidence and selector | Grade / boundary |
|---|---|---|---|
| P01 | Throughput table: 005/007/008b/009/011 at 176 streams | [evolution.csv](results/evolution.csv), each `s176`; original phases via [inventory](EXPERIMENTS.md) | R; caps 48/32 differ, cumulative changes |
| P02 | 011b: 176/176, 21549 tokens, 371.9 s, 57.948 whole-phase, 70.235 summed decode; TTFT mean 50.52 s | [011b phases](evidence/source/autolab/experiments/011b_long_generation/phases.json), `long176`; [counter audit](results/server_counter_audit.json) | R; server/client counts match exactly |
| P03 | Counter n=14, median 70.6665, mean 45.8637; 352 result 54.9 | [counter CSV](results/server_counter_011b.csv), endpoint inflight ≥170; [009 phases](evidence/source/autolab/experiments/009_dense_igpu/phases.json), `s352` | R; selected bins include prefill; 352 value rounded |
| P04 | Baseline fifteen-stream TTFT medians 31.52/31.23 s, whole-phase 15.678/17.005 | [prefill.csv](results/prefill.csv), 019 `mix15a/b` | R |
| P05 | Eight-row windows: median TTFT 6.91 s, whole-phase 22.521, sum 24.626 | [024 phases](evidence/source/autolab/experiments/024_prefill_windows/phases.json), `mix15a`; [verdict](evidence/source/autolab/experiments/024_prefill_windows/verdict.md) | R/J; not identical-prompt randomized A/B |
| P06 | Isolated TTFT 1.96/2.11; staggered median 2.48; 027 per-stream median 1.654/1.636 | Same 024 phases `fresh1a/b`, `stag15`; [027 phases](evidence/source/autolab/experiments/027_rank0_dense_as_moe/phases.json), `mix15a/b` | R; specific small samples |
| P07 | 015c task-conditioned ~3.1–10.95 tokens/s | [015 verdict](evidence/source/autolab/experiments/015_drafter_model/verdict.md); [015c phases](evidence/source/autolab/experiments/015c_ensemble/phases.json) | R/J; explain range in verdict, six family rows in JSON; not family-wide averages |
| P08 | Phrase transfer repeated code 5.225 → 10.600 | [038 baseline](evidence/source/autolab/experiments/038_phrase_transfer/phases-baseline.json), [after](evidence/source/autolab/experiments/038_phrase_transfer/phases.json), [verdict](evidence/source/autolab/experiments/038_phrase_transfer/verdict.md) | R; baseline learns, release changes, no unseen/general causal claim |

## Kernels, traffic and failures

| ID | Claim | Evidence and selector | Grade / boundary |
|---|---|---|---|
| K01 | Dense 8.15/8.11 → 4.51/4.45 ms one-row, errors 5.7e-4/5.9e-4 | [027 verdict](evidence/source/autolab/experiments/027_rank0_dense_as_moe/verdict.md) load-check table | J; two finite-precision implementations, not BF16 quality evaluation |
| K02 | Dense algebra is established | `mlpmoe`, `moefication` in [sources](../research/sources.json) | L; all slices active, unit weights |
| K03 | Role 0 compute 51.8882 → 43.6809 ms; summed-rate mean 24.6355 → 24.790 | [profiles.csv](results/profiles.csv), 026/027 `mix15a`, role 0; respective phase means | R/D; ~0.6271%, canary and prompt caveats |
| K04 | Head time 11.6202 → 7.3154 ms, role compute 35.9650 → 35.0848 | Same profiles, 027/028 `mix15a`, role 10 | R; “compute” excludes separately reported head |
| K05 | Head batching mean 24.790 → 24.1185 = −2.70875% | [derived.json](results/derived.json), mean of `mix15a/b` in 027 and 028 | R/D; scheduling explanation is inference |
| B01 | Small-frame model `t(r)≈16+19r` ms, r~1–3 | [PHYSICS](evidence/source/autolab/PHYSICS.md) | J/D; descriptive local approximation, not formal fitted law |
| B02 | Cycle bound `max(sum(stage times), F*max(stage time))` | Paper derivation under equal-frame, fixed-cost cyclic service assumptions; Roofline/service-demand attribution | D; no universal queueing novelty |
| B03 | Ten frames: 24.580/24.679 → 24.596/24.444; 176 streams 67.974 → 64.846 | [034 baseline](evidence/source/autolab/experiments/034_inflight10/phases-baseline.json), [ten frames](evidence/source/autolab/experiments/034_inflight10/phases.json); [derived](results/derived.json) | R; same tag/binary, prediction falsified |
| B04 | ~27.1 GB logical weights/token: expert16.76, attention8.59, dense0.52, head1.24 | [PHYSICS](evidence/source/autolab/PHYSICS.md), export-size accounting | J/D; 64×8×32.74 MB +66×130.1 MB+2×262 MB+1.235694528 GB, approximate |
| B05 | Middle cycle32.1 GB; final45.7 GB; conditional45 tokens/s | Same notes plus paper's explicit correction: `11*.78+15*1.57+11*1.235694528`; `15*136.5/bytes` | D; assumes no inter-frame reuse and stated bandwidth; no DRAM-counter measurement |
| B06 | CPU60–65 GB/s not bus peak; head ~108 GB/s | [PHYSICS](evidence/source/autolab/PHYSICS.md); [027](evidence/source/autolab/experiments/027_rank0_dense_as_moe/verdict.md); head byte/time calculation | J/D; logical effective rates |
| F01 | Nonfinite layer and duplicate fallback cache | [007](evidence/source/autolab/experiments/007_fused_f16_all/verdict.md), [008b](evidence/source/autolab/experiments/008b_all_fused/verdict.md) | J/R; not a comprehensive numerical correctness proof |
| F02 | 021/022 apparent GPU crash revised to OOM chain | [025 verdict](evidence/source/autolab/experiments/025_crash_evidence/verdict.md) | J; later diagnosis supersedes initial classification |
| F03 | Group-32 patch succeeds but 3.0–3.2 ms one-row calls not faster | [029](evidence/source/autolab/experiments/029_decode_kernels_exact/verdict.md) | J; tested plugin only |
| N01 | Input-tensor reuse no material service gain | [020](evidence/source/autolab/experiments/020_gpu_idle_diagnostic/verdict.md) and phases | R/J; tested implementation |
| N02 | Two GPU threads1.04–1.10×, below1.25 bar | [023](evidence/source/autolab/experiments/023_split_bench/verdict.md), [split_bench.json](evidence/source/autolab/experiments/023_split_bench/split_bench.json) | R/J; microbenchmark, not proof all overlap fails |
| N03 | Group-64 canary changes weights | [026](evidence/source/autolab/experiments/026_decode_kernel_group64/verdict.md), [028](evidence/source/autolab/experiments/028_head_batching/verdict.md) | J/C; disclosed confound |
| N04 | Sleeping GPU wait adds ~2.3 ms/frame | [029 verdict](evidence/source/autolab/experiments/029_decode_kernels_exact/verdict.md) | J; canary package/CPU saving, no wall-energy claim |
| N05 | USB timer small RTT3.3 →0.2–0.3 ms | [014](evidence/source/autolab/experiments/014_lan_latency_probe/verdict.md); official `cdc` source | J/L; both endpoints; not whole-model latency |
| N06 | All-to-all100 kB; all11 only30/50 MB/s; achieved41–45 at50 | [018 results](evidence/source/autolab/experiments/018_all_to_all_network/results.json), [verdict](evidence/source/autolab/experiments/018_all_to_all_network/verdict.md) | R/J; topology diagnosis inference, no EP inference result |
| N07 | Role relocation; readiness | [032](evidence/source/autolab/experiments/032_role_swap/verdict.md), [035](evidence/source/autolab/experiments/035_chain_readiness/verdict.md) | J/R/C; historical tests not rerun; no sustained reliability result |

## Drafting and incomplete work

| ID | Claim | Evidence and selector | Grade / boundary |
|---|---|---|---|
| D01 | 033 CPU MTP:36 sequences,12 families,160 generated positions,5724 targets, agreement0.726 | [033 verdict](evidence/source/autolab/experiments/033_mtp_offline_study/verdict.md), [full tables](evidence/source/autolab/research/mtp_offline/results/tables_mtp.txt) | J; raw tensor captures absent; no live speed |
| D02 | 039 original0.668064,65k0.645353,grids0.643606; .70 bar missed | [039 results](evidence/source/autolab/experiments/039_mtp_fleet_rescore/results.json), `original_a1`, `prefix.65536`, `quantized_a1`; [hypothesis](evidence/source/autolab/experiments/039_mtp_fleet_rescore/hypothesis.md) | R/J; JSON regenerated into derived tables, neural rescore not rerun |
| D03 | Incremental quantization loss0.174703 percentage points; family story/code/arithmetic | [derived](results/derived.json), [families](results/mtp_families.csv) | R/D; three sequences per family, deployment values0.482180/0.746331/0.748428 |
| D04 | Eight-module expected accepted drafts2.128/2.007/.769 | [039 results](evidence/source/autolab/experiments/039_mtp_fleet_rescore/results.json) and [verdict](evidence/source/autolab/experiments/039_mtp_fleet_rescore/verdict.md) | R/J; teacher/self-fed/no-deeper-context, not runtime throughput |
| D05 | FP16 overflow; residual magnitude4272968;36 FP32 responses match | [037](evidence/source/autolab/experiments/037_fleet_state_capture/verdict.md), [validation](evidence/source/autolab/experiments/037_fleet_state_capture/validation.json), [039 capture matches](evidence/source/autolab/experiments/039_mtp_fleet_rescore/capture_matches.json) | R/J; emitted fleet IDs remain target; 92.12% BF16-head agreement not quality |
| D06 | Raw first-five-boundary probe≈0; affine0.34–0.39 below bars | [033](evidence/source/autolab/experiments/033_mtp_offline_study/verdict.md), [final tables](evidence/source/autolab/research/mtp_offline/results/tables_final.txt) | J; specific probe protocol, not impossibility proof |
| U01 | 040 interrupted:41partial layers,0timed phases | [interruption.json](evidence/source/autolab/experiments/040_expert_usage/interruption.json) | R; no expert-usage result |
| U02 | INT4 attention39.0–43.2% shorter calls;9.6–9.7% relative RMS | [041 results](evidence/source/autolab/experiments/041_attention_int4/results.json), [derived CSV](results/attention_int4.csv) | R/D; two layers × one/two rows, random-input microbenchmark |
| U03 | Fleet-trained draft, INT4 serving canary, CPU overlap, EP serving unfinished | [complete inventory](EXPERIMENTS.md),042–045hypotheses | C/J; code existence/export success does not establish deployment benefit |

Figures are generated from `results/` by `scripts/plot.py`. Headline macros in `generated/numbers.tex` come from the same frozen inputs. The full literature-to-novelty mapping is separate in [NOVELTY.md](../research/NOVELTY.md).
