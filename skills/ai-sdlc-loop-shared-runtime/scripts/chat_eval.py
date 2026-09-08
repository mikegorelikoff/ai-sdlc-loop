#!/usr/bin/env python3
"""Evaluate captured/simulated chat responses independently of Markdown wording.

Each skill owns eight source-fact scenarios. Deterministic rendering is a
simulation, not a live agent run. Preserve generated responses for review.
"""
from __future__ import annotations
import argparse
import hashlib
import sys
from pathlib import Path
import chat_output as chat
from ai_sdlc_toon import encode_toon


def digest(value):return hashlib.sha256(value.encode('utf-8')).hexdigest()


def run(skills_root: Path, capture_root: Path | None = None):
    items=[]
    for root in sorted(skills_root.glob('ai-sdlc-*')):
        if not (root/'SKILL.md').is_file():continue
        c=chat.contract(root)
        fixture=next((root/'tests/fixtures').glob('chat-scenarios.*'))
        suite=chat.read(fixture)
        if suite.get('skill')!=root.name or {x['id'] for x in suite['scenarios']}!=set(chat.SCENARIOS):
            raise ValueError('Scenario coverage mismatch: '+root.name)
        records=[]
        for case in suite['scenarios']:
            before=case['baseline_response']
            baseline=chat.evaluate(c,before,required_facts=case['required_facts'],expected_status=case['result']['summary']['Status'])
            response=chat.render(c,case['result'])
            retained=list(case['required_facts'])+list(case['result']['summary'].values())
            for field in ('primary','secondary','failures','clarifications','actions'):
                retained.extend(v for row in case['result'].get(field,[])[:8] for v in row.values())
            repeat=chat.render(c,case['result'])
            result=chat.evaluate(c,response,required_facts=retained,expected_status=case['result']['summary']['Status'])
            if response!=repeat:result['failures'].append({'code':'INCONSISTENT_SCHEMA','evidence':'Identical facts rendered different bytes'});result['status']='FAIL'
            # Mutation checks evaluate actual response defects, not instruction text.
            mutation_codes=[]
            bad=response.replace('| Status | Decision | Evidence |','| Area | Result | Details |',1)
            if chat.evaluate(c,bad)['status']!='FAIL':raise ValueError('Evaluator accepted wrong summary schema')
            mutation_codes.append('WRONG_SCHEMA')
            if chat.evaluate(c,'An unnecessary prose report.\n\n'+response)['status']!='FAIL':raise ValueError('Evaluator accepted prose-first mutation')
            mutation_codes.append('NON_TABULAR')
            if chat.evaluate(c,response.replace(case['result']['summary']['Status'],'GREEN',1))['status']!='FAIL':raise ValueError('Evaluator accepted invalid status')
            mutation_codes.append('UNCLEAR_STATUS')
            if case['required_facts']:
                fact=case['required_facts'][0]
                if chat.evaluate(c,response,required_facts=[fact+'-missing'])['status']!='FAIL':raise ValueError('Evaluator lost evidence checks')
                mutation_codes.append('MISSING_INFORMATION')
            if capture_root:
                out=capture_root/root.name;out.mkdir(parents=True,exist_ok=True)
                (out/(case['id']+'.md')).write_text(response,encoding='utf-8')
                (out/(case['id']+'.baseline.md')).write_text(before,encoding='utf-8')
            records.append({'scenario':case['id'],'baseline_status':baseline['status'],'status':result['status'],
                'failures':result['failures'],'iterations':3,'baseline_bytes':len(before.encode()),'response_bytes':len(response.encode()),
                'baseline_words':len(before.split()),'response_words':len(response.split()),'required_facts':len(set(retained)),
                'response_sha256':digest(response),'mutations_rejected':mutation_codes})
        items.append({'skill':root.name,'contract_sha256':digest(encode_toon(c)),'scenarios':records,'status':'PASS' if all(x['status']=='PASS' for x in records) else 'BLOCKED'})
    return {'schema':'ai-sdlc-chat-eval/v1','mode':'deterministic-simulation','semantic_review':'separate agent review; not a live provider eval',
            'skills':len(items),'scenarios':sum(len(x['scenarios']) for x in items),'failed':sum(y['status']!='PASS' for x in items for y in x['scenarios']),'items':items}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--skills-root',required=True,type=Path);p.add_argument('--capture-root',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        result=run(a.skills_root,a.capture_root);body=encode_toon(result)
        if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(body,encoding='utf-8')
        else:sys.stdout.write(body)
        return int(result['failed']!=0)
    except (ValueError,OSError,KeyError,TypeError) as e:print(str(e),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
