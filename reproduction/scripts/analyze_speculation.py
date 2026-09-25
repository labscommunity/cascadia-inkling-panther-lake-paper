#!/usr/bin/env python3
"""Reconstruct Section 4.3's measured comparisons and illustrative latency model."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPS = ROOT / 'reproduction/evidence/source/autolab/experiments'
OUT = ROOT / 'reproduction/results'


def load(path):
    return json.loads(path.read_text())


def csv_write(name, rows):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def phase(exp, name):
    return next(p for p in load(EXPS / exp / 'phases.json') if p['phase'] == name)


def main():
    before, after = '002a_return_link', '002b_speculation'
    a = {p['i']: p for p in load(EXPS / before / 'gate.json')['prompts']}
    b = {p['i']: p for p in load(EXPS / after / 'gate.json')['prompts']}
    def settings(exp):
        return [s.strip() for s in (EXPS / exp / 'fleet-overrides.env').read_text().splitlines()
                if s.strip() and not s.lstrip().startswith('#')]
    assert settings(after) == settings(before) + ['CASCADIA_STREAMS_SPEC=1']
    assert 'GATE_TOKENS = 32' in (EXPS.parent / 'bench/lab.py').read_text()
    assert 'CASCADIA_INKLING_OV_MOE=0' in settings(before)
    assert '6bad6fd8' in (EXPS / after / 'hypothesis.md').read_text()
    rows = []
    for i, name in [(0, 'Sky explanation'), (1, 'Capital of France'), (5, 'Six times seven')]:
        assert a[i]['exact'] and b[i]['exact']
        assert a[i]['text'] == b[i]['text']
        assert a[i]['match_chars'] == a[i]['of'] == b[i]['match_chars'] == b[i]['of']
        ratio = b[i]['tok_s'] / a[i]['tok_s']
        rows.append(dict(prompt_id=i, prompt=name, output_cap=32,
                         disabled_tok_s=a[i]['tok_s'], enabled_tok_s=b[i]['tok_s'],
                         ratio=ratio, gain_pct=100*(ratio-1), reference_match=True))
    csv_write('speculation_toggle.csv', rows)

    families = []
    for p in load(EXPS / '015c_ensemble/phases.json'):
        assert p['streams'] == p['completed'] == 1 and p['tokens'] == 128
        families.append(dict(phase=p['phase'], decode_tok_s=p['sum_stream_tok_s'],
                             phase_tok_s=p['tokens']/(p['end']-p['start']), output_tokens=p['tokens']))
    csv_write('speculation_families.csv', families)

    survey = load(EXPS / '046_final_performance/measurements.json')
    first = next(p for p in survey if p['phase']=='mixed_a_c001')
    repeat = next(p for p in survey if p['phase']=='mixed_b_c001')
    equality = load(EXPS / '046_final_performance/single-stream-comparison.json')
    assert equality['identical_outputs'] == equality['identical_prompts'] == 12
    echo = phase(after, 'echo')
    # This count/stage interval comes from the retained load-study summary;
    # the resulting model prediction is explicitly distinct from a timing measurement.
    verdict = (EXPS / after / 'verdict.md').read_text()
    hits, tokens = map(int, re.search(r'copy task had (\d+) of (\d+) tokens', verdict).groups())
    stage_ms, stages = re.search(r'T = ([\d.]+) ms, D = (\d+)', verdict).groups()
    stage_s, stages = float(stage_ms)/1000, int(stages)
    assert tokens == echo['tokens'] == 96
    fraction = hits/tokens
    round_s = stages*stage_s
    predicted = 1/(fraction*stage_s+(1-fraction)*round_s)
    result = dict(
        toggle=dict(source_before=before, source_after=after, same_binary='6bad6fd8',
                    execution='Earlier CPU-expert configuration with iGPU attention projections and output head.',
                    output_cap=32, requests_per_prompt_per_condition=1, comparisons=rows,
                    interpretation='Sequential same-binary toggle observations, not randomized repeated estimates.'),
        copy=dict(source=after, phase='echo', measured_decode_tok_s=echo['sum_stream_tok_s'],
                  summary_confirmed_inflight=hits, tokens=tokens, effective_hit_fraction=fraction,
                  illustrative_stage_s=stage_s, illustrative_stages=stages,
                  illustrative_round_s=round_s, predicted_decode_tok_s=predicted,
                  predicted_speedup=predicted*round_s,
                  interpretation='First-order latency model; stage interval and hit count from retained summary; no matched copy-task disabled timing.'),
        repeat=dict(first_decode=first['steady_aggregate_tok_s'], repeat_decode=repeat['steady_aggregate_tok_s'],
                    decode_ratio=repeat['steady_aggregate_tok_s']/first['steady_aggregate_tok_s'],
                    first_phase=first['aggregate_tok_s'], repeat_phase=repeat['aggregate_tok_s'],
                    phase_ratio=repeat['aggregate_tok_s']/first['aggregate_tok_s'], identical_outputs=12,
                    interpretation='Speculation enabled in both passes; history/order and capture-state contrast, not an on/off ablation.'))
    (OUT / 'speculation_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    tex = ['% Generated from retained speculative-serving comparisons.', r'\newcommand{\SpeculationRows}{%']
    tex.extend(f'{r["prompt"]} & {r["disabled_tok_s"]:.3f} & {r["enabled_tok_s"]:.3f} & '
               f'{r["ratio"]:.2f}' + r'$\times$ & +' + f'{r["gain_pct"]:.1f}' + r'\% \\' for r in rows)
    tex.extend(['}', r'\newcommand{\SpecRepeatRatio}{'+f'{result["repeat"]["decode_ratio"]:.2f}'+'}',
                r'\newcommand{\SpecRepeatPhaseRatio}{'+f'{result["repeat"]["phase_ratio"]:.2f}'+'}',
                r'\newcommand{\SpecCopyPrediction}{'+f'{predicted:.2f}'+'}'])
    (ROOT / 'generated/speculation.tex').write_text('\n'.join(tex)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
