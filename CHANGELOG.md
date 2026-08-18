# Changelog

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

## [Unreleased]

### Added

- Add `ai-sdlc-loop-flow` with read-only Explore and fingerprinted, non-authorizing Apply.
- Add `ai-sdlc-loop-doctor` with read-only installation diagnostics and upgrade planning.
- Expand the product documentation into source-backed Start here, How it works, Guides, Reference, and Project paths with strict validation.
- Lock documentation dependencies with hashes for reproducible Python 3.9+ builds.
- Add a six-section MkDocs Material site, strict documentation build, and
  GitHub Pages deployment workflow.
- Initial one-skill Specify → Implement → Verify workflow.
- Portable three-profile installer and offline verification.
- Fingerprint-bound Implement and commit approvals.
- Deterministic redacted evidence and Harness-compatible promotion.
