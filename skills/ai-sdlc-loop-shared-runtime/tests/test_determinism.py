"""Reproducibility, lossless state and failure-atomicity regression checks."""
from __future__ import annotations
import copy
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve();sys.path.insert(0,str(HERE.parents[1]/'scripts'))
import ai_sdlc_toon as toon
import ai_sdlc_safe_io as io
import ai_sdlc_state_machine as state

class DeterminismTests(unittest.TestCase):
    def test_control_characters_are_lossless_single_line_scalars(self):
        for char in ('\x00','\x0b','\x1c','\x85','\u2028','\u2029'):
            value={'text':'before'+char+'after'}
            encoded=toon.encode_toon(value)
            self.assertEqual(len(encoded.splitlines()),1,repr(encoded))
            self.assertNotIn(char,encoded)
            if hasattr(toon,'decode_toon'):self.assertEqual(toon.decode_toon(encoded),value)

    def test_ambiguous_mapping_keys_are_rejected_before_output(self):
        for value in ({1:'numeric','1':'text'},{False:'boolean'},{'nested':{2:'numeric'}}):
            with self.assertRaises((TypeError,ValueError)):toon.encode_toon(value)

    def test_equivalent_mapping_insertion_orders_have_equal_bytes(self):
        self.assertEqual(toon.encode_toon({'b':[{'y':2,'x':1}],'a':'x'}),toon.encode_toon({'a':'x','b':[{'x':1,'y':2}]}))

    def test_state_round_trip_retains_reason_and_quoted_fields(self):
        value=state.initial_state('demo-feature','refinement')
        value['skips']=[{'stage':'discovery','reason':'One, two\n"quoted" \\ path','decision_ref':'DEC-001','flow_mode':'quick'}]
        self.assertEqual(state.from_toon(state.to_toon(value)),value)

    def test_duplicate_stage_identity_and_unknown_status_are_rejected(self):
        for mutate in (lambda v:v['stages'].append(copy.deepcopy(v['stages'][0])),lambda v:v['stages'][0].update(status='CONFIDENT')):
            value=state.initial_state('demo-feature','refinement');mutate(value)
            with self.assertRaises(ValueError):state.from_toon(state.to_toon(value))

    def test_blocked_stage_cannot_be_begun_without_resolution(self):
        value=state.initial_state('demo-feature','refinement');value['stages'][0]['status']='blocked';before=copy.deepcopy(value)
        errors,_=state.begin_stage(value,'ai-sdlc-working-backwards-discovery','full')
        self.assertTrue(errors);self.assertEqual(value,before)

    def test_same_content_write_is_a_safe_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'artifact.toon';io.atomic_write_text(root,p,'value: точный\n')
            os.utime(p,ns=(1_600_000_000_000_000_000,1_600_000_000_000_000_000));before=p.stat().st_mtime_ns
            io.atomic_write_text(root,p,'value: точный\n')
            self.assertEqual(p.stat().st_mtime_ns,before)
            self.assertEqual(p.read_bytes(),'value: точный\n'.encode('utf-8'))

    def test_failed_replace_keeps_valid_output_and_cleans_temporary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'artifact.toon';p.write_bytes(b'old\n')
            with patch.object(io.os,'replace',side_effect=OSError('injected replace failure')):
                with self.assertRaises(OSError):io.atomic_write_text(root,p,'new\n')
            self.assertEqual(p.read_bytes(),b'old\n');self.assertEqual(list(root.iterdir()),[p])

