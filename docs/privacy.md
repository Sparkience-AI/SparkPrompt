# BYOK and privacy notes

SparkPrompt uses bring-your-own-key (BYOK) access to Google Gemini, OpenAI, or Anthropic Claude.

- The selected provider's API key is passed directly to a provider client created for the
  current Streamlit session/rerun.
- SparkPrompt does not intentionally write that key to environment variables, source files, logs,
  or a database.
- The **Clear this provider key** control removes the selected value from the active Streamlit
  session. Closing the browser tab also ends the normal session lifecycle.
- Problem statements, learner prompts, evaluation feedback, and refinements are sent only after
  the user checks the provider-specific transmission confirmation. That provider's API terms and
  data-handling policies apply.
- OpenAI requests explicitly set response storage off. Provider-side safety, abuse-prevention, and
  retention behavior remains governed by the user's provider account and applicable terms.
- The app does not provide durable prompt history. Streamlit still holds active widget/session data
  in server memory for the life of the session.
- Do not submit secrets, personal data, confidential client information, or regulated data.
- Evaluation is AI-assisted educational feedback, not an objective certification of prompt quality.

Production deployments must configure HTTPS, access controls or quotas as appropriate, log
redaction, retention limits, and an incident-reporting path before accepting sensitive use cases.
