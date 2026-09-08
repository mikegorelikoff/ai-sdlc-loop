# Chat output contract registry

Generated from local contracts and executed deterministic simulations. Semantic review is separate; these are not live model runs.

| Skill | Primary table | Secondary table | Failure table | Scenarios | Eval |
| --- | --- | --- | --- | ---: | --- |
| ai-sdlc-loop-approvals-sandbox | Command / Boundary / Escalation / Evidence | Omitted | Blocked command / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-branching | Current branch / Expected branch / Base revision / Worktree / Decision | Omitted | Task scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-code-review | Severity / Location / Finding / Evidence / Required fix | Check / Status / Evidence / Coverage gap | Review diff / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-commit | Commit / Branch / Included scope / Approval / Evidence | Remaining path / Reason / Evidence | Commit approval / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-commit-prep | Path group / Disposition / Reason / Verification / Evidence | Commit / Branch / Task ID / Evidence | Commit scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-conventional-commit | Subject / Specification / Task ID / Validation / Evidence | Omitted | Change summary / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-doctor | Check / Installed state / Expected state / Status / Remediation | Omitted | Installation root / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-engineering-quality-gate | Severity / Location / Finding / Disposition / Verification / Evidence | Gate / Status / Unresolved count / Evidence | Implementation diff / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-flow | Intent / Selected skill / Reason / Authority / Expected artifact | Blocked transition / Gate / Evidence / Required action | User intent / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-implement | File / component / Change / Requirement ID / Verification / Evidence | Check / Status / Evidence | Implementation approval / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-orchestrate | Stage / State / Owning skill / Gate / Evidence | Omitted | Feature scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-qa | Scenario ID / Actor / setup / Action / Expected result / Execution status / Evidence | Regression target / Risk / Execution status / Evidence | Acceptance outcome / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-release-readiness | Release gate / Candidate commit / Status / Evidence / Required action | Residual risk / Owner / Mitigation / Evidence | Candidate commit / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-requirements-discovery | Option ID / Business option / Precedent / Trade-off / Decision status | Question ID / Question / Owner / Evidence method / Decision impact | Raw request / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-requirements-review | Requirement ID / Gap category / Severity / Impact / Evidence / Resolution | Omitted | Requirement package / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-security-testing | Severity / Trust boundary / Finding / Evidence / Remediation | Source / Supported claim / Freshness / Evidence | Trust boundary / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-shared-runtime | Runtime check / Expected / Actual / Status / Evidence | Omitted | Installed helper / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-specify | Requirement ID / Bounded behavior / Allowed path / Acceptance / Evidence | Omitted | Allowed scope / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-test-cases | Test ID / Requirement ID / Setup / trigger / Expected result / Layer / Evidence | Omitted | Acceptance criterion / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-validation | Check / Expected / Actual / Status / Evidence | Omitted | Verification command / Status / Blocker / Evidence / Required action | 8 | PASS |
| ai-sdlc-loop-verify | Check / Expected / Actual / Status / Evidence | Artifact / Freshness / Evidence | Current quality evidence / Status / Blocker / Evidence / Required action | 8 | PASS |
