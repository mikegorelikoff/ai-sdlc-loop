#!/usr/bin/env python3
"""Run property fixtures and retain deterministic candidate response captures.

Synthetic review assertions test gate enforcement, not live model accuracy.
Exit 0: expected properties hold; 1: regression; 2: malformed fixture or output.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import decompose as engine


def evaluate(fixtures, capture_root=None):
    cases=[]
    paths=sorted(fixtures.glob('case-*.toon'))
    if not paths:raise engine.Invalid('empty eval corpus')
    for path in paths:
        fixture=engine.load(path)
        report=engine.evaluate(fixture['candidate'])
        response=engine.render(report)
        codes={d['code'] for d in report['quality_report']}
        failures=[]
        if report['status']!=fixture['expected_status']:failures.append('UNEXPECTED_STATUS')
        if not set(fixture['expected_codes'])<=codes:failures.append('MISSING_EXPECTED_DEFECT')
        if not response.startswith('## Decomposition Summary\n\n| Metric | Result |'):failures.append('NON_TABULAR')
        if '| ID | Type | Parent | Title | Outcome | Status |' not in response:failures.append('WRONG_SCHEMA')
        for line in response.splitlines():
            if line.startswith('|') and len(line.split('|'))>8:failures.append('TOO_WIDE')
        if engine.evaluate(fixture['candidate'])!=report:failures.append('NONDETERMINISTIC')
        if engine.codec.loads(engine.encoded(report))!=report:failures.append('LOSSY_ROUND_TRIP')
        if capture_root:
            engine.atomic_write_text(capture_root,Path(path.stem+'.md'),response)
            engine.atomic_write_text(capture_root,Path(path.stem+'.toon'),engine.encoded(report))
        cases.append(dict(name=fixture['name'],status='PASS' if not failures else 'FAIL',failures=failures,expected=fixture['expected_status'],actual=report['status'],candidate_fingerprint=report['candidate_fingerprint'],response_words=len(response.split())))
    return dict(schema='ai-sdlc-decomposition-eval/v1',mode='simulated-property-fixtures',cases=cases,passed=sum(c['status']=='PASS' for c in cases),failed=sum(c['status']=='FAIL' for c in cases),semantic_limit='Property fixtures plus independent engineering review; no live provider accuracy claim')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--fixtures',type=Path,default=Path(__file__).resolve().parents[1]/'tests/fixtures');p.add_argument('--capture-root',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    try:
        if a.capture_root:a.capture_root.mkdir(parents=True,exist_ok=True)
        report=evaluate(a.fixtures,a.capture_root.resolve() if a.capture_root else None)
        text=engine.encoded(report)
        if a.output:engine.atomic_write_text(a.output.parent.resolve(),Path(a.output.name),text)
        else:print(text,end='')
        return int(report['failed']>0)
    except (ValueError,OSError,KeyError) as exc:
        print(engine.encoded(dict(error='EVAL_INVALID',message=str(exc))),end='');return 2
if __name__=='__main__':raise SystemExit(main())
