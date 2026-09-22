#!/usr/bin/env python3
"""Rebuild paper data from the frozen evidence, without models or fleet access."""
import collections
import csv
import gzip
import hashlib
import importlib.util
import json
import re
import statistics
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'reproduction/evidence'
SOURCE = EVIDENCE / 'source'
EXPS = SOURCE / 'autolab/experiments'
OUT = ROOT / 'reproduction/results'
GENERATED = ROOT / 'generated'


def load(path):
    return json.loads(path.read_text())


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def csv_write(name, rows, fields=None):
    fields = fields or list(rows[0])
    with (OUT / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def phases(exp, filename='phases.json'):
    return load(EXPS / exp / filename)


def one(exp, phase, filename='phases.json'):
    return next(p for p in phases(exp, filename) if p['phase'] == phase)


def profiles(records, phase, normalize):
    normalized = normalize(records)
    start, end = phase['start'], phase['end']
    rows = []
    for rank in range(11):
        selected = [r for r in normalized if r.get('rank') == rank and start - 1 <= r['lt'] <= end + 14]
        windows = [p for r in selected for p in r.get('profs', [])
                   if start - 1 <= p['lt'] <= end + 14
                   and p['lt'] - p.get('window_ms', 0) / 1000 >= start - 3
                   and p.get('opens', 0) == 0]
        totals = collections.Counter()
        for p in windows:
            for k, v in p.items():
                if isinstance(v, (int, float)):
                    totals[k] += v
        frames = totals['frames']
        if frames == 0:
            continue
        row = dict(role=rank, installed_box=selected[-1]['box'], windows=len(windows), frames=frames,
                   rows_per_frame=totals['rows'] / frames,
                   compute_ms=totals['compute_ms'] / frames, head_ms=totals['head_ms'] / frames,
                   attention_ms=totals['ov_attn_ms'] / frames, experts_ms=totals['ov_moe_ms'] / frames,
                   fallback_calls=totals['ov_moe_fallbacks'], nonfinite_calls=totals['ov_moe_nonfinite'])
        rows.append(row)
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    GENERATED.mkdir(parents=True, exist_ok=True)
    manifest = load(EVIDENCE / 'manifest.json')
    for entry in manifest['files']:
        actual = hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest()
        assert actual == entry['sha256'], entry['path']

    phase_rows, failed, mismatches, inventory = [], [], [], []
    for experiment in sorted(EXPS.iterdir()):
        if not experiment.is_dir():
            continue
        files = sorted(experiment.glob('phases*.json'))
        count = 0
        for file in files:
            data = load(file)
            if not isinstance(data, list):
                continue
            for phase in data:
                if 'phase' not in phase:
                    continue
                count += 1
                row = dict(experiment=experiment.name, source=file.name, **phase)
                row.pop('sample', None)
                row['valid_completion'] = phase['completed'] == phase['streams'] and not phase['errors']
                elapsed = phase['end'] - phase['start']
                row['recomputed_aggregate_tok_s'] = phase['tokens'] / elapsed
                if abs(row['recomputed_aggregate_tok_s'] - phase['aggregate_tok_s']) > 0.00051:
                    mismatches.append(dict(experiment=experiment.name, source=file.name, phase=phase['phase'],
                                           reported=phase['aggregate_tok_s'], recomputed=row['recomputed_aggregate_tok_s']))
                if not row['valid_completion']:
                    failed.append(dict(experiment=experiment.name, source=file.name, phase=phase['phase'],
                                       completed=phase['completed'], requested=phase['streams'], errors=phase['errors']))
                phase_rows.append(row)
        inventory.append(dict(experiment=experiment.name, phase_rows=count,
                              result_files=';'.join(p.name for p in sorted(experiment.glob('*.json'))),
                              has_verdict=(experiment / 'verdict.md').exists(),
                              telemetry=(EVIDENCE / 'telemetry' / (experiment.name + '.jsonl.gz')).exists()))
    fields = ['experiment', 'source', 'phase', 'streams', 'tokens_req', 'tokens', 'completed', 'start', 'end', 'wall_s',
              'aggregate_tok_s', 'recomputed_aggregate_tok_s', 'sum_stream_tok_s', 'ttft_mean_s', 'ttft_median_s',
              'ttft_max_s', 'stream_tok_s_median', 'stream_tok_s_min', 'valid_completion', 'errors']
    csv_write('phases.csv', phase_rows, fields)
    csv_write('inventory.csv', inventory)

    spec = importlib.util.spec_from_file_location('telemetry_analysis', SOURCE / 'autolab/bench/telemetry_analysis.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    normalized_profiles = []
    telemetry = {}
    for path in sorted((EVIDENCE / 'telemetry').glob('*.jsonl.gz')):
        name = path.name.removesuffix('.jsonl.gz')
        with gzip.open(path, 'rt') as f:
            records = [json.loads(line) for line in f if line.strip()]
        telemetry[name] = records
        for file in sorted((EXPS / name).glob('phases*.json')):
            for phase in load(file):
                if 'phase' not in phase:
                    continue
                for row in profiles(records, phase, module.normalize_records):
                    normalized_profiles.append(dict(experiment=name, source=file.name, phase=phase['phase'], **row))
    csv_write('profiles.csv', normalized_profiles)

    exp = '011b_long_generation'
    long = one(exp, 'long176')
    stats = [r for r in telemetry[exp] if 'stats' in r]
    counter_delta = stats[-1]['stats']['tokens_total'] - stats[0]['stats']['tokens_total']
    assert counter_delta == long['tokens'], (counter_delta, long['tokens'])
    counter_rows = []
    # Fixed disjoint blocks of five nominally 2-second polls, anchored at the first poll.
    # Includes ramp-up; requests-in-flight is not proof that all requests are decoding.
    for i in range(5, len(stats), 5):
        a, b = stats[i - 5], stats[i]
        dt = b['lt'] - a['lt']
        counter_rows.append(dict(start_s=a['lt'] - long['start'], end_s=b['lt'] - long['start'],
                                 interval_s=dt, tokens=b['stats']['tokens_total'] - a['stats']['tokens_total'],
                                 rate=(b['stats']['tokens_total'] - a['stats']['tokens_total']) / dt,
                                 inflight_start=a['stats']['requests_in_flight'], inflight_end=b['stats']['requests_in_flight']))
    csv_write('server_counter_011b.csv', counter_rows)
    selected = [r['rate'] for r in counter_rows if min(r['inflight_start'], r['inflight_end']) >= 170]
    counter = dict(experiment=exp, recorded_client_tokens=long['tokens'], server_counter_delta=counter_delta,
                   phase_seconds=long['end'] - long['start'],
                   phase_throughput=long['tokens'] / (long['end'] - long['start']),
                   sum_stream_rates=long['sum_stream_tok_s'], ttft_mean_s=long['ttft_mean_s'],
                   blocks_at_least_170_inflight=len(selected), median_rate=statistics.median(selected),
                   mean_rate=statistics.mean(selected), max_rate=max(selected),
                   method='Disjoint five-poll blocks; endpoint in-flight >=170; includes admission ramp; descriptive, not independent replicates.')
    save('server_counter_audit.json', counter)

    hardware = {}
    for r in telemetry[exp]:
        if 'static' in r and r['rank'] not in hardware:
            hardware[r['rank']] = dict(installed_box=r['rank'], **r['static'],
                                       mem_total_mib=(r.get('sys') or {}).get('mem_total'))
    save('hardware.json', list(hardware.values()))

    evolution = []
    for exp in ['005_short_steps', '007_fused_f16_all', '008b_all_fused', '009_dense_igpu', '011_parallel_attention']:
        p = one(exp, 's176')
        evolution.append(dict(experiment=exp, streams=p['streams'], output_cap=p['tokens_req'],
                              phase_tok_s=p['aggregate_tok_s'], sum_rates=p['sum_stream_tok_s'], completed=p['completed']))
    csv_write('evolution.csv', evolution)

    prefill = []
    for exp in ['019_baseline_15_streams', '024_prefill_windows', '027_rank0_dense_as_moe', '035_chain_readiness']:
        for p in phases(exp):
            if p['phase'].startswith('mix15'):
                prefill.append(dict(experiment=exp, phase=p['phase'], phase_tok_s=p['aggregate_tok_s'],
                                    sum_rates=p['sum_stream_tok_s'], ttft_median_s=p['ttft_median_s'],
                                    ttft_mean_s=p['ttft_mean_s'], stream_median=p['stream_tok_s_median']))
    csv_write('prefill.csv', prefill)

    serving = []
    for label, experiment, phase_name in [
        ('Long-generation burst', '011b_long_generation', 'long176'),
        ('Windowed burst', '024_prefill_windows', 'mix15a'),
        ('Windowed staggered', '024_prefill_windows', 'stag15'),
        ('Isolated request A', '024_prefill_windows', 'fresh1a'),
        ('Isolated request B', '024_prefill_windows', 'fresh1b'),
    ]:
        p = one(experiment, phase_name)
        serving.append(dict(workload=label, experiment=experiment, phase=phase_name,
                            requests=p['streams'], output_cap=p['tokens_req'], completed=p['completed'],
                            tokens=p['tokens'], phase_tok_s=p['aggregate_tok_s'], sum_rates=p['sum_stream_tok_s'],
                            ttft_median_s=p.get('ttft_median_s'), ttft_mean_s=p['ttft_mean_s']))
    csv_write('serving.csv', serving)

    dense_rows = []
    dense_verdict = (EXPS / '027_rank0_dense_as_moe/verdict.md').read_text()
    pattern = r'^\| layer (\d+) \| ([\d.]+) \| ([\de.-]+) \| ([\d.]+) / ([\d.]+) ms \| ([\d.]+) / ([\d.]+) ms \|'
    for match in re.finditer(pattern, dense_verdict, re.MULTILINE):
        layer, cosine, error, fused1, fused2, matrix1, matrix2 = match.groups()
        for rows, fused, matrix in [(1, fused1, matrix1), (2, fused2, matrix2)]:
            dense_rows.append(dict(layer=int(layer), rows=rows, matrix_ms=float(matrix), fused_ms=float(fused),
                                   reduction_pct=100 * (1 - float(fused) / float(matrix)),
                                   cosine=float(cosine), relative_difference=float(error)))
    assert len(dense_rows) == 4, 'Expected two layers with one-row and two-row dense measurements'
    csv_write('dense.csv', dense_rows)

    head_before = statistics.mean(p['sum_stream_tok_s'] for p in phases('027_rank0_dense_as_moe') if p['streams'] == 15)
    head_after = statistics.mean(p['sum_stream_tok_s'] for p in phases('028_head_batching') if p['streams'] == 15)
    dense_before = statistics.mean(p['sum_stream_tok_s'] for p in phases('026_decode_kernel_group64') if p['streams'] == 15)
    mtp = load(EXPS / '039_mtp_fleet_rescore/results.json')
    attention = load(EXPS / '041_attention_int4/results.json')
    attention_rows = []
    for p in attention:
        if p['bits'] != 4:
            continue
        q = next(x for x in attention if x['bits'] == 8 and x['layer'] == p['layer'] and x['rows'] == p['rows'])
        a, b = p['q_us'] + p['o_us'], q['q_us'] + q['o_us']
        attention_rows.append(dict(layer=p['layer'], rows=p['rows'], int4_us=a, int8_us=b,
                                   reduction_pct=100 * (1 - a / b), relative_rms_pct=p['relative_rms_ppm'] / 10000))
    csv_write('attention_int4.csv', attention_rows)
    csv_write('mtp_families.csv', mtp['families'])
    derived = dict(head_before_mean_sum_rates=head_before, head_after_mean_sum_rates=head_after,
                   head_change_pct=100 * (head_after / head_before - 1),
                   dense_before_mean_sum_rates=dense_before,
                   dense_change_pct=100 * (head_before / dense_before - 1),
                   inflight176_change_pct=100 * (one('034_inflight10', 'mix176')['sum_stream_tok_s'] /
                                                one('034_inflight10', 'mix176', 'phases-baseline.json')['sum_stream_tok_s'] - 1),
                   mtp_fleet_original=mtp['original_a1'], mtp_fleet_deployment=mtp['quantized_a1'],
                   mtp_positions=mtp['positions'], mtp_sequences=mtp['sequences'],
                   mtp_vocab65k=mtp['prefix']['65536'],
                   mtp_vocabulary_difference_pp=100 * (mtp['original_a1'] - mtp['prefix']['65536']),
                   mtp_incremental_quantization_loss_pp=100 * (mtp['prefix']['65536'] - mtp['quantized_a1']),
                   phase_rows=len(phase_rows), experiment_directories=len(inventory),
                   telemetry_archives=len(telemetry), evidence_files=len(manifest['files']))
    save('derived.json', derived)
    save('audit.json', dict(source_commit=manifest['source_commit'], evidence_hashes_verified=len(manifest['files']),
                            phase_rows=len(phase_rows), aggregate_mismatches=mismatches,
                            incomplete_or_failed_phases=failed,
                            caveats=['Sum of individual decode rates is not a simultaneous aggregate counter.',
                                     'No per-request timing traces in phase summaries; no invented confidence intervals.',
                                     'Archived verdicts can be superseded; CLAIMS.md and AUDIT.md govern paper wording.']))
    assert not mismatches, mismatches

    tex = ['% Generated from the frozen evidence by reproduction/scripts/analyze.py.']
    values = {'LongTokens': str(long['tokens']), 'LongSeconds': f'{long["wall_s"]:.1f}',
              'LongPhaseRate': f'{long["aggregate_tok_s"]:.2f}',
              'LongSumRate': str(Decimal(str(long['sum_stream_tok_s'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
              'LongTTFT': f'{long["ttft_mean_s"]:.2f}', 'CounterMedian': f'{counter["median_rate"]:.2f}',
              'CounterMean': f'{counter["mean_rate"]:.2f}', 'HeadRegression': f'{-derived["head_change_pct"]:.2f}',
              'InflightRegression': f'{-derived["inflight176_change_pct"]:.2f}',
              'MTPFleet': f'{100*mtp["original_a1"]:.2f}', 'MTPDeployment': f'{100*mtp["quantized_a1"]:.2f}',
              'EvidenceFiles': str(len(manifest['files'])), 'ExperimentCount': str(len(inventory)),
              'PhaseCount': str(len(phase_rows)), 'TelemetryCount': str(len(telemetry))}
    for key, value in values.items():
        tex.append('\\newcommand{\\' + key + '}{' + value + '}')
    (GENERATED / 'numbers.tex').write_text('\n'.join(tex) + '\n')
    print(json.dumps(dict(**derived, incomplete_phases=len(failed), aggregate_mismatches=len(mismatches)), indent=2))


if __name__ == '__main__':
    main()
