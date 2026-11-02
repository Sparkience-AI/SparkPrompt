"""Framework-independent SparkPrompt use cases."""

from dataclasses import dataclass

from sparkprompt.prompts import (
    build_evaluation_prompt,
    build_problem_statement_prompt,
    build_refinement_prompt,
)
from sparkprompt.providers import TextProvider


@dataclass(frozen=True)
class EvaluationResult:
    feedback: str
    refined_prompt: str


class PromptService:
    def __init__(self, provider: TextProvider) -> None:
        self._provider = provider

    def generate_problem_statement(self, domain: str, skills: str) -> str:
        return self._provider.generate(build_problem_statement_prompt(domain, skills))

    def evaluate_and_refine(
        self,
        user_prompt: str,
        problem_statement: str,
    ) -> EvaluationResult:
        feedback = self._provider.generate(build_evaluation_prompt(user_prompt, problem_statement))
        refined_prompt = self._provider.generate(
            build_refinement_prompt(user_prompt, problem_statement, feedback)
        )
        return EvaluationResult(feedback=feedback, refined_prompt=refined_prompt)
