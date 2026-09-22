# Metric and evidence audit

The manuscript reports implemented designs and measured capabilities. This document records the interpretation rules connecting those claims to the preserved source evidence.

## Throughput and first-token latency

`aggregate_tok_s` is total counted tokens divided by the full phase duration, including admission and completion. For all 125 archived phase records, recomputing this value from unrounded start/end timestamps matches three-decimal storage rounding.

`sum_stream_tok_s` sums each request's decode rate over its own first-to-last token interval. Those intervals can differ; the number is reported separately from simultaneous aggregate throughput. For the 176-request long-generation workload, the respective figures are **57.948** and **70.235** tokens/s.

The long workload's raw server counter increases by exactly **21,549** tokens, matching the client. Its full duration is **371.9 s**. The supporting counter plot uses disjoint five-poll intervals; the paper's headline throughput uses the complete phase rather than a selected interval.

The inspected backend emits one counted event per model token, including reasoning and structural tokens. TTFT refers to the first such event. The long workload supplies a mean TTFT of 50.52 s; the interactive workload tables explicitly use medians. The paper does not substitute one statistic for the other.

## Configuration and operator comparisons

Reference and windowed fifteen-request phases use the same 128-token output cap but different prompt tags. Their latency comparison is an observed configuration comparison. Isolated, staggered and long-generation workloads have the caps and arrival patterns stated in the serving table.

Dense-layer times come from retained one-/two-row load checks. The derived `dense.csv` extracts those values and computes reductions of 44.7%/45.1% for one row. The FP16 path differences of 5.7e-4/5.9e-4 are reported alongside the real-arithmetic decomposition. The role 0 profile comparison is a separate stage measurement; operator savings are not presented as an isolated fleet-throughput multiplier.

The additional fifteen-request results with fused dense blocks include the historical group 64 expert canary, identified in the paper. The principal windowed serving result uses the preceding group 32 configuration.

## Profiles and numerical labels

Profile windows are deduplicated and aligned using receipt age on the operator clock. Physical device identity and pipeline role are kept separate. Stage times are frame-weighted software-profile averages. GPU timings retain associated fallback counters.

Draft evaluation uses actual emitted fleet token IDs as labels. Vocabulary and weight-format comparisons use the same 36 captured sequences and 5724 prediction targets. The reported **2.271139** and **0.174703 percentage-point** differences are reconstructed from the raw agreement values. The quantized calculation uses FP32 arithmetic offline, and draft agreement is distinguished from live serving throughput.

Functional output checks consist of short serial/concurrent prefixes and twelve known-answer questions. Numerical/path agreement and these checks support the reported implementation evaluation; they are not presented as a general capability benchmark.

## Evidence integrity

The snapshot contains **357 hashed evidence files**, **125 phase records**, **49 source experiment directories** and **34 telemetry archives**. Every record remains available in the preserved archive. The manuscript's [claim map](CLAIMS.md) identifies the specific completed measurements that support its contributions.

The import process scrubs device/network identities and local home paths, normalizes nonfinite JSON numbers to `null`, and retains original/stored hashes. `null` is not interpreted as a measured zero. `make data` and `make verify` validate the frozen snapshot and regenerate the current result tables.
