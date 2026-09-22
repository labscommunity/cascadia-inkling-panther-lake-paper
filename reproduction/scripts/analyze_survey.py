#!/usr/bin/env python3
"""Reconstruct the finalized survey from retained token-event traces, offline."""
import collections
import csv
import gzip
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'reproduction/evidence'
SOURCE = EVIDENCE / 'source/autolab/experiments/046_final_performance'
RAW = EVIDENCE / 'requests/046_final_performance'
OUT = ROOT / 'reproduction/results'


def load(path):
    return json.loads(path.read_text())


def raw(name):
    with gzip.open(RAW / (name + '.jsonl.gz'), 'rt') as f:
        return [json.loads(line) for line in f if line.strip()]


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-8), (a, b)


def quantile(xs, q):
    xs = sorted(xs)
    p = (len(xs) - 1) * q
    lo, hi = math.floor(p), math.ceil(p)
    return xs[lo] + (xs[hi] - xs[lo]) * (p - lo)


def csv_write(name, rows):
    with (OUT / name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)


def main():
    phases = load(SOURCE / 'measurements.json')
    stats = raw('api-stats')
    audited, events_total, all_requests, counters, brackets = [], 0, 0, 0, 0
    for p in phases:
        requests = raw(p['phase'])
        assert len(requests) == p['requests'] == len(p['request_metrics'])
        assert len(requests) == p['streams'] * len(p['cohorts'])
        all_requests += len(requests)
        for r, metric in zip(requests, p['request_metrics']):
            assert sum(n for _, n in r['events']) == r['tokens'] == r['usage']['completion_tokens']
            assert r['tokens'] == p['tokens_req']
            assert r['prompt_tokens'] == r['usage']['prompt_tokens']
            assert r['finish_reason'] == 'length'
            close(r['started'], metric['started'])
            close(r['events'][0][0] - r['started'], r['ttft_s'])
            rate = (r['tokens'] - r['events'][0][1]) / (r['events'][-1][0] - r['events'][0][0])
            close(rate, metric['decode_tok_s'])
            events_total += len(r['events'])
        token_total = sum(r['tokens'] for r in requests)
        assert token_total == p['tokens']
        close(token_total / (p['end'] - p['start']), p['aggregate_tok_s'])
        overlap_tokens, overlap_s = 0, 0
        for i, cohort in enumerate(p['cohorts']):
            group = requests[i*p['streams']:(i+1)*p['streams']]
            lo = max(r['events'][0][0] for r in group)
            hi = min(r['events'][-1][0] for r in group)
            count = sum(n for r in group for t, n in r['events'] if lo < t <= hi)
            assert hi > lo and count == cohort['overlap_tokens']
            close(lo, cohort['overlap_start']); close(hi, cohort['overlap_end'])
            close(hi-lo, cohort['overlap_s'])
            overlap_tokens += count; overlap_s += hi-lo
        close(overlap_tokens / overlap_s, p['steady_aggregate_tok_s'])
        close(p['steady_aggregate_tok_s'] / p['streams'], p['steady_per_stream_tok_s'])
        for field, q in [('ttft_median_s', .5), ('ttft_p95_s', .95)]:
            close(quantile([r['ttft_s'] for r in requests], q), p[field])
        before = [s for s in stats if p['start']-10 <= s['time'] <= p['start'] and s['requests_in_flight'] == 0]
        after = [s for s in stats if p['end'] <= s['time'] <= p['end']+10 and s['requests_in_flight'] == 0]
        bracketed = bool(before and after)
        matched = bracketed and after[0]['tokens_total'] - before[-1]['tokens_total'] == token_total
        if bracketed:
            assert matched, p['phase']
        brackets += bracketed
        counters += matched
        audited.append(dict(phase=p['phase'], family=p['family'], concurrency=p['streams'],
                            requests=p['requests'], tokens=p['tokens'], output_cap=p['tokens_req'],
                            shared_decode_tokens=overlap_tokens, shared_decode_s=overlap_s,
                            decode_tok_s=overlap_tokens/overlap_s, phase_tok_s=p['aggregate_tok_s'],
                            mean_decode_per_stream=p['steady_per_stream_tok_s'],
                            ttft_median_s=p['ttft_median_s'], ttft_p95_s=p['ttft_p95_s'],
                            unique_prompts=len({r['prompt'] for r in requests}),
                            capture_writes=p.get('capture_writes', 'pilot'),
                            capacity_retries=p.get('capacity_retries', 0),
                            sampled_server_counter_status='matched' if matched else 'no_idle_bracket'))

    csv_write('survey_phases.csv', audited)
    grouped = collections.defaultdict(list)
    for p in phases:
        if p['phase'].startswith('mixed_'):
            grouped[p['streams']].append(p)
    curve = []
    for n, rr in sorted(grouped.items()):
        assert len(rr) == 2
        decode = [p['steady_aggregate_tok_s'] for p in rr]
        end = [p['aggregate_tok_s'] for p in rr]
        ttft = [r['ttft_s'] for p in rr for r in p['request_metrics']]
        curve.append(dict(concurrency=n, runs=len(rr), requests=sum(p['requests'] for p in rr),
                          mean_decode_tok_s=statistics.mean(decode), decode_min=min(decode), decode_max=max(decode),
                          mean_phase_tok_s=statistics.mean(end), phase_min=min(end), phase_max=max(end),
                          mean_decode_per_stream=statistics.mean(decode)/n,
                          ttft_median_s=quantile(ttft,.5), ttft_p95_s=quantile(ttft,.95)))
    csv_write('concurrency.csv', curve)
    peak = max(curve, key=lambda p:p['mean_decode_tok_s'])
    original_summary = load(SOURCE / 'summary.json')
    close(peak['mean_decode_tok_s'], original_summary['peak_steady_tok_s'])
    close(peak['mean_phase_tok_s'], original_summary['peak_end_to_end_tok_s'])
    reported = [p for p in phases if not p['phase'].startswith('pilot')]
    result = dict(source_commit=load(EVIDENCE/'manifest.json')['source_commit'],
                  survey_records=len(phases), reported_phases=len(reported), pilot_phases=len(phases)-len(reported),
                  mixed_phases=sum(len(v) for v in grouped.values()), mixed_concurrency_settings=len(curve),
                  reported_requests=sum(p['requests'] for p in reported), reported_tokens=sum(p['tokens'] for p in reported),
                  audited_requests=all_requests, audited_token_events=events_total,
                  raw_counter_matches=counters, raw_counter_bracketed_phases=brackets,
                  raw_counter_unbracketed_phases=[p['phase'] for p in audited if p['sampled_server_counter_status']=='no_idle_bracket'],
                  raw_counter_method='Nearest idle polls within ten seconds around each phase.',
                  peak=peak, interactive=next(p for p in curve if p['concurrency']==15),
                  serial=next(p for p in curve if p['concurrency']==1))
    (OUT/'survey_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    macros = {'SurveyDecode':f'{peak["mean_decode_tok_s"]:.2f}', 'SurveyPhase':f'{peak["mean_phase_tok_s"]:.2f}',
              'SurveyTTFT':f'{result["interactive"]["ttft_median_s"]:.2f}',
              'SurveyPeakStreams':str(peak['concurrency']), 'SurveyRecords':str(len(phases))}
    (ROOT/'generated/survey.tex').write_text('% Generated from the finalized survey token-event reconstruction.\n'+
        '\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in macros.items())+'\n')
    (ROOT/'generated/concurrency_rows.tex').write_text('% Generated paired phase means and pooled request quantiles.\n'+
        '\\newcommand{\\ConcurrencyRows}{%\n'+
        '\n'.join(f'{p["concurrency"]} & {p["mean_decode_tok_s"]:.2f} & {p["mean_phase_tok_s"]:.2f} & '
                  f'{p["mean_decode_per_stream"]:.3f} & {p["ttft_median_s"]:.2f} & {p["ttft_p95_s"]:.2f} '
                  + r'\\' for p in curve)+'\n}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
