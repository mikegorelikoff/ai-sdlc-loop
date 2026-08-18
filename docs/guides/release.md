# Guide: prepare a release

## Goal

Produce a commit-bound release decision with complete validation evidence.

## When to use it

Use this after implementation, QA, review, and security evidence are current.

## Prerequisites

The exact candidate commit is known and every required gate has an owner and evidence.

## Procedure

Run release readiness for the exact commit. Review blockers, residual risks, documentation status, compatibility, and rollback notes. Obtain explicit approval before tag creation, push, or hosted release publication.

## Verify

The release artifact is canonical TOON, binds every gate to the same commit, and cannot report ready while a blocker or incomplete gate remains.

## Troubleshooting

Refresh stale evidence against the candidate commit. Do not waive a failed gate by changing only the summary status.

## Next step

Use the repository release workflow only after the separate external-write approval.
