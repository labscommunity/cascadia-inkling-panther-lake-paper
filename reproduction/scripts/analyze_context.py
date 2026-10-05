#!/usr/bin/env python3
"""Rebuild the context-length results from the frozen evidence (experiments 034 and 047). No fleet access."""
import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPS = ROOT / 'reproduction/evidence/source/autolab/experiments'
OUT = ROOT / 'reproduction/results'
GENERATED = ROOT / 'generated'
FLOPS_PER_KEY = 64 * 128 * 2 * 2      # 64 query heads x 128 dims, a multiply-add for the score and one for the value


def csv_write(name, rows, fields):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def fit_linear_quadratic(points):
    """Least squares T = a N + b N^2 through the origin (2x2 normal equations)."""
    s11 = sum(n * n for n, _ in points); s12 = sum(n ** 3 for n, _ in points); s22 = sum(n ** 4 for n, _ in points)
    r1 = sum(n * t for n, t in points); r2 = sum(n * n * t for n, t in points)
    det = s11 * s22 - s12 * s12
    return (r1 * s22 - r2 * s12) / det, (s11 * r2 - s12 * r1) / det


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    stress = json.loads((EXPS / '047_context_stress/context_stress.json').read_text())
    requests = [r for r in stress['results'] if not r.get('skipped') and not r.get('in_flight')]
    ok = [r for r in requests if not r.get('error')]
    failed = [r for r in requests if r.get('error')]
    by = {}
    for r in ok:
        by.setdefault((r['streams'], r['size']), []).append(r)
    rows = []
    for (streams, size), rs in sorted(by.items()):
        cores = [b['cpu_mean'] * 16 for r in rs for b in r.get('boxes', {}).values() if b.get('cpu_mean') is not None]
        gpu = [b['gpu_mean'] * 100 for r in rs for b in r.get('boxes', {}).values() if b.get('gpu_mean') is not None]
        watts = [b['pkg_w_mean'] for r in rs for b in r.get('boxes', {}).values() if b.get('pkg_w_mean') is not None]
        free = [b['mem_avail_min_mb'] for r in rs for b in r.get('boxes', {}).values() if b.get('mem_avail_min_mb') is not None]
        rows.append(dict(streams=streams, size=size, repeats=len(rs),
                         prompt_tokens=round(statistics.mean(r['prompt_tokens'] for r in rs)),
                         ttft_s=round(statistics.mean(r['ttft_s'] for r in rs), 2),
                         ttft_sd=round(statistics.pstdev(r['ttft_s'] for r in rs), 2),
                         prefill_tok_s=round(statistics.mean(r['prefill_tok_s'] for r in rs), 2),
                         decode_tok_s=round(statistics.mean(r['decode_tok_s'] for r in rs), 3),
                         decode_min=min(r['decode_tok_s'] for r in rs), decode_max=max(r['decode_tok_s'] for r in rs),
                         output_tokens=round(statistics.mean(r['tokens'] for r in rs), 1),
                         needle_found=sum(1 for r in rs if r['needle_found']),
                         cores_busy=round(statistics.mean(cores), 2) if cores else None,
                         gpu_busy_pct=round(statistics.mean(gpu), 1) if gpu else None,
                         package_w=round(statistics.mean(watts), 1) if watts else None,
                         min_free_gib=round(min(free) / 1024, 2) if free else None))
    csv_write('context.csv', rows, list(rows[0].keys()))
    single = [r for r in rows if r['streams'] == 1]
    a, b = fit_linear_quadratic([(r['prompt_tokens'], r['ttft_s']) for r in single])
    quadratic_gflops = FLOPS_PER_KEY / 2 / b / 1e9     # per box: the N^2/2 key visits of one prompt, in the fitted time
    probe_rows = json.loads((EXPS / '034_context_scan/probe_cx.json').read_text())
    probe = []
    for size in sorted({int(r['ctx']) for r in probe_rows}):
        rs = [r for r in probe_rows if int(r['ctx']) == size]
        fits = [r for r in rs if int(r.get('fits', 0))]
        probe.append(dict(context=size, boxes_reporting=len(rs), boxes_fit=len(fits),
                          need_mb=int(rs[0]['need_mb']) if rs and 'need_mb' in rs[0] else None,
                          avail_mb_min=min(int(r['avail_mb']) for r in rs), avail_mb_max=max(int(r['avail_mb']) for r in rs),
                          decode_ms_median=statistics.median(int(r['decode_ms']) for r in fits) if fits else None,
                          decode_ms_min=min(int(r['decode_ms']) for r in fits) if fits else None,
                          decode_ms_max=max(int(r['decode_ms']) for r in fits) if fits else None,
                          attn_ms_median=statistics.median(int(r['attn_ms']) for r in fits) if fits else None))
    csv_write('context_probe.csv', probe, list(probe[0].keys()))
    # slope of the per-box attention cost, ms per 1k positions, over the sizes every box fits
    full = [p for p in probe if p['boxes_fit'] == p['boxes_reporting'] and p['attn_ms_median'] is not None]
    xs = [p['context'] for p in full]; ys = [p['attn_ms_median'] for p in full]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    attn_gflops_64k = FLOPS_PER_KEY * 65536 / (next(p['attn_ms_median'] for p in probe if p['context'] == 65536) / 1000) / 1e9
    one_m = next(p for p in probe if p['context'] == 1048576)
    n64 = next(r for r in single if r['size'] == 65536)
    n1 = next(r for r in single if r['size'] == 1024)
    n32 = next(r for r in single if r['size'] == 32768)
    def hours(n):
        return (a * n + b * n * n) / 3600
    tex = ['% Generated from the frozen evidence by reproduction/scripts/analyze_context.py.']
    values = {
        'CtxSizes': str(len(single)), 'CtxRequests': str(len(ok)), 'CtxNeedle': str(sum(r['needle_found'] for r in single)),
        'CtxFirstTokenOneK': f'{n1["ttft_s"]:.0f}', 'CtxDecodeOneK': f'{n1["decode_tok_s"]:.2f}',
        'CtxFirstTokenThirtyTwoK': f'{n32["ttft_s"]/60:.0f}', 'CtxDecodeThirtyTwoK': f'{n32["decode_tok_s"]:.2f}',
        'CtxFirstTokenSixtyFourKMin': f'{n64["ttft_s"]/60:.0f}', 'CtxDecodeSixtyFourK': f'{n64["decode_tok_s"]:.2f}',
        'CtxPrefillRateSmall': f'{max(r["prefill_tok_s"] for r in single):.0f}', 'CtxPrefillRateSixtyFourK': f'{n64["prefill_tok_s"]:.1f}',
        'CtxLinearRate': f'{1/a:.0f}', 'CtxQuadraticCoeff': f'{b*1e6:.2f}', 'CtxQuadraticGflops': f'{quadratic_gflops:.0f}',
        'CtxPredictHoursOneTwoEightK': f'{hours(131072):.1f}', 'CtxPredictHoursTwoFiveSixK': f'{hours(262144):.0f}',
        'CtxPredictHoursOneM': f'{hours(1048576):.0f}',
        'CtxCoresBusy': f'{statistics.mean(r["cores_busy"] for r in single):.2f}',
        'CtxGpuBusyOneK': f'{n1["gpu_busy_pct"]:.0f}', 'CtxGpuBusySixtyFourK': f'{n64["gpu_busy_pct"]:.0f}',
        'CtxFreeOneK': f'{n1["min_free_gib"]:.2f}', 'CtxFreeSixtyFourK': f'{n64["min_free_gib"]:.2f}',
        'ProbeAttnSlope': f'{slope*1000:.1f}', 'ProbeDecodeFourK': str(next(p['decode_ms_median'] for p in probe if p['context'] == 4096)),
        'ProbeDecodeSixtyFourK': str(next(p['decode_ms_median'] for p in probe if p['context'] == 65536)),
        'ProbeAttnSixtyFourK': str(next(p['attn_ms_median'] for p in probe if p['context'] == 65536)),
        'ProbeDecodeFiveTwelveK': str(next(p['decode_ms_median'] for p in probe if p['context'] == 524288)),
        'ProbeDecodeOneM': str(one_m['decode_ms_median']), 'ProbeOneMNeedGB': f'{one_m["need_mb"]/1024:.1f}',
        'ProbeOneMFit': str(one_m['boxes_fit']), 'ProbeOneMAvailMin': f'{one_m["avail_mb_min"]/1024:.1f}', 'ProbeOneMAvailMax': f'{one_m["avail_mb_max"]/1024:.1f}',
        'ProbeAttnGflopsSixtyFourK': f'{attn_gflops_64k:.0f}',
        'CtxFailedSize': str(failed[0]['size']) if failed else '0',
    }
    for key, value in values.items():
        tex.append('\\newcommand{\\' + key + '}{' + value + '}')
    lines = []
    for r in single:
        lines.append('%s & %d & %s & %.1f & %.2f (%.2f--%.2f) & %d/%d & %.2f & %.0f\\%% & %.2f\\\\' % (
            f'{r["prompt_tokens"]:,}', r['repeats'], (f'{r["ttft_s"]:.0f}\\,s' if r['ttft_s'] < 100 else f'{r["ttft_s"]/60:.1f}\\,min'),
            r['prefill_tok_s'], r['decode_tok_s'], r['decode_min'], r['decode_max'], r['needle_found'], r['repeats'],
            r['cores_busy'], r['gpu_busy_pct'], r['min_free_gib']))
    tex.append('\\newcommand{\\ContextRows}{' + '\n'.join(lines) + '}')
    plines = []
    for p in probe:
        ctx = f'{p["context"]//1024}k' if p['context'] < 1048576 else '1M'
        if p['boxes_fit']:
            plines.append('%s & %d/%d & %s & %s & %s\\\\' % (ctx, p['boxes_fit'], p['boxes_reporting'], p['decode_ms_median'],
                                                             f'{p["decode_ms_min"]}--{p["decode_ms_max"]}' if p['boxes_fit'] > 1 else '--', p['attn_ms_median']))
        else:
            plines.append('%s & 0/%d & \\multicolumn{3}{l}{does not fit: %.1f\\,GB needed, %.1f--%.1f free}\\\\' % (
                ctx, p['boxes_reporting'], p['need_mb'] / 1024, p['avail_mb_min'] / 1024, p['avail_mb_max'] / 1024))
    tex.append('\\newcommand{\\ProbeRows}{' + '\n'.join(plines) + '}')
    (GENERATED / 'context.tex').write_text('\n'.join(tex) + '\n')
    print(json.dumps(dict(sizes=len(single), requests=len(ok), failed=[(f['size'], f['error']) for f in failed],
                          linear_tok_s=round(1 / a, 1), quadratic_s_per_token2=b, quadratic_gflops=round(quadratic_gflops, 1),
                          probe_attn_ms_per_1k=round(slope * 1000, 2), predicted_hours={'128k': round(hours(131072), 1), '256k': round(hours(262144), 1), '1M': round(hours(1048576))}), indent=2))


if __name__ == '__main__':
    main()
