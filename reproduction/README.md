# Reconstructing the measurements

The artifact freezes source commit **d1ab1abd7387b7f0b83d6d56b7aec2e1a56f9651** from `labscommunity/cascadia` and locally retained operator telemetry, through **2026-09-21**. It supports offline reconstruction of the report. It does not contain the model weights, full binary tensor captures or every system manifest needed to rerun inference.

## Layout

| Path | Contents |
|---|---|
| `evidence/manifest.json` | 357 evidence entries, original and scrubbed SHA-256, byte sizes, source paths, transformations and exclusions |
| `evidence/source/autolab/` | Frozen experiment JSON, hypotheses, verdicts, research scripts/tables, journal and harness |
| `evidence/source/docs/` | Relevant Inkling architecture/performance notes |
| `evidence/source/deploy/` | Scrubbed fleet configuration context |
| `evidence/telemetry/` | 34 scrubbed, deterministic gzip JSONL archives |
| `results/` | Regenerated CSV and strict JSON tables, inventory and audits |
| `scripts/analyze.py` | Standard-library reconstruction; verifies every imported hash first |
| `scripts/plot.py` | Five exportable PDF/PNG figures using pinned Matplotlib |
| `scripts/verify.py` | Independent consistency and artifact checks |

## Commands

From the repository root, with Python 3.10 or later:

```sh
make data
make verify
make figures
make
```

The first two commands need no model, fleet, GPU or network. Figures use `uv` to resolve Matplotlib 3.10.8. Paper compilation uses Tectonic when available, otherwise pdfLaTeX and BibTeX; a first Tectonic build may fetch TeX packages. Checked-in figures and `generated/numbers.tex` permit PDF compilation without rebuilding plots. `make clean` removes TeX intermediates, not the paper or source evidence.

Do not execute archived deployment/benchmark scripts to reproduce the tables. They are retained as historical evidence and some contain publishing or fleet-access routines. The supported reconstruction entry points are only the new scripts in this directory.

## Provenance and transformations

Git evidence is read from the pinned commit, not a moving working tree. Telemetry was copied from the operator's retained experiment directories. Private IPs, observed device names, MAC addresses, MAC-derived interface names, serial/host identity fields and local home paths are removed or replaced. Installed-box integers and logical pipeline roles are preserved. Author contact information and public research URLs remain.

Nonfinite JSON numbers are normalized to `null`, so the snapshot is valid strict JSON. This matters for failed gate/numerical records; `null` is not a measured zero. Text verdicts may still describe nonfinite values. Telemetry compression sets a zero gzip timestamp. Each entry records the hash of the original bytes and of the stored transformed bytes; telemetry's original hash refers to uncompressed source JSONL.

The snapshot includes the study-generated experiment 013 corpus. External Dolly collection data, deployment logs, signing material, model weights and binary residual dumps are not included. Archived relative links can refer to files in the original checkout or to excluded assets; current report documentation uses local working links wherever available.

`import_evidence.py` is the provenance utility, not a normal rebuild step. It requires an explicitly supplied original checkout, immutable ref and telemetry directory. Re-importing a different snapshot changes the dataset and should be treated as a new research revision.

## Metric reconstruction

All `phases*.json` files in the 49 experiment directories are enumerated, including baseline and failed-capture files. The result is 125 phase records; five are incomplete/failed. `aggregate_tok_s` is recomputed using unrounded start/end timestamps and actual token counts. Every stored value agrees within 0.00051 tokens/s, allowing three-decimal rounding.

`sum_stream_tok_s` is retained as an observed statistic from the harness. Individual request timing traces were not saved, so it cannot be independently re-derived from phase summaries. It equals a sum of rates over differing request intervals, not a server counter measured over one common decode interval. No confidence intervals are inferred from these summaries.

For experiment 011b, the raw server `tokens_total` difference independently equals 21,549 client-counted tokens. The counter plot uses nonoverlapping blocks of five consecutive nominal two-second polls, starting at the first retained poll. The additional summary selects blocks with at least 170 in-flight requests at both endpoints. It still includes admission/prefill; its median is not a new steady-state benchmark.

For stage timing, the frozen `telemetry_analysis.py` deduplicates repeated profile windows per installed box and corrects timestamps using the operator receipt clock and profile age. A phase profile includes windows within the original harness's tolerance (`start-1` through `end+14`, window start at least `start-3`) with no opens. Timings are weighted by frame count. Role mapping is inferred within each experiment archive; it does not assume installed box equals pipeline role. These are sampled software profiles, not exact per-request traces or DRAM counters.

## Remaining reproduction gaps

The dataset does not include every exported weight checksum, exact graphics driver/firmware revision, fleet memory timing, raw MTP residual tensor, gate reference token trace or per-request streaming trace. MTP summary numbers can be checked and plotted, but rescoring the head requires the omitted assets. Microbenchmark verdicts with no raw timing vector remain journal-level evidence. The [claim map](CLAIMS.md) makes those differences explicit.
