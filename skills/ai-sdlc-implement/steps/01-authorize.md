# Authorize implementation

## Entry

A current `spec.toon` fingerprint has been shown to the user.

## Procedure

Use `ai-sdlc-approvals-sandbox` to classify any required command authority. After explicit approval, run `approve --action implement`, followed by `implement-check`. Missing, rejected, stale, or mismatched authority blocks mutation.

## Exit

Proceed only after the runtime prints `implement eligible` for the current fingerprint.
