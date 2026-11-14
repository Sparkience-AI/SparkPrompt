# Release checklist

- [ ] Lockfile, formatter, lint, strict typing, unit/security/skill tests, docs/GEO, and Python 3.11–3.13 package smoke checks pass.
- [ ] Gemini, OpenAI Responses with `store=False`, and Anthropic fake-client contracts pass with time/output limits and sanitized UI errors.
- [ ] Skill positive, negative, missing-input, secret, injection, comparison, and consequential-action cases are reviewed.
- [ ] Clean environment installs the wheel and a source checkout launches Streamlit.
- [ ] Keyboard, screen-reader labels, focus order, contrast, zoom, and narrow viewport checks are recorded.
- [ ] Performance envelope and provider-call count are unchanged or an intentional change is documented.
- [ ] The manual `Release evidence` workflow passes for version `0.1.0` and retains checksums, an artifact-installed CycloneDX SBOM, a release manifest, and GitHub provenance/SBOM attestations for the exact source commit.
- [ ] Release notes state formative-scoring, provider-retention, hosted-demo, privacy, and rollback limitations.
- [ ] Rollback is rehearsed by reinstalling the previous wheel and lockfile.

No Windows installer, executable bundler, signing certificate, or store package is part of the release.
