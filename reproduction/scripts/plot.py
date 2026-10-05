#!/usr/bin/env python3
"""Generate contribution-focused figures from the frozen result tables."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'reproduction/results'
FIG = ROOT / 'figures'
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                     'pdf.fonttype': 42, 'ps.fonttype': 42, 'axes.axisbelow': True})
BLUE, ORANGE, GRAY = '#275d8c', '#bd652b', '#7c8791'


def read(name):
    return list(csv.DictReader((DATA / name).open()))


def save(fig, name):
    fig.savefig(FIG / (name + '.pdf'), bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(FIG / (name + '.png'), dpi=180, bbox_inches='tight')
    plt.close(fig)


def main():
    FIG.mkdir(exist_ok=True)
    curve = read('concurrency.csv')
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.0))
    ns = [int(r['concurrency']) for r in curve]
    mean = [float(r['mean_decode_tok_s']) for r in curve]
    axes[0].plot(ns, mean, 'o-', color=BLUE, markersize=3, label='Shared-interval decode')
    axes[0].fill_between(ns, [float(r['decode_min']) for r in curve],
                         [float(r['decode_max']) for r in curve], color=BLUE, alpha=.18, label='Observed repeat range')
    axes[0].plot(ns, [float(r['mean_phase_tok_s']) for r in curve], 's--', color=ORANGE, markersize=3,
                 label='Including startup and drain')
    axes[0].fill_between(ns, [float(r['phase_min']) for r in curve],
                         [float(r['phase_max']) for r in curve], color=ORANGE, alpha=.12)
    axes[0].set_ylabel('Aggregate tokens/s'); axes[0].set_ylim(0, 83)
    axes[0].legend(frameon=False, fontsize=6.6, loc='upper left')
    axes[1].plot(ns, [float(r['ttft_median_s']) for r in curve], 'o-', color=BLUE, markersize=3, label='Median')
    axes[1].plot(ns, [float(r['ttft_p95_s']) for r in curve], 's--', color=ORANGE, markersize=3, label='p95')
    axes[1].set_ylabel('Time to first token (s)'); axes[1].set_ylim(bottom=0)
    axes[1].legend(frameon=False, fontsize=8, loc='upper left')
    for ax in axes:
        ax.set_xscale('log', base=2); ax.set_xticks([1, 4, 15, 32, 88, 176])
        ax.xaxis.set_major_formatter(ScalarFormatter()); ax.tick_params(axis='x', labelsize=8, rotation=35)
        ax.set_xlabel('Concurrent streams'); ax.grid(alpha=.2)
    fig.tight_layout(); save(fig, 'concurrency')
    dense = read('dense.csv')
    fig, ax = plt.subplots(figsize=(6.3, 2.6))
    x = list(range(len(dense)))
    ax.bar([v-.18 for v in x], [float(r['matrix_ms']) for r in dense], .36, color=BLUE, label='Three compressed matrix calls')
    ax.bar([v+.18 for v in x], [float(r['fused_ms']) for r in dense], .36, color=ORANGE, label='Eight all-active fused slices')
    ax.set_xticks(x, [f"Layer {r['layer']}\n{r['rows']} row{'s' if r['rows'] != '1' else ''}" for r in dense])
    ax.set_ylabel('Dense-layer call time (ms)'); ax.set_ylim(0, 11.5)
    ax.legend(frameon=False, fontsize=8, loc='upper left'); ax.grid(axis='y', alpha=.2)
    fig.tight_layout(); save(fig, 'dense')

    data = read('prefill.csv')
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.6))
    cats = ['019_baseline_15_streams', '024_prefill_windows']
    names = ['Reference\nadmission', 'Eight-row\nprefill windows']
    for ax, field, ylabel in [(axes[0], 'ttft_median_s', 'Median TTFT (seconds)'), (axes[1], 'phase_tok_s', 'Whole-phase tokens/s')]:
        for i, exp in enumerate(cats):
            vals = [float(r[field]) for r in data if r['experiment'] == exp]
            ax.scatter([i + .045*(j-(len(vals)-1)/2) for j in range(len(vals))], vals, color=BLUE, zorder=3, s=32)
        ax.set_xticks(range(2), names, fontsize=9); ax.set_ylabel(ylabel)
        ax.set_xlim(-.4, 1.4); ax.set_ylim(bottom=0); ax.grid(axis='y', alpha=.2)
    fig.tight_layout(); save(fig, 'prefill')

    mtp = read('mtp_families.csv')
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    x = list(range(len(mtp)))
    ax.bar([v-.18 for v in x], [100*float(r['original_a1']) for r in mtp], .36, color=BLUE, label='Original weights, full vocabulary')
    ax.bar([v+.18 for v in x], [100*float(r['quantized_a1']) for r in mtp], .36, color=ORANGE, label='INT4/INT8 weight grids, 65k vocabulary')
    ax.set_xticks(x, [r['family'] for r in mtp], rotation=30, ha='right', fontsize=8)
    ax.set_ylim(0, 100); ax.set_ylabel('First-draft agreement (%)'); ax.grid(axis='y', alpha=.2)
    ax.legend(frameon=False, fontsize=8, loc='upper left')
    save(fig, 'mtp')

    # Supporting counter audit, available with the artifact's measurement tables.
    counter = read('server_counter_011b.csv')
    counter_audit = json.loads((DATA / 'server_counter_audit.json').read_text())
    fig, ax = plt.subplots(figsize=(6.6, 2.5))
    ax.step([float(r['end_s']) for r in counter], [float(r['rate']) for r in counter], where='pre', color=BLUE,
            label='Server counter, disjoint ~10 s blocks')
    rate = counter_audit['phase_throughput']
    ax.axhline(rate, color=GRAY, linestyle='--', label=f'Client whole phase: {rate:.2f} tok/s')
    ax.set_xlabel('Seconds from client phase start'); ax.set_ylabel('Generated tokens/s'); ax.set_ylim(bottom=0)
    ax.legend(frameon=False, fontsize=8, loc='lower center'); ax.grid(alpha=.2)
    save(fig, 'counter')
    context = read('context.csv')
    probe = read('context_probe.csv')
    single = [r for r in context if r['streams'] == '1']
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.0))
    ns = [int(r['prompt_tokens']) for r in single]
    ttft = [float(r['ttft_s']) for r in single]
    axes[0].errorbar(ns, ttft, yerr=[float(r['ttft_sd']) for r in single], fmt='o-', color=BLUE, markersize=3, label='Time to first token')
    # the fitted a N + b N^2 (recomputed here from the same rows, so the figure and the text agree)
    s11 = sum(n * n for n in ns); s12 = sum(n ** 3 for n in ns); s22 = sum(n ** 4 for n in ns)
    r1 = sum(n * t for n, t in zip(ns, ttft)); r2 = sum(n * n * t for n, t in zip(ns, ttft))
    det = s11 * s22 - s12 * s12; a = (r1 * s22 - r2 * s12) / det; b = (s11 * r2 - s12 * r1) / det
    grid = [2 ** k for k in range(10, 19)]
    axes[0].plot(grid, [a * n + b * n * n for n in grid], '--', color=GRAY, label='Fit $aN+bN^2$')
    axes[0].plot(grid, [a * n for n in grid], ':', color=GRAY, label='Linear part only')
    axes[0].set_yscale('log'); axes[0].set_ylabel('Time to first token (s)')
    axes[0].legend(frameon=False, fontsize=6.6, loc='upper left')
    fit = [r for r in probe if r['decode_ms_median']]
    px = [int(r['context']) for r in fit]
    axes[1].plot(px, [float(r['decode_ms_median']) for r in fit], 'o-', color=BLUE, markersize=3, label='One token, per machine (median of 11)')
    axes[1].plot(px, [float(r['attn_ms_median']) for r in fit], 's--', color=ORANGE, markersize=3, label='Of which CPU attention')
    axes[1].plot(ns, [1000 / float(r['decode_tok_s']) / 11 for r in single], '^:', color=GRAY, markersize=3,
                 label='Measured decode, per machine share')
    axes[1].set_yscale('log'); axes[1].set_ylabel('Milliseconds per token')
    axes[1].legend(frameon=False, fontsize=6.6, loc='upper left')
    for ax in axes:
        ax.set_xscale('log', base=2); ax.set_xticks([1024, 4096, 16384, 65536, 262144, 1048576])
        ax.set_xticklabels(['1k', '4k', '16k', '64k', '256k', '1M']); ax.tick_params(axis='x', labelsize=8)
        ax.set_xlabel('Context (tokens)'); ax.grid(alpha=.2, which='both')
    fig.tight_layout(); save(fig, 'context')
    print('Generated five paper charts and one supporting counter chart, each as PDF/PNG.')


if __name__ == '__main__':
    main()
