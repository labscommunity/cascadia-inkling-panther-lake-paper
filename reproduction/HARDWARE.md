# Hardware and capability ledger

## Installed machines

Primary source: [011b telemetry](evidence/telemetry/011b_long_generation.jsonl.gz); reconstruction: [hardware.json](results/hardware.json).

| Property | Installed boxes 0–7 | Installed boxes 8–10 |
|---|---|---|
| CPU string | Intel Core Ultra X7 358H | Same |
| Logical CPUs | 16 | 16 |
| Nominal installed memory | 64 GB (operator description) | 64 GB (operator description) |
| OS-reported memory | 62,757 MiB = 61.286 GiB | 62,615 MiB = 61.147 GiB |
| Kernel | 7.0.0-31-generic | Same |
| Governor / EPP / profile | powersave / performance / performance | Same |
| Interface | USB NCM; original MAC-derived name removed | PCIe-style `enp86s0` / `enp87s0` |
| Reported link rate | 1000 Mb/s | 1000 Mb/s |
| Platform PL1 / PL2 fields | 25 / 31 W | 0 / 148 W |
| Package PL1 / PL2 fields | 200 / 70 W | 200 / 80 W |

These PL values are raw domain-specific configuration telemetry, not wall draw, observed turbo power or a complete interpretation of firmware limits. In particular, a zero field does not prove zero power use. The apparent tension between governor name and EPP/profile is preserved, not normalized away.

Logical roles initially match installed-box indices. Experiment 032 exchanges roles 0 and 8; the original entry box retains the tunnel/relay. Performance profiles use logical roles; hardware diagnosis uses installed-box identity.

## Vendor-described capability

The [Intel SKU specification](https://www.intel.com/content/www/us/en/products/sku/245527/intel-core-ultra-x7-processor-358h-18m-cache-up-to-4-80-ghz/specifications.html) and [Intel Series 3 architecture white paper](https://builders.intel.com/docs/networkbuilders/industrial-and-robotics-innovation-with-intel-core-ultra-processors-series-3-1767869217.pdf), accessed 2026-09-21, establish:

| SKU/family capability | Relevance to the study |
|---|---|
| 4 performance + 8 efficient + 4 low-power efficient cores; 16 threads | CPU executes routing, attention state and host logic alongside iGPU work. Logical-CPU count is also confirmed by telemetry. |
| Up to 4.8 GHz; 18 MB cache | Specifications, not a claim that fleet cores sustain this clock. |
| Arc B390, 12 Xe cores, Xe3 graphics | Accelerator family used for compressed projections and fused experts. Full device/driver IDs are not archived for every box. |
| Up to 122 INT8 GPU TOPS; 50 INT8 NPU TOPS | Arithmetic capability ratings do not predict this memory-sensitive pipeline. NPU is unused. |
| Up to 96 GB, LPDDR5X up to 9600 MT/s | SKU maxima; fleet has nominal 64 GB and no retained per-box DRAM timing inventory. |
| Processor base power 25 W; maximum turbo power 80 W | Vendor CPU specification; distinct from platform/package configuration fields and wall power. |

A separate reference host in the [bandwidth notes](evidence/source/autolab/PHYSICS.md) reports 8533 MT/s. Multiplying 8533 MT/s by a 128-bit interface gives about 136.5 GB/s nominal transfer capacity. Neither fleet-wide memory speed nor sustained bandwidth was measured by that multiplication. The report's bandwidth arguments are conditional on explicitly stated assumptions.

## Capability actually exercised

The fleet serves the text-only decoder across eleven layer shards. Its CPU/iGPU memory capacity supports compressed expert residency; it is not eleven replicas or a single coherent 704 GB address space. The fixed chain transfers FP32 residuals over Ethernet and returns sampled token IDs.

The deployment defaults to 1024 sequence positions. Retained prompts/generation phases exercise relatively short contexts. Public Inkling support for multimodal input or long context does not demonstrate those capabilities in this export. The data does not establish NPU acceleration, million-token context, multimodal inference, wall-energy efficiency, purchase cost or long-run hardware reliability.

Missing items for a complete hardware reproduction manifest: exact system/motherboard variants, firmware revisions, graphics driver/Level Zero versions, per-device memory timing, cooling/ambient conditions and independently measured wall power. Preserve privacy by using stable anonymous box IDs when these are collected.
