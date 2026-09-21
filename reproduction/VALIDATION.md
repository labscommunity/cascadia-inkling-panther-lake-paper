# Artifact validation record

Initial draft validation: **2026-09-21**, macOS, Python **3.14.4**, uv **0.11.12**, Matplotlib **3.10.8**, Tectonic **0.16.9**. The analysis/verification scripts use the Python standard library and target Python 3.10+; that compatibility range has not been tested as a version matrix.

Completed checks:

- Reconstructed all tables and five PDF/PNG figure pairs from the frozen evidence.
- Verified all **357** imported hashes and byte sizes.
- Recomputed all **125** phase aggregate rates; every result agrees within three-decimal storage rounding. Retained all **five** incomplete/failed records.
- Matched the **21,549-token** server-counter delta independently to the long-phase client total.
- Checked derived head-batching, dense-mapping and MTP comparisons, plus post-swap installed-box/role identity.
- Resolved all **31 manuscript citations** within the **33-entry literature ledger** and validated current report-document links.
- Validated strict JSON and scanned text/compressed archives for known private-address, host-path, MAC and credential patterns. This is a specified pattern check, not a claim of a universal security audit.
- Built the **17-page PDF** successfully with resolved references, no overfull boxes, and visually inspected the title, hardware/architecture page and principal charts. Tectonic's harmless `inputenc` warning reflects its UTF-8 engine.
- Validated `CITATION.cff` against schema 1.2.0 using **cffconvert 2.0.0**.

These checks validate the research artifact and its internal consistency. They do not rerun historical integration tests, evaluate model quality, establish causal attribution, reproduce offline neural scoring without its tensor assets, or run new inference on the fleet.
