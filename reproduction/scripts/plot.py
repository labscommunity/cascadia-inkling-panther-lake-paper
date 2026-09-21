#!/usr/bin/env python3
"""Generate publication figures from the checked result tables (matplotlib 3.10.8)."""
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
    evolution = read('evolution.csv')
    fig, ax = plt.subplots(figsize=(6.6, 2.6))
    x = list(range(len(evolution)))
    ax.bar([v-.18 for v in x], [float(r['phase_tok_s']) for r in evolution], .36, color=BLUE, label='Whole-phase throughput')
    ax.bar([v+.18 for v in x], [float(r['sum_rates']) for r in evolution], .36, color=ORANGE, label='Sum of per-stream decode rates')
    ax.set_xticks(x, ['005\nCPU experts*', '007\nPartial iGPU', '008b\nAll MoE iGPU', '009\nDense iGPU', '011\nParallel attention'])
    ax.set_ylabel('Generated tokens/s'); ax.set_ylim(0, 79)
    ax.legend(loc='upper left', fontsize=8, frameon=False)
    ax.grid(axis='y', alpha=.2)
    fig.text(.13, -.04, '176 streams; output caps: *48 tokens, others 32. Sequential configurations, not isolated ablations.', fontsize=8)
    save(fig, 'throughput')

    data = read('prefill.csv')
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.7))
    cats = ['019_baseline_15_streams', '024_prefill_windows', '027_rank0_dense_as_moe', '035_chain_readiness']
    names = ['019\nBaseline', '024\n8-row windows', '027\nDense slices', '035\nReadiness']
    for ax, field, ylabel in [(axes[0], 'ttft_median_s', 'Median TTFT (seconds)'), (axes[1], 'phase_tok_s', 'Whole-phase tokens/s')]:
        for i, exp in enumerate(cats):
            vals = [float(r[field]) for r in data if r['experiment'] == exp]
            ax.scatter([i + .06*(j-(len(vals)-1)/2) for j in range(len(vals))], vals, color=BLUE, zorder=3, s=28)
        ax.set_xticks(range(4), names, fontsize=8); ax.set_ylabel(ylabel); ax.set_ylim(bottom=0); ax.grid(axis='y', alpha=.2)
    fig.tight_layout()
    save(fig, 'prefill')

    counter = read('server_counter_011b.csv')
    counter_audit = json.loads((DATA / 'server_counter_audit.json').read_text())
    fig, ax = plt.subplots(figsize=(6.6, 2.5))
    ax.step([float(r['end_s']) for r in counter], [float(r['rate']) for r in counter], where='pre', color=BLUE, label='Server counter, disjoint ~10 s blocks')
    rate = counter_audit['phase_throughput']
    ax.axhline(rate, color=GRAY, linestyle='--', label=f'Client whole phase: {rate:.2f} tok/s')
    ax.set_xlabel('Seconds from client phase start'); ax.set_ylabel('Generated tokens/s'); ax.set_ylim(bottom=0)
    ax.legend(frameon=False, fontsize=8, loc='lower center'); ax.grid(alpha=.2)
    save(fig, 'counter')

    mtp = read('mtp_families.csv')
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    x = list(range(len(mtp)))
    ax.bar([v-.18 for v in x], [100*float(r['original_a1']) for r in mtp], .36, color=BLUE, label='Original MTP/head on fleet states')
    ax.bar([v+.18 for v in x], [100*float(r['quantized_a1']) for r in mtp], .36, color=ORANGE, label='Proposed quantization + 65k vocabulary')
    ax.axhline(70, color=GRAY, linestyle='--', linewidth=1, label='Study qualification threshold')
    ax.set_xticks(x, [r['family'] for r in mtp], rotation=30, ha='right', fontsize=8)
    ax.set_ylim(0, 103); ax.set_ylabel('First-draft agreement (%)'); ax.grid(axis='y', alpha=.2)
    ax.legend(frameon=False, fontsize=7, loc='upper left', ncol=1)
    save(fig, 'mtp')

    profiles = read('profiles.csv')
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.6), sharey=True)
    for ax, exp, title in [(axes[0], '027_rank0_dense_as_moe', '027: separate head calls'), (axes[1], '028_head_batching', '028: shared head calls')]:
        rows = [r for r in profiles if r['experiment'] == exp and r['source']=='phases.json' and r['phase']=='mix15a']
        x = [int(r['role']) for r in rows]
        core = [float(r['compute_ms']) for r in rows]
        ax.bar(x, core, color=BLUE, label='Layer computation')
        ax.bar(x, [float(r['head_ms']) for r in rows], bottom=core, color=ORANGE, label='Output head')
        ax.set_xticks(range(11)); ax.set_xlabel('Pipeline role'); ax.set_title(title, fontsize=9); ax.grid(axis='y', alpha=.2)
    axes[0].set_ylim(0, 61)
    axes[0].set_ylabel('Mean ms/frame (decode windows)'); axes[0].legend(frameon=False, fontsize=7, loc='upper left')
    fig.tight_layout(); save(fig, 'head_batching')
    print('Generated five PDF/PNG figure pairs.')


if __name__ == '__main__':
    main()
