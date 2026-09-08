# Diagnose

## Entry

Installation context is available.

## Procedure

For framework health, follow [the framework diagnostic contract](../references/framework-contract.md) and run `scripts/doctor.py framework --root <source-root> --mode quick`. Escalate to standard/deep only for the requested diagnostic scope.

Run deterministic read-only checks or compare the installation with a local candidate package.

## Exit

A canonical report or non-authorizing upgrade plan is emitted.
