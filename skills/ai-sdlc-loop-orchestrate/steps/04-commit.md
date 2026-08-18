# Commit route

## Entry

Current verification passed and the user requested a commit.

## Procedure

Load `ai-sdlc-loop-commit`; it must obtain and validate separate approval for the verified fingerprint.

## Exit

Return the created commit identity. Push, tag, release, and PR actions remain out of scope.
