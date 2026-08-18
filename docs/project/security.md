# Security and privacy

Loop keeps workflow state local, invokes verification commands without a shell, contains project paths, and redacts common secret patterns from persisted evidence. It does not provide cryptographic reviewer identity or organizational authorization.

Flow and Doctor are read-only. Doctor remediation and upgrade plans never self-apply. Source mutation, commands, commits, tags, pushes, releases, and deployments remain subject to the owning skill, host sandbox, repository policy, and explicit user authority.

Report vulnerabilities through the repository [security advisory form](https://github.com/mikegorelikoff/ai-sdlc-loop/security/advisories/new).
