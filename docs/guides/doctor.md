# Guide: diagnose an installation

## Goal

Explain installation health or package drift without modifying the project.

## When to use it

Use Doctor after verification failure, local skill edits, missing runtime files, or before a package upgrade.

## Prerequisites

Know the installed profile and custom skill root when using `agent-project`.

## Procedure

Run the installed `doctor.py check` command with the project root and profile. For an upgrade preview, run `upgrade-plan` with a trusted local package checkout.

## Verify

The report uses `ai-sdlc-loop-doctor-report/v1`. Every failure includes remediation. Upgrade plans use `ai-sdlc-loop-upgrade-plan/v1` and report `apply_authorized: false`.

## Troubleshooting

An unreadable or missing install record requires review before reinstalling. Digest drift may represent valuable local edits; preserve it before any approved replacement.

## Next step

Request a separate approval for any repair or upgrade action recommended by Doctor.
