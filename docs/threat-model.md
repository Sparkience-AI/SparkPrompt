# Threat model

SparkPrompt treats learner prompts, exercises, feedback, model output, and skill inputs as untrusted text.

| Threat | Enforced control | Residual risk |
|---|---|---|
| Prompt injection in learner text | Delimited data prompts and skill rules prohibit embedded overrides | A provider can still misunderstand adversarial text |
| Credential disclosure | Password widgets, session-only direct clients, no environment mutation, skill placeholders | Provider and hosting memory remain in the trust boundary |
| Unapproved cloud transmission | Provider-specific consent gates all requests; provider/model changes clear generated state | Users must understand their provider's terms |
| Runaway input/output cost | Input character, output-token, response-character, and timeout limits | Provider pricing and quotas vary by account |
| Destructive prompt execution | Skill separates refinement from execution and requires normal fresh authorization | A user can separately authorize a consequential workflow |
| Misleading scores | Scores are explicitly formative and rubric-based | Model feedback remains subjective and fallible |

The agent skill never needs a provider API key and must not inspect the environment for one. The Streamlit application sends only after explicit consent and cannot execute the learner's prompt.
