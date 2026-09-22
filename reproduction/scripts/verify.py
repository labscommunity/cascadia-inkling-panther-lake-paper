#!/usr/bin/env python3
"""Check the frozen research artifact without fleet, model or network access."""
import csv
import gzip
import hashlib
import ipaddress
import json
import math
import re
import statistics
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'reproduction/evidence'
EXPS = EVIDENCE / 'source/autolab/experiments'
RESULTS = ROOT / 'reproduction/results'


def strict_load(text):
    def reject(value):
        raise ValueError(f'Nonstandard JSON number: {value}')
    return json.loads(text, parse_constant=reject)


def load(path):
    return strict_load(path.read_text())


def phase(exp, name, filename='phases.json'):
    return next(p for p in load(EXPS / exp / filename) if p['phase'] == name)


def close(a, b, tolerance=1e-9):
    assert math.isclose(a, b, rel_tol=0, abs_tol=tolerance), (a, b)


def main():
    manifest = load(EVIDENCE / 'manifest.json')
    assert manifest['source_commit'] == 'd1ab1abd7387b7f0b83d6d56b7aec2e1a56f9651'
    assert len(manifest['files']) == 357
    for entry in manifest['files']:
        data = (ROOT / entry['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
        assert len(data) == entry['bytes'], entry['path']
    print('PASS: 357 evidence files match frozen hashes and byte sizes.')

    all_phases = []
    for path in sorted(EXPS.glob('*/phases*.json')):
        for p in load(path):
            if 'phase' not in p:
                continue
            assert p['end'] > p['start']
            close(p['tokens'] / (p['end'] - p['start']), p['aggregate_tok_s'], 0.00051)
            all_phases.append(p)
    assert len(all_phases) == 125
    assert sum(p['completed'] != p['streams'] or bool(p['errors']) for p in all_phases) == 5
    assert len([d for d in EXPS.iterdir() if d.is_dir()]) == 49
    assert len(list((EVIDENCE / 'telemetry').glob('*.jsonl.gz'))) == 34
    print('PASS: all 125 aggregate rates recompute; five failed/incomplete rows retained.')

    with gzip.open(EVIDENCE / 'telemetry/011b_long_generation.jsonl.gz', 'rt') as f:
        stats = [r['stats'] for line in f if 'stats' in (r := strict_load(line))]
    long = phase('011b_long_generation', 'long176')
    assert stats[-1]['tokens_total'] - stats[0]['tokens_total'] == long['tokens'] == 21549
    assert long['completed'] == long['streams'] == 176
    audit = load(RESULTS / 'server_counter_audit.json')
    close(audit['phase_throughput'], long['tokens'] / (long['end'] - long['start']))
    close(audit['sum_stream_rates'], 70.235)
    print('PASS: server counter independently matches all 21,549 client tokens.')

    derived = load(RESULTS / 'derived.json')
    means = {}
    for e in ['026_decode_kernel_group64', '027_rank0_dense_as_moe', '028_head_batching']:
        means[e[:3]] = statistics.mean(phase(e, p)['sum_stream_tok_s'] for p in ['mix15a', 'mix15b'])
    close(derived['head_change_pct'], 100 * (means['028'] / means['027'] - 1))
    close(derived['dense_change_pct'], 100 * (means['027'] / means['026'] - 1))
    mtp = load(EXPS / '039_mtp_fleet_rescore/results.json')
    assert mtp['sequences'] == 36 and mtp['positions'] == 5724
    close(derived['mtp_fleet_original'], mtp['original_a1'])
    close(derived['mtp_fleet_deployment'], mtp['quantized_a1'])
    close(derived['mtp_incremental_quantization_loss_pp'], 100 * (mtp['prefix']['65536'] - mtp['quantized_a1']))
    close(derived['mtp_vocabulary_difference_pp'], 100 * (mtp['original_a1'] - mtp['prefix']['65536']))
    serving = list(csv.DictReader((RESULTS / 'serving.csv').open()))
    assert len(serving) == 5
    for row in serving:
        original = phase(row['experiment'], row['phase'])
        assert original['completed'] == original['streams'] == int(row['requests'])
        assert original['tokens'] == int(row['tokens'])
        assert original['tokens_req'] == int(row['output_cap'])
        close(float(row['phase_tok_s']), original['aggregate_tok_s'])
        close(float(row['sum_rates']), original['sum_stream_tok_s'])
    dense = list(csv.DictReader((RESULTS / 'dense.csv').open()))
    assert {(r['layer'], r['rows']) for r in dense} == {('0', '1'), ('0', '2'), ('1', '1'), ('1', '2')}
    for row in dense:
        close(float(row['reduction_pct']), 100 * (1 - float(row['fused_ms']) / float(row['matrix_ms'])))
    profiles = list(csv.DictReader((RESULTS / 'profiles.csv').open()))
    swapped = [r for r in profiles if r['experiment'] == '032_role_swap' and r['role'] == '0']
    assert swapped and all(r['installed_box'] == '8' for r in swapped)
    for exp in ['027_rank0_dense_as_moe', '028_head_batching']:
        selected = [r for r in profiles if r['experiment'] == exp and r['phase'] == 'mix15a' and r['role'] == '10']
        assert len(selected) == 1 and float(selected[0]['head_ms']) > 0
    print('PASS: contribution tables, derived comparisons and pipeline-role identity are consistent.')

    main_tex = (ROOT / 'main.tex').read_text()
    sources = load(ROOT / 'research/sources.json')
    keys = {s['key'] for s in sources}
    bib_keys = set(re.findall(r'@\w+\{([^,]+),', (ROOT / 'references.bib').read_text()))
    cited = {k.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}', main_tex) for k in group.split(',')}
    assert len(sources) == len(keys) == 33 and bib_keys == keys
    assert cited <= bib_keys, cited - bib_keys
    for s in sources:
        assert s['review'] and s['finding'] and urlparse(s['url']).scheme == 'https'
    for figure in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', main_tex):
        assert (ROOT / figure).is_file(), figure
    assert (ROOT / 'main.pdf').read_bytes().startswith(b'%PDF-')
    macros = (ROOT / 'generated/numbers.tex').read_text()
    assert r'\newcommand{\LongSumRate}{70.24}' in macros
    print(f'PASS: {len(cited)} cited sources resolve within the 33-source ledger; figures and PDF exist.')

    documents = [ROOT / 'README.md', ROOT / 'NOTICE.md', *ROOT.glob('research/*.md'), *ROOT.glob('reproduction/*.md')]
    for doc in documents:
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            if urlparse(link).scheme or link.startswith('#'):
                continue
            target = unquote(link.split('#')[0])
            assert (doc.parent / target).exists(), (str(doc.relative_to(ROOT)), target)
    print('PASS: report documentation links resolve locally (historical archive links excluded).')

    secret = re.compile(r'(?:github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
    identity = re.compile(r'/(?:Users|home)/[A-Za-z0-9_.-]+|\benx[0-9a-fA-F]{12}\b|\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b')
    ip_pattern = re.compile(r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])')
    checked = 0
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or any(p in {'.git', '__pycache__', '.venv'} for p in path.parts):
            continue
        if path.suffix not in {'.md', '.json', '.jsonl', '.gz', '.py', '.tex', '.bib', '.env', '.txt', '.cff'}:
            continue
        body = gzip.decompress(path.read_bytes()).decode() if path.suffix == '.gz' else path.read_text()
        # The scrubber/verifier contain pattern literals, not identifiers.
        assert not secret.search(body), f'Possible credential in {path.relative_to(ROOT)}'
        assert not identity.search(body), f'Unredacted identity in {path.relative_to(ROOT)}'
        for candidate in ip_pattern.findall(body):
            if candidate == '100.64.0.0' and path in {ROOT / 'reproduction/scripts/import_evidence.py', Path(__file__).resolve()}:
                continue  # The public CGNAT prefix is a redaction rule, not a fleet address.
            try:
                address = ipaddress.ip_address(candidate)
            except ValueError:
                continue
            private = address.is_private or address in ipaddress.ip_network('100.64.0.0/10')
            assert not private or address.is_loopback or address.is_unspecified, f'Private address in {path.relative_to(ROOT)}'
        if path.suffix == '.json':
            strict_load(body)
        elif path.suffix in {'.jsonl', '.gz'}:
            for line in body.splitlines():
                if line.strip():
                    strict_load(line)
        checked += 1
    print(f'PASS: {checked} text/archive files checked for strict JSON and known identity/credential patterns.')
    print('Artifact verification passed. This validates reconstruction, not inference quality or experimental causality.')


if __name__ == '__main__':
    main()
