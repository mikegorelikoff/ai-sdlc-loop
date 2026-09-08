"""Property and mutation corpus; semantic candidates are authored fixtures."""
import copy
import subprocess
from unittest import mock
import sys
import tempfile
import unittest
from pathlib import Path

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[1]/'scripts'))
import ai_sdlc_hunters as H
PREFIX=HERE.parents[1].name[:-len('shared-runtime')]

class HunterTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory();self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)
        self.write('requirements.md','REQ-01: input count using database and external API with timestamp.\n')
        self.write('design.md','A component stores records.\n')
        self.write('operations.md','An operator starts the service.\n')
        self.write('app.py','def run():\n    return 1\n')
        self.write('test_app.py','import unittest\nfrom app import run\nclass Contract(unittest.TestCase):\n    def test_requirement(self):\n        self.assertEqual(run(),2)\n')
        self.inventory=[dict(path=p,role=r) for p,r in [('requirements.md','requirements'),('design.md','design'),('operations.md','operations'),('app.py','implementation'),('test_app.py','tests')]]

    def write(self,path,text):
        target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')

    def prepared(self,kind):return H.prepare(self.root,kind,'fixture',self.inventory)

    def candidate(self,value,dimension=None):
        kind=value['hunter'];path='app.py' if kind=='bug-hunter' else 'requirements.md'
        return dict(signature='declared-scenario',dimension=dimension or value['dimensions'][0],title='Current contract concern',condition='The scoped input reaches the boundary',expected='REQ-01 holds at the boundary',severity='high',impact='Required behavior may fail',evidence_type='OBSERVED' if kind=='bug-hunter' else 'INFERRED' if kind=='blind-case-hunter' else 'HYPOTHETICAL',evidence=dict(path=path,line=1,quote=(self.root/path).read_text().splitlines()[0]),trace_targets=['REQ-01'],owner='QA',next_action='Validate the targeted behavior',review=dict(decision='ACCEPT',reason='Reviewed against REQ-01'),test_refs=['test_app.py'],related_findings=[],reproduction='')

    def report(self,kind,dimension=None):
        value=self.prepared(kind);value['candidates']=[self.candidate(value,dimension)]
        return H.evaluate(self.root,value)

    def repro_candidate(self):
        value=self.prepared('bug-hunter');value['candidates']=[self.candidate(value)]
        receipt=H.reproduce(self.root,value,'test_app.py','repro.log')
        self.write('repro.toon',H.encode_toon(receipt));value['candidates'][0]['reproduction']='repro.toon'
        return value,receipt

    def test_edge_applicability_corpus(self):
        scenarios=[('pure function input','INPUT'),('HTTP endpoint with external API','NETWORK'),('state workflow','LIFECYCLE'),('database update','PERSISTENCE'),('concurrent transaction','CONCURRENCY'),('external API retry','RETRY'),('date range timestamp','TIME'),('pagination with large dataset','DATA_VOLUME')]
        for description,dimension in scenarios:
            with self.subTest(description=description):
                self.write('requirements.md','REQ-01: '+description+'\n')
                value=self.prepared('edge-case-hunter');self.assertIn(dimension,value['dimensions'])
                value['candidates']=[self.candidate(value,dimension)]
                result=H.evaluate(self.root,value)
                self.assertEqual('MAPPED',result['findings'][0]['validation_status'])
                self.assertEqual([dimension],result['dimensions_with_cases'])

    def test_blind_omission_corpus(self):
        for dimension in ['ACTORS','FAILURE_RECOVERY','ROLLBACK','MIGRATION','TEMPORAL_MODEL']:
            with self.subTest(dimension=dimension):
                result=self.report('blind-case-hunter',dimension)
                self.assertEqual('MISSING',result['findings'][0]['validation_status'])
                self.assertEqual('ABSENT_IN_DECLARED_SCOPE',result['absence_searches'][0]['status'])

    def test_missing_permission_flow(self):
        self.write('requirements.md','REQ-01: admin role receives input.\n')
        self.assertEqual('MISSING',self.report('blind-case-hunter','PERMISSIONS')['findings'][0]['validation_status'])

    def test_blind_absence_needs_all_roles(self):
        self.inventory=[r for r in self.inventory if r['role']!='operations']
        result=self.report('blind-case-hunter','ROLLBACK')
        self.assertEqual('UNKNOWN',result['findings'][0]['validation_status'])

    def test_covered_elsewhere_is_not_absent(self):
        self.write('operations.md','Rollback restores the previous deployment.\n')
        result=self.report('blind-case-hunter','ROLLBACK')
        self.assertEqual('UNVERIFIED',result['findings'][0]['validation_status'])
        self.assertTrue(result['absence_searches'][0]['matches'])

    def test_out_of_scope_is_not_missing(self):
        self.write('operations.md','Rollback is explicitly outside this prototype.\n')
        value=self.prepared('blind-case-hunter');value['candidates']=[self.candidate(value,'ROLLBACK')]
        value['coverage']=[dict(dimension='ROLLBACK',status='OUT_OF_SCOPE',evidence=dict(path='operations.md',line=1,quote='Rollback is explicitly outside this prototype.'))]
        finding=H.evaluate(self.root,value)['findings'][0]
        self.assertEqual(('REJECTED','OUT_OF_SCOPE'),(finding['validation_status'],finding['validation_reason']))

    def test_bug_without_reproduction_is_supported_not_confirmed(self):
        self.assertEqual('SUPPORTED',self.report('bug-hunter')['findings'][0]['validation_status'])

    def test_bug_mutation_corpus(self):
        mutations={'obvious':'return 1','boundary':'return len([1])+0','inverted-condition':'return 1 if True else 2','missing-retry':'return sum([1])','lost-update-interleaving':'a=0; b=0; a+=1; b+=1; return b','removed-error-handling':'return 0','stale-state':'state=2; old=1; return old'}
        for label,body in mutations.items():
            with self.subTest(mutation=label):
                self.write('app.py','def run():\n    '+body+'\n')
                value,receipt=self.repro_candidate()
                self.assertEqual('REPRODUCED',receipt['status'])
                self.assertEqual('CONFIRMED',H.evaluate(self.root,value)['findings'][0]['validation_status'])

    def test_unusual_correct_code_not_confirmed(self):
        self.write('app.py','def run():\n    return sum([1,1])\n')
        value,receipt=self.repro_candidate()
        self.assertEqual('UNVERIFIED',receipt['status'])
        self.assertEqual('UNVERIFIED',H.evaluate(self.root,value)['findings'][0]['validation_status'])

    def test_failing_test_requires_review(self):
        value,receipt=self.repro_candidate();value['candidates'][0]['review']['decision']='PENDING'
        self.assertEqual('REPRODUCED',H.evaluate(self.root,value)['findings'][0]['validation_status'])

    def test_misleading_test_stdout_cannot_confirm_error(self):
        self.write('test_app.py',"import unittest\nclass T(unittest.TestCase):\n    def test_run(self):\n        print('FAILED (failures=1)')\n        raise RuntimeError('infrastructure')\n")
        value,receipt=self.repro_candidate()
        self.assertEqual((0,1,'UNVERIFIED'),(receipt['failures'],receipt['errors'],receipt['status']))
        self.assertEqual('UNVERIFIED',H.evaluate(self.root,value)['findings'][0]['validation_status'])

    def test_infrastructure_error_is_unverified(self):
        self.write('test_app.py','import unavailable_dependency\n')
        value,receipt=self.repro_candidate()
        self.assertEqual('UNVERIFIED',receipt['status'])
        self.assertEqual('UNVERIFIED',H.evaluate(self.root,value)['findings'][0]['validation_status'])

    def test_hypothesis_does_not_become_confirmed(self):
        value,receipt=self.repro_candidate();value['candidates'][0]['evidence_type']='HYPOTHETICAL'
        self.assertEqual('REPRODUCED',H.evaluate(self.root,value)['findings'][0]['validation_status'])

    def test_false_bug_rejected(self):
        value=self.prepared('bug-hunter');item=self.candidate(value);item['review']=dict(decision='REJECT',reason='EXPECTED_BEHAVIOR established by requirements');value['candidates']=[item]
        self.assertEqual('REJECTED',H.evaluate(self.root,value)['findings'][0]['validation_status'])

    def test_source_drift_blocks(self):
        value=self.prepared('edge-case-hunter');self.write('requirements.md','REQ-01 changed\n')
        with self.assertRaisesRegex(H.Invalid,'stale'):H.evaluate(self.root,value)

    def test_forged_quote_blocks(self):
        value=self.prepared('edge-case-hunter');item=self.candidate(value);item['evidence']['quote']='Invented evidence';value['candidates']=[item]
        with self.assertRaisesRegex(H.Invalid,'quoted evidence'):H.evaluate(self.root,value)

    def test_missing_trace_blocks(self):
        value=self.prepared('edge-case-hunter');item=self.candidate(value);item['trace_targets']=['REQ-999'];value['candidates']=[item]
        with self.assertRaisesRegex(H.Invalid,'trace target'):H.evaluate(self.root,value)

    def test_duplicate_exact_signature_merges(self):
        value=self.prepared('edge-case-hunter');item=self.candidate(value);value['candidates']=[item,copy.deepcopy(item)]
        report=H.evaluate(self.root,value);self.assertEqual(1,len(report['findings']));self.assertEqual(1,len(report['duplicate_ids']))

    def test_conflicting_signature_rejected(self):
        value=self.prepared('edge-case-hunter');a=self.candidate(value);b=copy.deepcopy(a);b['expected']='Different product requirement';value['candidates']=[a,b]
        with self.assertRaisesRegex(H.Invalid,'conflicting facts'):H.evaluate(self.root,value)

    def test_repeated_state_and_render(self):
        for kind in H.KINDS:
            with self.subTest(kind=kind):
                value=self.prepared(kind);value['candidates']=[self.candidate(value)]
                first=H.evaluate(self.root,value);second=H.evaluate(self.root,value)
                self.assertEqual(H.encode_toon(first),H.encode_toon(second))
                self.assertEqual(first,H.decode_toon(H.encode_toon(first)))
                skill=HERE.parents[2]/(PREFIX+kind)
                self.assertEqual(H.render(skill,first),H.render(skill,second))

    def test_cross_hunter_linked_lifecycle(self):
        blind=self.report('blind-case-hunter','FAILURE_RECOVERY');self.write('blind.toon',H.encode_toon(blind))
        edge=self.prepared('edge-case-hunter');edge['related_reports']=['blind.toon'];item=self.candidate(edge,'NETWORK');item['related_findings']=[blind['findings'][0]['id']];edge['candidates']=[item]
        er=H.evaluate(self.root,edge);self.write('edge.toon',H.encode_toon(er))
        bug,receipt=self.repro_candidate();bug['related_reports']=['edge.toon'];bug['candidates'][0]['related_findings']=[er['findings'][0]['id']]
        br=H.evaluate(self.root,bug)
        self.assertEqual('CONFIRMED',br['findings'][0]['validation_status'])
        self.assertEqual(3,len({blind['findings'][0]['id'],er['findings'][0]['id'],br['findings'][0]['id']}))
        self.assertFalse(br['authorizes_execution'])

    def test_unresolved_cross_hunter_link(self):
        value=self.prepared('bug-hunter');c=self.candidate(value);c['related_findings']=['invented'];value['candidates']=[c]
        with self.assertRaisesRegex(H.Invalid,'related finding'):H.evaluate(self.root,value)

    def test_reproduction_receipt_tampering(self):
        value,receipt=self.repro_candidate();receipt['failures']=99;receipt['fingerprint']=H.digest({k:v for k,v in receipt.items() if k!='fingerprint'});self.write('repro.toon',H.encode_toon(receipt))
        with self.assertRaisesRegex(H.Invalid,'contradicts log'):H.evaluate(self.root,value)

    def test_iteration_bound(self):
        value=self.prepared('edge-case-hunter');value['iteration']=4
        with self.assertRaisesRegex(H.Invalid,'repair limit'):H.evaluate(self.root,value)

    def test_risk_signals_are_machine_owned(self):
        self.write('app.py','def run(x):\n    if x: return 1\n    return 2\n')
        value=self.prepared('bug-hunter');self.assertEqual('CONDITIONAL',value['signals'][0]['kind'])
        value['signals']=[]
        with self.assertRaisesRegex(H.Invalid,'risk signals'):H.evaluate(self.root,value)

    def test_no_source_mutation(self):
        before={r['path']:read for r in self.inventory for read in [(self.root/r['path']).read_bytes()]}
        value,receipt=self.repro_candidate();H.evaluate(self.root,value)
        self.assertEqual(before,{p:(self.root/p).read_bytes() for p in before})
        with self.assertRaisesRegex(H.Invalid,'overwrite source'):H.reproduce(self.root,value,'test_app.py','app.py')

    def test_budget_and_unknown_scope_block(self):
        self.write('requirements.md','REQ-01: unclassified domain.\n')
        inventory=[dict(path='requirements.md',role='requirements')]
        value=H.prepare(self.root,'edge-case-hunter','empty',inventory)
        self.assertEqual('BLOCKED',H.evaluate(self.root,value)['execution'])
        self.write('requirements.md','x'*256001)
        with self.assertRaises(H.Invalid):H.prepare(self.root,'edge-case-hunter','large',inventory)

    def test_unknown_fields_rejected(self):
        value=self.prepared('bug-hunter');value['confidence']=1
        with self.assertRaisesRegex(H.Invalid,'candidate fields'):H.evaluate(self.root,value)

    def test_ordering_is_canonical(self):
        value=self.prepared('edge-case-hunter');a=self.candidate(value);b=copy.deepcopy(a);b['signature']='second';b['severity']='low';value['candidates']=[b,a]
        first=H.evaluate(self.root,value);value['candidates']=[a,b];second=H.evaluate(self.root,value)
        self.assertEqual(first,second)

    def cli(self,kind,*args):
        script=HERE.parents[2]/(PREFIX+kind)/'scripts/hunt.py'
        return subprocess.run([sys.executable,str(script),*args,'--root',str(self.root)],capture_output=True,text=True)

    def test_cli_handoff_roundtrip_and_tamper(self):
        for kind in H.KINDS:
            report=self.report(kind);self.write('report.toon',H.encode_toon(report))
            made=self.cli(kind,'handoff','--input','report.toon','--output','handoff.toon')
            self.assertEqual(0,made.returncode,made.stdout)
            checked=self.cli(kind,'verify-handoff','--input','handoff.toon','--report','report.toon')
            self.assertEqual(0,checked.returncode,checked.stdout)
            packet=H.load(self.root,'handoff.toon');packet['authorizes_execution']=True
            self.write('handoff.toon',H.encode_toon(packet))
            self.assertNotEqual(0,self.cli(kind,'verify-handoff','--input','handoff.toon','--report','report.toon').returncode)

    def test_cli_cannot_overwrite_sources_or_producer(self):
        self.write('inventory.toon',H.encode_toon(self.inventory))
        before=(self.root/'app.py').read_bytes()
        attempt=self.cli('bug-hunter','prepare','--input','inventory.toon','--scope','fixture','--output','app.py')
        self.assertNotEqual(0,attempt.returncode)
        self.assertEqual(before,(self.root/'app.py').read_bytes())
        self.write('report.toon',H.encode_toon(self.report('bug-hunter')))
        self.cli('bug-hunter','handoff','--input','report.toon','--output','handoff.toon')
        attempt=self.cli('bug-hunter','verify-handoff','--input','handoff.toon','--report','report.toon','--output','report.toon')
        self.assertNotEqual(0,attempt.returncode)

    def test_cli_protects_reproduction_and_related_evidence(self):
        value,receipt=self.repro_candidate()
        self.write('related.toon',H.encode_toon(self.report('edge-case-hunter')))
        value['related_reports']=['related.toon']
        self.write('candidate.toon',H.encode_toon(value))
        for path in ('repro.toon','repro.log','related.toon'):
            before=(self.root/path).read_bytes()
            attempt=self.cli('bug-hunter','evaluate','--input','candidate.toon','--output',path)
            self.assertNotEqual(0,attempt.returncode,attempt.stdout)
            self.assertEqual(before,(self.root/path).read_bytes())

    def test_nested_report_also_source_protects_receipt(self):
        value,receipt=self.repro_candidate();report=H.evaluate(self.root,value)
        self.write('related.toon',H.encode_toon(report))
        self.inventory.append(dict(path='related.toon',role='design'))
        value=self.prepared('edge-case-hunter');value['related_reports']=['related.toon']
        self.write('candidate.toon',H.encode_toon(value));before=(self.root/'repro.toon').read_bytes()
        result=self.cli('edge-case-hunter','evaluate','--input','candidate.toon','--output','repro.toon')
        self.assertNotEqual(0,result.returncode)
        self.assertEqual(before,(self.root/'repro.toon').read_bytes())

    def test_diamond_related_graph_validates_leaf_once(self):
        leaf=self.report('edge-case-hunter');self.write('leaf.toon',H.encode_toon(leaf))
        for name in ('left','right'):
            value=self.prepared('edge-case-hunter');value['scope']=name;value['related_reports']=['leaf.toon'];value['candidates']=[self.candidate(value)]
            self.write(name+'.toon',H.encode_toon(H.evaluate(self.root,value)))
        value=self.prepared('bug-hunter');value['related_reports']=['left.toon','right.toon']
        original=H.evaluate
        with mock.patch.object(H,'evaluate',wraps=original) as calls:
            original(self.root,value)
        self.assertEqual(3,calls.call_count)

    def test_okf_provenance_survives_hunter_lifecycle(self):
        from ai_sdlc_okf import render_concept, concept_metadata
        original=render_concept((self.root/'requirements.md').read_text(),profile_key='requirements.md',generated_at='2026-09-08T00:00:00Z')
        self.write('requirements.md',original)
        before=concept_metadata(original)
        self.test_cross_hunter_linked_lifecycle()
        self.assertEqual(original,(self.root/'requirements.md').read_text())
        self.assertEqual(before,concept_metadata((self.root/'requirements.md').read_text()))

    def test_existing_quality_lens_finding_contract(self):
        path=HERE.parents[2]/(PREFIX+'quality-lenses')/'scripts/quality_lens_report.py'
        if not path.is_file():self.skipTest('Loop consumes shared finding fields without the optional quality-lens skill')
        import importlib.util
        spec=importlib.util.spec_from_file_location('hunter_lens_compatibility',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for kind in H.KINDS:
            findings=self.report(kind)['findings']
            self.assertEqual([],module.validate_findings(findings,[H.LENSES[kind]],module.load_registry()))

    def test_wrapper_owns_hunter_kind(self):
        self.write('inventory.toon',H.encode_toon(self.inventory))
        attempt=self.cli('bug-hunter','prepare','--input','inventory.toon','--scope','fixture','--hunter','edge-case-hunter')
        self.assertNotEqual(0,attempt.returncode)

    def test_related_report_recomputed_not_only_hashed(self):
        report=self.report('edge-case-hunter');report['findings'][0]['validation_status']='CONFIRMED'
        report['fingerprint']=H.digest({k:v for k,v in report.items() if k!='fingerprint'})
        self.write('edge.toon',H.encode_toon(report))
        value=self.prepared('bug-hunter');value['related_reports']=['edge.toon']
        with self.assertRaisesRegex(H.Invalid,'evaluation drift'):H.evaluate(self.root,value)

if __name__=='__main__':unittest.main()
