import pytest

from sparkprompt.service import PromptService


class RecordingProvider:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.prompts = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return next(self.responses)


def test_problem_statement_flow_uses_provider() -> None:
    provider = RecordingProvider(["A generated exercise"])
    service = PromptService(provider)
    assert service.generate_problem_statement("AI", "reasoning") == "A generated exercise"
    assert "Domain: AI" in provider.prompts[0]


@pytest.mark.parametrize(
    ("domain", "skills", "message"),
    [
        ("", "reasoning", "Domain is required"),
        ("AI", "", "Skills is required"),
        ("x" * 201, "a", "200"),
    ],
)
def test_problem_statement_inputs_are_bounded(domain: str, skills: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        PromptService(RecordingProvider([])).generate_problem_statement(domain, skills)


def test_evaluation_inputs_are_bounded_before_provider_call() -> None:
    provider = RecordingProvider([])
    with pytest.raises(ValueError, match="8,000"):
        PromptService(provider).evaluate_and_refine("x" * 8_001, "exercise")
    assert provider.prompts == []


def test_refinement_receives_evaluation_feedback_and_original_prompt() -> None:
    provider = RecordingProvider(["Needs an output format.", "Improved learner prompt"])
    service = PromptService(provider)

    result = service.evaluate_and_refine("Analyze sales", "Write an analysis prompt")

    assert result.feedback == "Needs an output format."
    assert result.refined_prompt == "Improved learner prompt"
    assert len(provider.prompts) == 2
    assert "Analyze sales" in provider.prompts[0]
    assert "Analyze sales" in provider.prompts[1]
    assert "Needs an output format." in provider.prompts[1]
