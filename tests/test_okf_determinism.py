"""Portable OKF provenance and reproducibility checks."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/ai-sdlc-loop-shared-runtime/scripts'))
from ai_sdlc_okf import render_concept, render_frontmatter, concept_metadata, concept_profile, migrate_concept_text
class OkfDeterminismTests(unittest.TestCase):
    def test_legacy_date_precision_survives_refresh_and_migration(self):
        original = render_concept('# Requirements\n', profile_key='requirements.md', generated_at='2026-08-03')
        self.assertEqual(concept_metadata(original)['generated_at'], '2026-08-03')
        refreshed = render_concept('# Requirements\n', profile_key='requirements.md', existing_text=original, meaningful_change=False)
        self.assertEqual(concept_metadata(refreshed)['generated_at'], '2026-08-03')
        self.assertEqual(concept_metadata(migrate_concept_text(original, profile_key='requirements.md'))['generated_at'], '2026-08-03')
        with self.assertRaises(ValueError):
            concept_metadata(original.replace('2026-08-03', '2026-02-30'))

    def test_invalid_generation_timestamp_is_rejected(self):
        text = render_concept('# Requirements\n', profile_key='requirements.md', generated_at='2026-09-08T00:00:00Z')
        with self.assertRaises(ValueError):
            concept_metadata(text.replace('2026-09-08T00:00:00Z', 'not-a-date'))

    def test_changed_source_invalidates_verification(self):
        headers = render_frontmatter(profile=concept_profile('requirements.md'), status='stable', generated_by='process:ai-sdlc', generated_at='2026-07-27T00:00:00Z', sources=['old.md'], verified_by='human:reviewer', verified_at='2026-07-27T01:00:00Z', verification_evidence=['test.log'])
        original = '\n'.join(headers) + '\n# Requirements\n'
        result = render_concept('# Requirements\n', profile_key='requirements.md', existing_text=original, sources=['new.md'], meaningful_change=False)
        self.assertNotIn('verified:', result)
        self.assertIn('new.md', result)

    def test_sources_survive_refresh_and_migration(self):
        original=render_concept('# Requirements\n',profile_key='requirements.md',sources=['request.md'])
        self.assertIn('request.md',migrate_concept_text(original,profile_key='requirements.md'))
        self.assertIn('request.md',render_concept('# Requirements\n',profile_key='requirements.md',existing_text=original,meaningful_change=False))

    def test_duplicate_portable_keys_are_rejected(self):
        original=render_concept('# Requirements\n',profile_key='requirements.md')
        for malformed in (original.replace('type:', 'status: "stable"\ntype:',1),original.replace('generated:\n','generated:\n  by: "human:conflict"\n',1)):
            with self.assertRaises(ValueError):concept_metadata(malformed)

    def test_render_detects_content_change_despite_refresh_hint(self):
        metadata=render_frontmatter(profile=concept_profile('requirements.md'),status='stable',generated_by='process:ai-sdlc',generated_at='2026-07-27T00:00:00Z',verified_by='human:reviewer',verified_at='2026-07-27T01:00:00Z',verification_evidence=['test.log'])
        original='\n'.join(metadata)+'\n# Old behavior\n'
        changed=render_concept('# New behavior\n',profile_key='requirements.md',existing_text=original,meaningful_change=False)
        self.assertNotIn('verified:',changed)

    def test_fixed_clock_and_source_permutation_are_reproducible(self):
        options=dict(profile_key='requirements.md',generated_at='2026-09-08T00:00:00Z')
        first=render_concept('# Requirements\n',sources=['b.md','a.md','a.md'],**options)
        second=render_concept('# Requirements\n',sources=['a.md','b.md'],**options)
        self.assertEqual(first,second)
