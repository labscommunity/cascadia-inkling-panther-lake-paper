# Publication framing

## Central claim

Cascadia implements resident 975B MoE inference across eleven integrated-GPU AI PCs. The manuscript develops three contributions: shared-memory execution with dense/sparse operator unification, a streaming service across resident layer shards, and draft evaluation using captured deployed states.

## Manuscript organization

1. Establish the architecture and the hardware resources it uses.
2. Explain compressed residency, operator placement and the measured fused dense implementation.
3. Describe the streaming/runtime mechanisms that coordinate concurrent service.
4. Evaluate demonstrated serving configurations with explicit throughput and latency definitions.
5. Present the capture/replay method and matched-state draft findings.
6. Position each contribution against the closest prior work.

The research narrative is organized by contribution. The claim map carries experiment identifiers and source selectors. Paper figures show the dense operator comparison, windowed-admission results and draft agreement by family.

## Claim discipline

Use measured whole-phase throughput for the complete service result, and distinguish summed per-request decode rates. Label operator measurements separately from fleet performance. Describe configuration contrasts using their actual workloads. Present matched-state draft scores as offline agreement, with the numerical arithmetic stated. Attribute existing algebra, chunked-prefill scheduling and speculative-decoding primitives.

The current repository remains private for author review. Submission and public release can use the manuscript, bibliography, figures and supporting claim map as a coherent package.