class StateInputTests(unittest.TestCase):
    def test_injected_observation_date_and_repeated_begin(self):
        from datetime import date
        observed = date(2026, 1, 2)
        value = state.initial_state('demo', 'refinement', observed_on=observed)
        self.assertEqual(value['updated_at'], '2026-01-02')
        args = ('ai-sdlc-working-backwards-discovery', 'quick')
        self.assertFalse(state.begin_stage(value, *args, assumption='explicit assumption', observed_on=observed)[0])
        first = copy.deepcopy(value)
        self.assertFalse(state.begin_stage(value, *args, assumption='explicit assumption', observed_on=observed)[0])
        self.assertEqual(value, first)

    def test_invalid_mode_does_not_mutate_state(self):
        value = state.initial_state('demo', 'refinement'); before = copy.deepcopy(value)
        errors, _ = state.begin_stage(value, 'ai-sdlc-working-backwards-discovery', 'automatic')
        self.assertTrue(errors); self.assertEqual(value, before)

    def test_unknown_fields_are_not_silently_discarded(self):
        value = state.initial_state('demo', 'refinement'); value['unexpected'] = 'retain me'
        with self.assertRaises(ValueError): state.to_toon(value)

class EnvironmentTests(unittest.TestCase):
    def test_hash_seed_and_working_directory_do_not_change_encoding(self):
        import subprocess
        code = "import sys;sys.path.insert(0,sys.argv[1]);from ai_sdlc_toon import encode_toon;print(encode_toon({k:k for k in {'gamma','alpha','beta'}}),end='')"
        outputs = []
        with tempfile.TemporaryDirectory() as tmp:
            for seed in ('0', '1', '12345'):
                env = dict(os.environ, PYTHONHASHSEED=seed)
                result = subprocess.run([sys.executable, '-c', code, str(HERE.parents[1]/'scripts')], cwd=tmp, env=env, capture_output=True, check=True)
                outputs.append(result.stdout)
        self.assertEqual(len(set(outputs)), 1)

    def test_every_skill_links_to_an_existing_owning_helper(self):
        import ast, re
        skills_root = HERE.parents[2]
        skills = sorted(skills_root.glob('*/SKILL.md'))
        self.assertTrue(skills)
        for path in skills:
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding='utf-8')
                self.assertEqual(text.count('## Deterministic Execution Contract'), 1)
                block = text.split('## Deterministic Execution Contract', 1)[1].split('\n## ', 1)[0]
                match = re.search(r'\[the owning Python entry point\]\(([^)]+)\)', block)
                self.assertIsNotNone(match)
                helper = (path.parent / match.group(1)).resolve()
                self.assertTrue(helper.is_relative_to(skills_root.resolve()))
                ast.parse(helper.read_text(encoding='utf-8'))
                self.assertIn('- D:', block); self.assertIn('- S:', block); self.assertIn('- H:', block)

class ArtifactRefreshTests(unittest.TestCase):
    def test_native_metadata_refresh_is_stable_and_keeps_provenance(self):
        import ai_sdlc_artifact_helper as artifacts
        import ai_sdlc_okf as okf
        fields = dict(feature='demo', artifact_name='requirements.md', artifact_path='specs/demo/requirements.md', workspace='implementation', skill_name='ai-sdlc-sdd', flow_mode='quick', decision_log_path='specs/demo/decision-log.md', state_file_path='specs/demo/_ai_sdlc/state.toon', state_args=None, status='draft')
        with patch.object(okf, 'utc_now', return_value='2026-09-08T00:00:00Z'):
            original = '\n'.join(artifacts.artifact_metadata_lines(**fields)) + '\n\n# Requirements\n\nKeep source evidence.\n'
        original = original.replace('  at: "2026-09-08T00:00:00Z"', '  at: "2026-09-08T00:00:00Z"\n  sources:\n    - "request.md"')
        with patch.object(okf, 'utc_now', return_value='2026-09-09T00:00:00Z'):
            refreshed = artifacts.refreshed_artifact_metadata(text=original, prior_text=original, **fields)
            self.assertEqual(refreshed, original)
            changed = artifacts.refreshed_artifact_metadata(text=original.replace('Keep source evidence.', 'Change behavior.'), prior_text=original, **fields)
            self.assertIn('2026-09-09T00:00:00Z', changed)
            self.assertIn('request.md', changed)

if __name__=='__main__':unittest.main()
