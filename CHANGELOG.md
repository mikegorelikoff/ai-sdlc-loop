# Changelog

## v0.4.0 - 2026-09-08

### Changed

- Give all 21 Loop skills individual table-first chat contracts, domain-specific
  result/failure/clarification tables, compact evidence and owned next actions.
  Keep native artifacts and lifecycle authority unchanged.
- Add bounded deterministic chat rendering and structural evaluation, eight
  captured simulation scenarios per skill, negative tests and semantic review.
  Simulations are explicitly distinguished from live model evaluations.
- Include local chat contracts in step context and graph fingerprints; fix TOON
  decoding of quoted content containing named-list headers without weakening hashes.


## 0.3.0 - 2026-09-08

- Added read-only deterministic selection of compact Loop graphs with cycle,
  dependency, missing-source and inconsistent-completion rejection.
- Validate all 21 skill graphs; include shared execution references in semantic
  context and graph fingerprints. Consolidate input/recovery rules and remove
  mandatory Harness lifecycle assumptions from Loop preflight.
- Reject source drift during verification and stale or invalid evidence before
  commit approval. Expose read-only `evidence-check`; only Commit creates commits.
- Match routing keywords at word boundaries and prioritize requirements
  discovery, requirements review and engineering quality-gate requests.


### Added

- Add `ai-sdlc-loop-requirements-discovery` for raw feature/task analysis,
  business alternatives grounded in precedents, and actionable stakeholder
  questions. The optional assistant expands the current source inventory to
  21 directories without changing the required Loop stage graph.
- Back discovery with deterministic source preparation, draft scaffolding,
  typed validation, canonical TOON finalization and freshness checks. Include
  malformed-input, repeatability, safe-write and installed-helper coverage.
- Add `ai-sdlc-loop-flow` with read-only Explore and fingerprinted, non-authorizing Apply.
- Add `ai-sdlc-loop-doctor` with read-only installation diagnostics and upgrade planning.
- Expand the product documentation into source-backed Start here, How it works, Guides, Reference, and Project paths with strict validation.
- Lock documentation dependencies with hashes for reproducible Python 3.9+ builds.
- Add `ai-sdlc-loop-engineering-quality-gate` as a mandatory stage between
  Implement and Verify, with bounded repository-pattern discovery, typed
  adversarial findings, safe localized High and Medium fixes, deterministic
  verification reruns, and fingerprinted TOON readiness reports.
- Expand every installation profile to the exact twenty-member package and
  fail Verify closed when quality evidence is missing, non-ready, invalid, or
  stale for the current change.
- Add a six-section MkDocs Material site, strict documentation build, and
  GitHub Pages deployment workflow.
- Initial one-skill Specify → Implement → Verify workflow.
- Portable three-profile installer and offline verification.
- Fingerprint-bound Implement and commit approvals.
- Deterministic redacted evidence and Harness-compatible promotion.

## 0.2.0 - 2026-08-18

- Released guided Flow, installation Doctor, and the expanded documentation site.

## 0.1.1 - 2026-08-17

- Replace the premature monolithic skill with five stage-oriented skills and one shared runtime.
- Add canonical `steps/manifest.toon` graphs and bounded step documents.
- Replace JSON durable artifacts and install records with canonical TOON.
- Add eight self-contained Harness delivery-control skills for branching, test design, validation, review, security, approval planning, and commit quality.
- Add a compact QA skill for risk-based acceptance, regression, manual checks, signoff, and canonical TOON QA plans.
- Add compact requirements-gap and release-readiness skills with typed TOON review artifacts.
- Force shared helper output to UTF-8 and regression-test Windows `cp1252` compatibility.
- Namespace every installed skill as `ai-sdlc-loop-{slug}` and expose the root router as `ai-sdlc-loop-orchestrate`.

All notable changes follow Keep a Changelog. This project uses semantic versioning.
