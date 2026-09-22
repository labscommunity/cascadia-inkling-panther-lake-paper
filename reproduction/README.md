# Reconstructing the paper's measurements

The artifact freezes Cascadia source commit **3189a189fe3428f5a6315a7eb67b13148ec314e2** and retained operator telemetry through **2026-09-21**. Its scripts reconstruct the paper's tables and figures offline from the included evidence.

## Build

From the repository root, with Python 3.10 or later:

```sh
make data
make figures
make
make verify
```

`make data` and `make verify` use the Python standard library. `make figures` uses uv with Matplotlib 3.10.8. `make` uses Tectonic, or pdfLaTeX and BibTeX. First use of uv or Tectonic can download their dependencies. The checked-in PDF and figures are directly readable.

These commands reconstruct measurements rather than execute inference. The supported entry points are the new scripts under `reproduction/scripts/`; archived operator and benchmark code supplies provenance.

## Contribution-oriented results

| Paper contribution | Reconstructed material |
|---|---|
| Custom resident engine and dense/sparse operator unification | `results/hardware.json`, `results/dense.csv`, relevant `results/profiles.csv` rows, `figures/dense.pdf` |
| Streaming service across resident shards | `results/concurrency.csv`, `results/survey_phases.csv`, `results/prefill.csv`, `figures/concurrency.pdf`, `figures/prefill.pdf` |
| Draft evaluation on deployed states | `results/mtp_families.csv`, `results/derived.json`, `figures/mtp.pdf` |
| Independent token-accounting check | `results/survey_audit.json`; historical `results/server_counter_audit.json` and supporting `figures/counter.pdf` |

Figure paths are relative to the repository root. Each chart is generated as both PDF and PNG. [CLAIMS.md](CLAIMS.md) maps every reported number and mechanism to its source; [AUDIT.md](AUDIT.md) records metric interpretation.

## Frozen inputs

| Path | Contents |
|---|---|
| `evidence/manifest.json` | Original/stored SHA-256, byte sizes, source paths and transformations for 421 evidence files |
| `evidence/source/autolab/` | Recorded measurements, configuration files, research summaries, harness and scoring code |
| `evidence/source/tools/`, `evidence/source/crates/` | Four pinned exporter, gate, layer-runtime and C++ bridge files supporting the engine description |
| `evidence/source/docs/` | Inkling architecture and execution context |
| `evidence/source/deploy/` | Scrubbed fleet defaults |
| `evidence/telemetry/` | 35 deterministic fleet telemetry gzip JSONL archives |
| `evidence/requests/046_final_performance/` | 35 phase token-event archives and one API-statistics archive |
| `results/phases.csv` | Reconstruction of 125 historical phase records |
| `results/survey_phases.csv` | 35 finalized-survey records: 33 measured phases and two pilots |
| `results/concurrency.csv` | Fifteen paired mixed-workload concurrency points |

Git evidence comes from the pinned commit. Telemetry comes from the corresponding retained experiment directories. The preserved archive provides the detailed provenance behind the contribution-based presentation.

Private IPs, observed host names, MAC-derived interface names, serial/host identity fields and local home paths are scrubbed. Installed-box integers and logical pipeline roles remain available for analysis. Nonfinite JSON numbers are normalized to `null`, which is kept distinct from a measured zero. Compression uses a fixed gzip timestamp. Original and stored hashes identify each transformation.

`import_evidence.py` is the provenance utility. It requires an explicitly supplied original checkout, immutable ref and telemetry directory; normal reconstruction uses the already frozen inputs.

## Reconstruction rules

Whole-phase throughput is recomputed from actual token counts and unrounded start/end timestamps. `analyze_survey.py` reconstructs common decode intervals from raw token events and validates every request against final API usage. It checks all 35 survey records, including two pilots: 1,605 requests and 204,192 token events. The paper uses thirty paired mixed-workload phases for the concurrency curve and records the three completed explanation-family phases separately.

The paired curve averages phase rates and pools request TTFT quantiles. Capture state, prompt repetition and active phrase learning are recorded in [AUDIT.md](AUDIT.md). Historical sums of individual request decode rates remain a separate statistic in `phases.csv`; they are not substituted for common-interval throughput. The historical long-generation counter independently matches 21,549 client tokens.

Profiles are deduplicated per installed box and aligned using receipt age on the operator clock. Phase windows use the historical harness's timing tolerance and select windows with no opens. Reported stage timings are weighted by frame count; role identity is distinct from physical device identity.

Dense-call tables are parsed from the retained layer load checks. Draft tables use the retained fleet rescore and family summaries. Capture validation and scoring scripts accompany those records; the reconstructed report labels the draft results as offline agreement.
