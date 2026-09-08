"""Regression checks for semantic chat contracts, evidence retention and bounded Markdown."""
from __future__ import annotations
import copy
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
SKILLS=HERE.parents[2]
SHARED=HERE.parents[1]
sys.path.insert(0,str(SHARED/'scripts'))
import chat_output as chat
import chat_eval

class ChatOutputTests(unittest.TestCase):
    def setUp(self):
        self.root=SKILLS/(SHARED.name.removesuffix('shared-runtime')+'validation')
        self.c=chat.contract(self.root)
        self.v={'schema':'ai-sdlc-chat-result/v1','summary':{'Status':'PASS','Decision':'Check completed','Evidence':'test.log:1'},'primary':[self.c['example']]}

    def test_every_skill_has_eight_executed_scenarios(self):
        result=chat_eval.run(SKILLS)
        self.assertEqual(result['failed'],0)
        self.assertEqual(result['scenarios'],result['skills']*8)

    def test_source_contracts_are_visible_in_own_instructions(self):
        for root in SKILLS.glob('ai-sdlc-*'):
            if not (root/'SKILL.md').is_file():continue
            c=chat.contract(root);s=(root/'SKILL.md').read_text()
            self.assertIn('## Chat Output Contract',s)
            for col in c['primary']:self.assertIn(col,s)

    def test_unknown_fields_and_missing_evidence_fail(self):
        for mutate in [lambda v:v.update(unknown='hidden'),lambda v:v['summary'].pop('Evidence'),lambda v:v['primary'][0].pop('Evidence')]:
            v=copy.deepcopy(self.v);mutate(v)
            with self.assertRaises(ValueError):chat.render(self.c,v)

    def test_invalid_status_and_contradictory_pass_fail(self):
        v=copy.deepcopy(self.v);v['summary']['Status']='GREEN'
        with self.assertRaises(ValueError):chat.render(self.c,v)
        v=copy.deepcopy(self.v);v['failures']=[dict(zip(self.c['failure'],['command','BLOCKED','Missing tool','test.log:1','Install tool']))]
        with self.assertRaises(ValueError):chat.render(self.c,v)

    def test_invalid_markdown_mutations_are_rejected(self):
        response=chat.render(self.c,self.v)
        candidates=[
            'Prose report\n'+response,
            response.replace('| Status | Decision | Evidence |','| Area | Result | Details |'),
            response.replace('| --- | --- | --- |','| --- | --- |'),
            response.replace('Check completed','x'*181),
            response+'\nCheck completed\n',
            '```markdown\n'+response+'```\n',
            response.replace('PASS','GREEN',1),
        ]
        for candidate in candidates:self.assertEqual(chat.evaluate(self.c,candidate)['status'],'FAIL')

    def test_missing_required_fact_is_detected_without_sentence_matching(self):
        response=chat.render(self.c,self.v)
        self.assertEqual(chat.evaluate(self.c,response,required_facts=['test.log:1'])['status'],'PASS')
        self.assertEqual(chat.evaluate(self.c,response,required_facts=['AC-999'])['status'],'FAIL')
        self.assertEqual(chat.evaluate(self.c,response.replace('Check completed','Assertions passed'),required_facts=['test.log:1'])['status'],'PASS')

    def test_large_preview_is_explicit_and_repeatable(self):
        self.v['primary']=[{**self.c['example'],self.c['primary'][0]:'check-'+str(i)} for i in range(20)]
        with self.assertRaises(ValueError):chat.render(self.c,self.v)
        self.v['full_artifact']='full-report.toon';s=chat.render(self.c,self.v)
        self.assertEqual(s,chat.render(self.c,self.v));self.assertIn('| 8 | 20 | full-report.toon |',s)
        self.assertNotIn('check-19',s)

    def test_escaping_preserves_native_bytes_and_table_shape(self):
        self.v['primary'][0][self.c['primary'][0]]='literal | value\nперенос'
        native='```embedded\n| not | a chat table |\n  exact whitespace\n'
        self.v['native']=[{'language':'text','content':native}]
        s=chat.render(self.c,self.v);self.assertIn(native,s)
        self.assertEqual(chat.evaluate(self.c,s,required_facts=['literal | value\nперенос'])['status'],'PASS')

    def test_symlink_contract_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/self.root.name;(root/'references').mkdir(parents=True)
            source=next((self.root/'references').glob('chat-output.*'))
            try:(root/'references'/source.name).symlink_to(source)
            except OSError:self.skipTest('Symlinks unavailable')
            with self.assertRaises(ValueError):chat.contract(root)

    def test_failure_needs_owned_action(self):
        self.v['summary']['Status']='BLOCKED'
        self.v['failures']=[dict(zip(self.c['failure'],['command','BLOCKED','Missing tool','test.log:1','Install tool']))]
        with self.assertRaises(ValueError):chat.render(self.c,self.v)
        self.v['actions']=[dict(zip(chat.ACTIONS,['Maintainer','Install tool','Tool version output']))]
        self.assertEqual(chat.evaluate(self.c,chat.render(self.c,self.v))['status'],'PASS')

    def test_failure_clarification_and_summary_mutations(self):
        suite=chat.read(self.root/'tests/fixtures/chat-scenarios.toon')
        for case_id,key in [('blocked','failure'),('missing-input','clarification')]:
            v=next(x['result'] for x in suite['scenarios'] if x['id']==case_id)
            response=chat.render(self.c,v)
            self.assertEqual(chat.evaluate(self.c,response)['status'],'PASS')
            malformed=response.replace('| '+' | '.join(self.c[key])+' |','| Missing | Details |')
            self.assertEqual(chat.evaluate(self.c,malformed)['status'],'FAIL')
            malformed=response.replace('| BLOCKED |','| PASS |',1)
            self.assertEqual(chat.evaluate(self.c,malformed)['status'],'FAIL')

    def test_summary_only_no_findings_is_explicit(self):
        self.v.pop('primary')
        self.v['summary']['Decision']='No findings within the reviewed diff; report.toon records scope.'
        response=chat.render(self.c,self.v)
        self.assertEqual(chat.evaluate(self.c,response,required_facts=['report.toon'])['status'],'PASS')

    def test_workflow_presentation_retains_handoffs_and_stops_on_blockers(self):
        names=(['requirements-discovery','requirements-review','specify','implement','engineering-quality-gate','verify','commit-prep']
               if SHARED.name.startswith('ai-sdlc-loop-') else
               ['working-backwards-discovery','ba','prfaq-package-synthesis','requirements-readiness-review','sdd','backlog-decomposition-and-task-planning','validation'])
        prefix=SHARED.name.removesuffix('shared-runtime')
        previous='request.md'
        visited=[]
        for name in names:
            skill=SKILLS/(prefix+name)
            c=chat.contract(skill)
            fixture=skill/'tests/fixtures/chat-scenarios.toon'
            suite=chat.read(fixture)
            value=copy.deepcopy(next(x['result'] for x in suite['scenarios'] if x['id']=='happy'))
            value['summary']['Evidence']=previous
            response=chat.render(c,value)
            self.assertEqual(chat.evaluate(c,response,required_facts=[previous],expected_status=value['summary']['Status'])['status'],'PASS')
            visited.append(name)
            if value['summary']['Status'] in ('FAIL','BLOCKED'):
                self.assertTrue(value['failures'])
                break  # Formatting PASS never advances a blocked delivery stage.
            previous=name+'.toon'
        self.assertIn(visited[-1],('requirements-review','requirements-readiness-review'))
        self.assertNotIn('commit-prep',visited)
        self.assertNotIn('validation',visited)

if __name__=='__main__':unittest.main()
