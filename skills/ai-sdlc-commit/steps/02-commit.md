# Create commit

## Entry

Commit approval matches unchanged passing evidence.

## Procedure

Run `commit` with a reviewed Conventional Commit message. The runtime stages only verified paths and restores the prior index if commit creation fails.

## Exit

Return exactly one commit SHA. Do not push, tag, publish, release, deploy, or open a PR implicitly.
