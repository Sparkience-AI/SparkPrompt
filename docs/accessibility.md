# Accessibility audit

The Streamlit interface uses labeled native controls for provider, model, key, consent, domain, skills, and learner prompt. Provider keys use password input. Errors are presented as text and do not rely only on color.

Before a release, manually verify keyboard-only navigation, visible focus, screen-reader labels, heading order, zoom to 200%, narrow viewport behavior, contrast, and that provider/consent state changes are announced in nearby text. Record browser, operating system, assistive technology, and unresolved findings in the release notes. Automated source tests supplement but do not replace this manual check.
