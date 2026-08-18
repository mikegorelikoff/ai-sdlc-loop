# Artifact

## Entry

Start only after the QA boundary and required scenarios are known.

## Procedure

Use `scripts/qa_plan.py` to emit canonical TOON. Pass each acceptance scenario as `ID|actor|setup|action|expected|evidence|risk`. Record validation as executed, planned, failed, or skipped; never turn planned work into passing evidence.

## Exit

Produce one `ai-sdlc-loop-qa/v1` artifact on stdout or at an approved project-relative `.toon` path.
