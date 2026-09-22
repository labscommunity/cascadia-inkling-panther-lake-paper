# Reconstructing the paper's measurements

The artifact freezes Cascadia source commit **d1ab1abd7387b7f0b83d6d56b7aec2e1a56f9651** and retained operator telemetry through **2026-09-21**. Its scripts reconstruct the paper's tables and figures offline from the included evidence.

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
| Resident execution and dense/sparse operator unification | `results/hardware.json`, `results/dense.csv`, relevant `results/profiles.csv` rows, `figures/dense.pdf` |
| Streaming service across resident shards | `results/serving.csv`, `results/prefill.csv`, `figures/prefill.pdf` |
| Draft evaluation on deployed states | `results/mtp_families.csv`, `results/derived.json`, `figures/mtp.pdf` |
| Independent token-accounting check | `results/server_counter_audit.json`, `results/server_counter_011b.csv`, supporting `figures/counter.pdf` |

Figure paths are relative to the repository root. Each chart is generated as both PDF and PNG. [CLAIMS.md](CLAIMS.md) maps every reported number and mechanism to its source; [AUDIT.md](AUDIT.md) records metric interpretation.

## Frozen inputs

| Path | Contents |
|---|---|
| `evidence/manifest.json` | Original/stored SHA-256, byte sizes, source paths and transformations for 357 evidence files |
| `evidence/source/autolab/` | Recorded measurements, configuration files, research summaries, harness and scoring code |
| `evidence/source/docs/` | Inkling architecture and execution context |
| `evidence/source/deploy/` | Scrubbed fleet defaults |
| `evidence/telemetry/` | 34 deterministic gzip JSONL archives |
| `results/phases.csv` | Complete reconstruction of 125 phase records |

Git evidence comes from the pinned commit. Telemetry comes from the corresponding retained experiment directories. The preserved archive provides the detailed provenance behind the contribution-based presentation.

Private IPs, observed host names, MAC-derived interface names, serial/host identity fields and local home paths are scrubbed. Installed-box integers and logical pipeline roles remain available for analysis. Nonfinite JSON numbers are normalized to `null`, which is kept distinct from a measured zero. Compression uses a fixed gzip timestamp. Original and stored hashes identify each transformation.

`import_evidence.py` is the provenance utility. It requires an explicitly supplied original checkout, immutable ref and telemetry directory; normal reconstruction uses the already frozen inputs.

## Reconstruction rules

Whole-phase throughput is recomputed from actual token counts and unrounded start/end timestamps. The sum of individual decode rates is a distinct recorded statistic, with the interval definition in the paper. For the long-generation workload, the independent server counter matches all 21,549 client tokens.

Profiles are deduplicated per installed box and aligned using receipt age on the operator clock. Phase windows use the historical harness's timing tolerance and select windows with no opens. Reported stage timings are weighted by frame count; role identity is distinct from physical device identity.

Dense-call tables are parsed from the retained layer load checks. Draft tables use the retained fleet rescore and family summaries. Capture validation and scoring scripts accompany those records; the reconstructed report labels the draft results as offline agreement.
