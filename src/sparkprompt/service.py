"""Framework-independent SparkPrompt use cases."""

from dataclasses import dataclass

from sparkprompt.prompts import (
    build_evaluation_prompt,
    build_problem_statement_prompt,
    build_refinement_prompt,
)
from sparkprompt.providers import TextProvider

MAX_DOMAIN_CHARACTERS = 200
MAX_SKILLS_CHARACTERS = 1_000
MAX_PROMPT_CHARACTERS = 8_000
MAX_EXERCISE_CHARACTERS = 8_000


def _bounded(value: str, *, label: str, limit: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label} is required.")
    if len(normalized) > limit:
        raise ValueError(f"{label} exceeds the {limit:,}-character limit.")
    return normalized


@dataclass(frozen=True)
class EvaluationResult:
    feedback: str
    refined_prompt: str


class PromptService:
    def __init__(self, provider: TextProvider) -> None:
        self._provider = provider

    def generate_problem_statement(self, domain: str, skills: str) -> str:
        safe_domain = _bounded(domain, label="Domain", limit=MAX_DOMAIN_CHARACTERS)
        safe_skills = _bounded(skills, label="Skills", limit=MAX_SKILLS_CHARACTERS)
        return self._provider.generate(build_problem_statement_prompt(safe_domain, safe_skills))

    def evaluate_and_refine(
        self,
        user_prompt: str,
        problem_statement: str,
    ) -> EvaluationResult:
        safe_prompt = _bounded(user_prompt, label="Learner prompt", limit=MAX_PROMPT_CHARACTERS)
        safe_exercise = _bounded(
            problem_statement,
            label="Problem statement",
            limit=MAX_EXERCISE_CHARACTERS,
        )
        feedback = self._provider.generate(build_evaluation_prompt(safe_prompt, safe_exercise))
        refined_prompt = self._provider.generate(
            build_refinement_prompt(safe_prompt, safe_exercise, feedback)
        )
        return EvaluationResult(feedback=feedback, refined_prompt=refined_prompt)
