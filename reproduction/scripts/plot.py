#!/usr/bin/env python3
"""Generate contribution-focused figures from the frozen result tables."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    print('Generated three paper charts and one supporting counter chart, each as PDF/PNG.')


if __name__ == '__main__':
    main()
