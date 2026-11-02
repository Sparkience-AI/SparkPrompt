# SparkPrompt evaluation rubric

Use the smallest rubric that fits the request. The three core criteria are:

- **Relevance:** the prompt targets the stated objective and audience without unrelated work.
- **Clarity:** the task, context, terminology, and requested output are understandable.
- **Completeness:** necessary inputs, constraints, success conditions, and edge cases are present.

When tools, data, or side effects are involved, also assess:

- **Executability:** named tools and inputs are available, and completion can be verified.
- **Safety and data handling:** authority is explicit; sensitive data and destructive actions have appropriate boundaries.

## Formative scoring

If the user asks for a score, use a 0–10 scale and explain the main reason:

- **0–3:** the objective or required context is missing.
- **4–6:** usable, but important ambiguity or constraints remain.
- **7–8:** clear and practical with minor gaps.
- **9–10:** unusually precise for the stated objective; no score guarantees model performance.

Do not reward unnecessary length, role-play framing, fabricated context, or rigid formatting that does not improve the requested outcome.
