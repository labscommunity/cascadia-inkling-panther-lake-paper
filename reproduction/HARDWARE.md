# Hardware and capability

## Installed fleet

Primary source: [long-generation telemetry](evidence/telemetry/011b_long_generation.jsonl.gz); reconstruction: [hardware.json](results/hardware.json).

| Property | Installed boxes 0–7 | Installed boxes 8–10 |
|---|---|---|
| CPU | Intel Core Ultra X7 358H | Same |
| Logical CPUs | 16 | 16 |
| Nominal memory | 64 GB | 64 GB |
| OS-reported memory | 62,757 MiB = 61.286 GiB | 62,615 MiB = 61.147 GiB |
| Kernel | 7.0.0-31-generic | Same |
| Governor / EPP / profile | powersave / performance / performance | Same |
| Network interface | USB NCM | PCIe-style interface |
| Reported link rate | 1000 Mb/s | 1000 Mb/s |

The eleven machines provide nominal 704 GB capacity distributed across separate address spaces. Each pipeline role owns six consecutive decoder layers. The CPU and integrated GPU share memory within a machine; stage-to-stage communication uses explicit FP32 residual messages over Ethernet.

## Processor capabilities

The [Intel SKU specification](https://www.intel.com/content/www/us/en/products/sku/245527/intel-core-ultra-x7-processor-358h-18m-cache-up-to-4-80-ghz/specifications.html) and [Series 3 architecture white paper](https://builders.intel.com/docs/networkbuilders/industrial-and-robotics-innovation-with-intel-core-ultra-processors-series-3-1767869217.pdf), reviewed 2026-09-21, describe:

| Capability | Application to this work |
|---|---|
| 4 performance  + 8 efficient  + 4 low-power efficient cores; 16 threads | CPU routing, attention/state management and serving coordination |
| Up to 4.8 GHz; 18 MB cache | Vendor-specified CPU capability |
| Arc B390; 12 Xe cores; Xe3 graphics | Compressed projections and fused expert execution |
| GPU up to 122 INT8 TOPS; NPU 50 INT8 TOPS | Accelerator capability ratings;  this deployment uses CPU and iGPU |
| Up to 96 GB memory; LPDDR5X up to 9600 MT/s | SKU capabilities;  installed fleet configuration is nominal 64 GB per machine |

Vendor specifications describe available capabilities. The paper's serving measurements describe the application on the installed fleet.

## Executed model path

Cascadia serves Inkling's text decoder with group 32 INT4 experts, INT8 attention/head weights, FP16 fused arithmetic and FP32 inter-stage residuals. The resident configuration allocates approximately 52 GiB of GPU page budget per machine, with a larger allocation on the final role. Routing and stream-local KV/convolution state are managed by the CPU runtime.

The deployment default is 1024 sequence positions. The evaluated workloads use short prompts with output caps stated in the paper. The architecture description covers this CPU/iGPU text-serving path.
