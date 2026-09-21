# Complete experiment inventory

All 49 directories in the frozen snapshot are accounted for below. A phase row is a recorded attempt, not an independent scientific replicate or proof of a successful intervention. See [machine-readable inventory](results/inventory.csv), [all phase records](results/phases.csv) and [corrections](AUDIT.md).

Status is an editorial assessment from retained evidence, not a copy of the moving queue. "Kept" describes the historical intervention decision, not the fleet's current configuration. No experiments were rerun for this artifact.

| Experiment | Phase rows | Telemetry | Assessment | Evidence-based disposition |
|---|---:|---|---|---|
| [001_balanced_groups](evidence/source/autolab/experiments/001_balanced_groups/) | 5 | yes | Measured / kept | Balanced group admission and initial scheduling fixes; cumulative baseline, not an isolated algorithm contribution. |
| [002a_return_link](evidence/source/autolab/experiments/002a_return_link/) | 3 | yes | Measured / kept | Direct final-to-first token return fills the pipeline more effectively. |
| [002b_speculation](evidence/source/autolab/experiments/002b_speculation/) | 3 | yes | Measured / kept | Single-stream speculative scheduling; verification follows the deployed path, not an original-model quality proof. |
| [003_per_rank_ab](evidence/source/autolab/experiments/003_per_rank_ab/) | 3 | yes | Measured / mixed | Per-rank CPU/iGPU trials and fused FP16 qualification; ranks differ in hardware and layer assignment. |
| [004_row_gemm_prewarm_batchadmit](evidence/source/autolab/experiments/004_row_gemm_prewarm_batchadmit/) | 4 | yes | Measured / kept | Row GEMM, prewarm and batch admission bundle; admission lock starvation remains. |
| [005_short_steps](evidence/source/autolab/experiments/005_short_steps/) | 5 | yes | Measured / kept | Short engine steps improve service; 176 streams complete with a 48-token cap. |
| [006_admit_while_waiting](evidence/source/autolab/experiments/006_admit_while_waiting/) | 3 | yes | Measured / kept with failure | Admit while waiting; 264-request phase completes only 251 and has connection errors. |
| [007_fused_f16_all](evidence/source/autolab/experiments/007_fused_f16_all/) | 5 | yes | Measured / qualified | Partial fused-expert rollout; nonfinite fallback/cache duplication; 264-request phase incomplete. |
| [008a_six_fused_one_rank](evidence/source/autolab/experiments/008a_six_fused_one_rank/) | 2 | yes | Measured / canary | Six fused layers fit on one rank; local capacity qualification before fleet rollout. |
| [008b_all_fused](evidence/source/autolab/experiments/008b_all_fused/) | 5 | yes | Measured / kept with failure | All-fused fleet path and removal of CPU copies; 176 completes, 352 attempt incomplete. |
| [009_dense_igpu](evidence/source/autolab/experiments/009_dense_igpu/) | 4 | yes | Measured / kept | Dense layers moved to iGPU; completed 352-request run is slower by summed decode rate than 176. |
| [010_after_seeding](evidence/source/autolab/experiments/010_after_seeding/) | 4 | yes | Measured / negative | Phrase-table seeding does not materially improve unseen prompts; repeated prompts differ. |
| [011_parallel_attention](evidence/source/autolab/experiments/011_parallel_attention/) | 3 | yes | Measured / kept | CPU attention parallelized across rows; 176-stream sum of decode rates64.175. |
| [011b_long_generation](evidence/source/autolab/experiments/011b_long_generation/) | 1 | yes | Measured / confirmation | Longer 128-token-cap phase; client 21,549 tokens independently equals server counter delta. |
| [012_single_stream_anatomy](evidence/source/autolab/experiments/012_single_stream_anatomy/) | 3 | yes | Measured / diagnostic | Single-stream traversal and idle-time anatomy; no new configuration improvement claimed. |
| [013_acceptance_study](evidence/source/autolab/experiments/013_acceptance_study/) | 0 | no | Offline / measured | Study-generated 192-sequence corpus and small-model/ngram acceptance; teacher-forced agreement is not live speed. |
| [014_lan_latency_probe](evidence/source/autolab/experiments/014_lan_latency_probe/) | 0 | no | Probe / measured | USB NCM aggregation timer; both-endpoint low-latency confirmation occurs with 015 deployment. |
| [015_drafter_model](evidence/source/autolab/experiments/015_drafter_model/) | 5 | yes | Measured / superseded variants | Initial drafter release fails progress watchdog; later variants fix loop and combine table/model proposals. |
| [015c_ensemble](evidence/source/autolab/experiments/015c_ensemble/) | 6 | yes | Measured / kept | Six retained task-family phase rows; broad prose range comes from015 verdict, not six independent family means. |
| [016_distill_data](evidence/source/autolab/experiments/016_distill_data/) | 0 | no | Incomplete | Distillation data collection proposal; no retained result establishes a trained drafter gain. |
| [017_rollback](evidence/source/autolab/experiments/017_rollback/) | 0 | no | Operational / no result | Rollback directory; no timed phase or scientific verdict retained. |
| [018_all_to_all_network](evidence/source/autolab/experiments/018_all_to_all_network/) | 0 | no | Probe / measured negative | Model-idle all-to-all traffic; low-rate steps are partial fleet; all 11 at30/50 MB/s; no EP serving result. |
| [019_baseline_15_streams](evidence/source/autolab/experiments/019_baseline_15_streams/) | 5 | yes | Measured / baseline | Five service phases including paired fifteen-stream reference; raw phases govern numbers. |
| [020_gpu_idle_diagnostic](evidence/source/autolab/experiments/020_gpu_idle_diagnostic/) | 3 | yes | Measured / negative | Input reuse and GPU idle diagnostics; no meaningful measured service improvement. |
| [021_moe_decode_kernel](evidence/source/autolab/experiments/021_moe_decode_kernel/) | 2 | yes | Failed / reverted | Two timed phases complete zero requests; apparent GPU crash later revised by 025 to fallback/OOM chain. |
| [022_patched_decode_kernel](evidence/source/autolab/experiments/022_patched_decode_kernel/) | 0 | no | Failed / reverted | Offset patch insufficient; gate retained but no successful timed phase;025 revises cause. |
| [023_split_bench](evidence/source/autolab/experiments/023_split_bench/) | 1 | yes | Microbenchmark / negative | Two-thread GPU call overlap 1.04–1.10x below 1.25 threshold; split-stage design not justified by this probe. |
| [024_prefill_windows](evidence/source/autolab/experiments/024_prefill_windows/) | 4 | yes | Measured / kept | Eight-row prefill windows; median TTFT 6.91 s burst and 2.48 s staggered at 15 streams. |
| [025_crash_evidence](evidence/source/autolab/experiments/025_crash_evidence/) | 0 | no | Diagnostic / revised cause | Historical crash evidence identifies failed inference, fallback cache growth and OOM. |
| [026_decode_kernel_group64](evidence/source/autolab/experiments/026_decode_kernel_group64/) | 2 | yes | Measured / canary | Group-64 decode kernel works but changes quantization; comparison is not unchanged-weight parity. |
| [027_rank0_dense_as_moe](evidence/source/autolab/experiments/027_rank0_dense_as_moe/) | 3 | yes | Measured / local gain | Dense-as-eight-active-experts cuts role 0 compute; fleet sum-rate gain only ~0.63%; close algebraic prior art. |
| [028_head_batching](evidence/source/autolab/experiments/028_head_batching/) | 3 | yes | Measured / negative | Head batching saves head work but regresses sum-rate mean 2.71%; canary/prompt confounds disclosed. |
| [029_decode_kernels_exact](evidence/source/autolab/experiments/029_decode_kernels_exact/) | 3 | yes | Measured / negative | Group-32 patch and sleeping GPU waits work but do not improve measured service; controls removed. |
| [030_clean_exact](evidence/source/autolab/experiments/030_clean_exact/) | 0 | yes | Operational / telemetry only | Clean configuration archive; telemetry exists but no retained timed-phase JSON or verdict. |
| [031_single_stream_check](evidence/source/autolab/experiments/031_single_stream_check/) | 7 | yes | Measured / diagnostic | Seven single-stream records across before-swap and later files; history/ordering affects interpretation. |
| [032_role_swap](evidence/source/autolab/experiments/032_role_swap/) | 2 | yes | Measured / kept | Roles 0 and 8 swapped; ingress remains on original box; short test does not establish hardware repair. |
| [033_mtp_offline_study](evidence/source/autolab/experiments/033_mtp_offline_study/) | 0 | no | Offline / superseded qualification | CPU-sequence MTP 0.726 and logit-lens study; live speed is projected, later fleet 039 misses bar. |
| [034_inflight10](evidence/source/autolab/experiments/034_inflight10/) | 8 | yes | Measured / negative | Same binary/tag frame-count contrast; 10 frames fail predicted benefit and regress 176-stream summed rate 4.60%. |
| [035_chain_readiness](evidence/source/autolab/experiments/035_chain_readiness/) | 2 | yes | Measured / operational keep | Full-chain readiness; historical delayed-start integration tests and two load phases; no throughput gain claimed. |
| [036_telemetry_roles](evidence/source/autolab/experiments/036_telemetry_roles/) | 0 | no | Harness / kept | Preserve box/role identities, deduplicate and align clocks; no separate timed serving phase. |
| [037_fleet_state_capture](evidence/source/autolab/experiments/037_fleet_state_capture/) | 4 | yes | Capture / corrected | Initial FP16 captures overflow; FP32 captures validate 36 sequences; both initial/final timing files retained. |
| [038_phrase_transfer](evidence/source/autolab/experiments/038_phrase_transfer/) | 12 | yes | Measured / history dependent | Transfer phrase history and disable captures; repeated-prompt gains confounded by learning during baseline. |
| [039_mtp_fleet_rescore](evidence/source/autolab/experiments/039_mtp_fleet_rescore/) | 0 | no | Offline / negative qualification | Fleet original 0.6681 and deployment grid 0.6436 first-draft agreement miss 0.70; no multi-stream MTP serving. |
| [040_expert_usage](evidence/source/autolab/experiments/040_expert_usage/) | 0 | yes | Interrupted | Zero completed timed phases, 41 partial expert layers; training collection not started; no usage distribution result. |
| [041_attention_int4](evidence/source/autolab/experiments/041_attention_int4/) | 0 | no | Microbenchmark / qualified | INT4 attention 39.0–43.2% faster projection calls, 9.6–9.7% random-input relative RMS difference; no fleet quality/speed result. |
| [042_fleet_draft_training](evidence/source/autolab/experiments/042_fleet_draft_training/) | 0 | no | Unfinished / proposal | Fleet-state draft training plan; no qualified held-out trained-head result. |
| [043_attention_int4_canary](evidence/source/autolab/experiments/043_attention_int4_canary/) | 0 | no | Unfinished / proposal | INT4 attention serving canary planned; no measured canary result. |
| [044_cpu_overlap](evidence/source/autolab/experiments/044_cpu_overlap/) | 0 | no | Unfinished / proposal | CPU attention/router overlap preparation; no completed fleet benefit measurement. |
| [045_expert_parallel_serving](evidence/source/autolab/experiments/045_expert_parallel_serving/) | 0 | no | Unfinished / proposal | Expert-parallel serving preparation; code/proposals do not constitute full-model fleet EP validation. |
