# Authorize commit

## Entry

Current verification passed and the user requested a commit.

## Procedure

Use `ai-sdlc-commit-prep` to establish the exact boundary and `ai-sdlc-conventional-commit` to validate the message. Show the verified fingerprint and exact commit boundary. After separate explicit approval, run `approve --action commit`. Never infer approval from Implement.

## Exit

Proceed only with a matching current receipt.
