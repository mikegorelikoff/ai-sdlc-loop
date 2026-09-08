"""Mutation corpus for the read-only framework doctor; no model wording goldens."""
import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('framework_doctor_test_subject', SKILL / 'scripts/framework.py')
D = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = D
SPEC.loader.exec_module(D)

class FrameworkDoctorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / 'skills' / SKILL.name
        shutil.copytree(SKILL, self.skill, ignore=shutil.ignore_patterns('__pycache__'))
        shared = SKILL.parent / (D.PREFIX + 'shared-runtime')
        shutil.copytree(shared, self.root/'skills'/shared.name, ignore=shutil.ignore_patterns('__pycache__'))
        names=[SKILL.name, shared.name]
        if D.PREFIX == 'ai-sdlc-loop-':
            (self.root / 'install.py').write_text('SKILLS = ' + repr(tuple(names)) + '\n', encoding='utf-8')
        else:
            directory = self.root / 'modules/core'
            directory.mkdir(parents=True)
            (directory / 'module.toon').write_text(D.encode_toon(dict(schema='ai-sdlc-module/v1',skills=[dict(name=name,path='skills/'+name) for name in names])), encoding='utf-8')

    def diagnose(self, **kwargs):
        return D.diagnose(self.root, **kwargs)

    def finding(self, report, code):
        values = [c for c in report['findings'] if c['code'] == code]
        self.assertTrue(values, code)
        return values[0]

    def test_healthy_read_only_and_repeatable(self):
        def snapshot():
            return {p.relative_to(self.root).as_posix():p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        before = snapshot()
        first, second = self.diagnose(), self.diagnose()
        self.assertEqual('HEALTHY', first['health'])
        self.assertEqual(D.encode_toon(first), D.encode_toon(second))
        self.assertEqual(before, snapshot())
        self.assertEqual(D.decode_toon(D.encode_toon(first)), first)

    def test_missing_skill_blocks_dependents(self):
        (self.skill / 'SKILL.md').unlink()
        report = self.diagnose(mode='standard')
        root = self.finding(report, 'MISSING_SKILL')
        children = [c for c in report['checks'] if root['id'] in c['blocked_by']]
        self.assertTrue(children)
        self.assertTrue(all(c['status'] == 'BLOCKED' for c in children))
        self.assertFalse(any(c['code'] == 'EXECUTION_EVAL_FAILED' for c in report['findings']))

    def test_hunter_family_contract_and_schema_drift(self):
        names=[SKILL.name,D.PREFIX+'shared-runtime']
        for kind in ('edge-case-hunter','blind-case-hunter','bug-hunter'):
            name=D.PREFIX+kind;names.append(name)
            shutil.copytree(SKILL.parent/name,self.root/'skills'/name,ignore=shutil.ignore_patterns('__pycache__'))
        if D.PREFIX=='ai-sdlc-loop-':
            (self.root/'install.py').write_text('SKILLS = '+repr(tuple(names))+'\n',encoding='utf-8')
        else:
            (self.root/'modules/core/module.toon').write_text(D.encode_toon(dict(schema='ai-sdlc-module/v1',skills=[dict(name=n,path='skills/'+n) for n in names])),encoding='utf-8')
        report=self.diagnose(mode='standard')
        self.assertEqual('PASS',next(c['status'] for c in report['checks'] if c['check_id']=='DOC-HUNTER-002'))
        path=self.root/'skills'/(D.PREFIX+'shared-runtime')/'references/hunters.schema.toon'
        value=D.decode_toon(path.read_text());value['unexpected']='drift';path.write_text(D.encode_toon(value),encoding='utf-8')
        self.finding(self.diagnose(),'HUNTER_CONTRACT_INVALID')

    def test_packaged_inventory_drift(self):
        if D.PREFIX!='ai-sdlc-':self.skipTest('Backbone packaged default inventory contract')
        (self.root/'config').mkdir()
        names=sorted([SKILL.name,D.PREFIX+'shared-runtime'])
        (self.root/'config/ai-sdlc-managed-skills.txt').write_text('\n'.join(names)+'\n',encoding='utf-8')
        report=self.diagnose()
        self.assertTrue(any(f['code']=='INVENTORY_DRIFT' and f['component']=='packaged-inventory' for f in report['findings']))

    def test_invalid_python(self):
        (self.skill / 'scripts/broken.py').write_text('def broken(:\n', encoding='utf-8')
        finding = self.finding(self.diagnose(), 'PYTHON_SYNTAX_FAILED')
        self.assertEqual(('PYTHON','HIGH','PYTHON'), (finding['layer'],finding['severity'],finding['repair_route']))

    def test_malformed_toon_and_no_cascade(self):
        (self.skill / 'references/broken.toon').write_text('rows[2]: a\n', encoding='utf-8')
        result = self.diagnose()
        self.finding(result, 'TOON_PARSE_FAILED')
        self.assertFalse(any(c['code']=='TOON_ROUNDTRIP_FAILED' for c in result['findings']))

    def test_roundtrip_mutation(self):
        with patch.object(D, 'decode_toon', return_value={'changed':True}):
            with self.assertRaises(ValueError): D.roundtrip({'original':True})

    def test_chat_schema_drift(self):
        path = self.skill / 'references/chat-output.toon'
        value = D.decode_toon(path.read_text(encoding='utf-8'))
        value['skill']='wrong-owner'
        path.write_text(D.encode_toon(value),encoding='utf-8')
        self.finding(self.diagnose(), 'CHAT_CONTRACT_INVALID')

    def test_missing_step_and_route(self):
        path=self.skill / 'steps/manifest.toon'
        value=D.decode_toon(path.read_text(encoding='utf-8'))
        value['steps'][0]['path']='steps/missing.md'
        path.write_text(D.encode_toon(value),encoding='utf-8')
        self.finding(self.diagnose(), 'STEP_GRAPH_INVALID')

    def test_unreachable_node(self):
        path=self.skill / 'steps/manifest.toon'
        value=D.decode_toon(path.read_text(encoding='utf-8'))
        value['steps'][0]['depends_on']=['handoff']
        path.write_text(D.encode_toon(value),encoding='utf-8')
        self.finding(self.diagnose(), 'STEP_GRAPH_INVALID')

    def test_missing_eval(self):
        (self.skill / 'tests/fixtures/chat-scenarios.toon').unlink()
        report=self.diagnose()
        finding=self.finding(report,'CHAT_EVAL_MISSING')
        self.assertEqual('MEDIUM',finding['severity'])
        self.assertEqual('DEGRADED',report['health'])

    def test_no_arbitrary_imports(self):
        sentinel=self.root/'should-not-exist'
        (self.skill/'scripts/malicious.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').touch()\n',encoding='utf-8')
        self.diagnose()
        self.assertFalse(sentinel.exists())

    def test_unsafe_path(self):
        with self.assertRaises(ValueError): D.regular(self.root,'../outside')
        with self.assertRaises(ValueError): D.regular(self.root,str(self.skill/'SKILL.md'))

    def test_optional_and_invalid_fixtures_not_production_errors(self):
        (self.skill/'tests/fixtures/invalid.toon').write_text('x[3]: y\n',encoding='utf-8')
        self.assertEqual('HEALTHY',self.diagnose()['health'])

    def test_invalid_okf(self):
        bundle=self.root/'bundle'
        bundle.mkdir()
        report=self.diagnose(artifacts=(('okf','bundle'),))
        finding=self.finding(report,'OKF_INVALID')
        self.assertEqual('OKF',finding['repair_route'])

    def test_invalid_state(self):
        (self.root/'state.toon').write_text('status: imaginary\n',encoding='utf-8')
        self.finding(self.diagnose(artifacts=(('state','state.toon'),)), 'STATE_INVALID')

    def test_invalid_root_is_blocked_not_healthy(self):
        report=D.diagnose(self.root/'absent')
        self.assertEqual('BLOCKED',report['health'])
        self.assertEqual('PASS',report['execution'])

    def test_stable_ids_ignore_evidence(self):
        path=self.skill/'scripts/broken.py'
        path.write_text('def a(:\n',encoding='utf-8')
        first=self.finding(self.diagnose(),'PYTHON_SYNTAX_FAILED')
        path.write_text('def b(:\n',encoding='utf-8')
        second=self.finding(self.diagnose(),'PYTHON_SYNTAX_FAILED')
        self.assertEqual(first['id'],second['id'])

    def test_report_tampering_is_rejected(self):
        report=self.diagnose()
        report['checks'][0]['id']='random'
        with self.assertRaises(ValueError): D.validate_report(report)

    def test_transition_simulation(self):
        self.assertIn('rejected',D.state_simulation())

    def test_table_first_escapes_hostile_components(self):
        report=self.diagnose(target='unknown|<script>')
        text=D.markdown(report)
        self.assertTrue(text.startswith('|'))
        self.assertNotIn('<script>',text)
        self.assertIn('&#124;',text)

    def test_missing_local_import(self):
        (self.skill/'scripts/imports.py').write_text('from ai_sdlc_nonexistent import check\n',encoding='utf-8')
        finding=self.finding(self.diagnose(),'LOCAL_IMPORT_MISSING')
        self.assertEqual('PYTHON',finding['repair_route'])

    def test_missing_referenced_script(self):
        path=self.skill/'SKILL.md'
        path.write_text(path.read_text(encoding='utf-8')+'\n[helper](scripts/missing.py)\n',encoding='utf-8')
        self.finding(self.diagnose(),'MISSING_SCRIPT')

    def test_deep_repeats_isolated_native_evals(self):
        report=self.diagnose(mode='deep')
        self.assertEqual('HEALTHY',report['health'],[(c['code'],c['evidence']) for c in report['findings']])
        self.assertEqual('PASS',next(c['status'] for c in report['checks'] if c['check_id']=='DOC-DET-001'))

    def test_failed_eval_is_not_missing_dependency(self):
        path=self.skill/'tests/fixtures/chat-scenarios.toon'
        value=D.decode_toon(path.read_text(encoding='utf-8'))
        value['scenarios'][0]['required_facts']=['fact-not-produced']
        path.write_text(D.encode_toon(value),encoding='utf-8')
        report=self.diagnose(mode='standard')
        self.assertEqual('FAIL',self.finding(report,'CHAT_EVAL_FAILED')['status'])

    def test_health_and_repair_policy_cannot_be_overridden(self):
        report=self.diagnose()
        report['health']='UNHEALTHY'
        with self.assertRaises(ValueError):D.validate_report(report)

    def test_decomposition_invalid_handoff(self):
        (self.root/'packet.toon').write_text('branch: imaginary\n',encoding='utf-8')
        (self.root/'report.toon').write_text('candidate: invalid\n',encoding='utf-8')
        self.finding(self.diagnose(artifacts=(('handoff','packet.toon@report.toon'),)), 'HANDOFF_INVALID')

    def test_okf_valid_bundle(self):
        bundle=self.root/'bundle';bundle.mkdir()
        (bundle/'index.md').write_text('---\nokf_version: "0.2"\n---\n# Bundle\n',encoding='utf-8')
        from ai_sdlc_okf import render_concept
        (bundle/'requirements.md').write_text(render_concept('# Requirements\n',profile_key='requirements.md',generated_at='2000-01-01'),encoding='utf-8')
        report=self.diagnose(artifacts=(('okf','bundle'),))
        self.assertEqual('HEALTHY',report['health'])

    def test_source_bytes_identical_between_products(self):
        if D.PREFIX == 'ai-sdlc-loop-':
            peer=SKILL.parents[3]/'skills/ai-sdlc-doctor/scripts/framework.py'
        else:
            peer=SKILL.parents[1]/'products/ai-sdlc-loop/skills/ai-sdlc-loop-doctor/scripts/framework.py'
        if not peer.is_file():self.skipTest('peer product absent in standalone checkout')
        self.assertEqual((SKILL/'scripts/framework.py').read_bytes(),peer.read_bytes())

    def test_lifecycle_mutation_flags_are_rejected(self):
        import io
        from contextlib import redirect_stdout
        for flag in ('--begin-state','--complete-state','--state-check'):
            output=io.StringIO()
            with redirect_stdout(output):
                code=D.main(['--root',str(self.root),flag])
            self.assertEqual(1,code)
            self.assertEqual('FAIL',D.decode_toon(output.getvalue())['execution'])

    def test_invalid_loop_state_is_terminal_failure(self):
        if D.PREFIX != 'ai-sdlc-loop-':self.skipTest('Loop-specific adapter')
        report=self.diagnose(artifacts=(('loop-state','missing-feature'),))
        self.assertEqual('FAIL',self.finding(report,'STATE_INVALID')['status'])

    def test_toon_unicode_and_delimiters_roundtrip(self):
        self.assertIn('preserved',D.roundtrip({'names':['Привет','a,b','pipe|value','newline\nvalue'], 'nested':{'empty':[], 'enabled':True}}))

if __name__=='__main__': unittest.main()
