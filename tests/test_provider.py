import os
from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from sparkprompt.providers import (
    PROVIDER_DEFAULTS,
    AnthropicProvider,
    GeminiProvider,
    OpenAIProvider,
    ProviderName,
)


class FakeGeminiModels:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(text="gemini answer")


class FakeGeminiClient:
    def __init__(self, api_key: str, http_options: dict[str, int]) -> None:
        self.api_key = api_key
        self.http_options = http_options
        self.models = FakeGeminiModels()


class FakeOpenAIResponses:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(output_text="openai answer")


class FakeOpenAIClient:
    def __init__(self, api_key: str, timeout: float) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.responses = FakeOpenAIResponses()


@dataclass
class TextBlock:
    type: str
    text: str


class FakeAnthropicMessages:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(content=[TextBlock("text", "claude answer")])


class FakeAnthropicClient:
    def __init__(self, api_key: str, timeout: float) -> None:
        self.api_key = api_key
        self.timeout = timeout
        self.messages = FakeAnthropicMessages()


def test_gemini_uses_an_isolated_key_and_current_model(monkeypatch) -> None:
    created: list[FakeGeminiClient] = []

    def factory(*, api_key, http_options):
        client = FakeGeminiClient(api_key, http_options)
        created.append(client)
        return client

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    provider = GeminiProvider("session-key", client_factory=factory)

    assert provider.generate("practice") == "gemini answer"
    assert created[0].api_key == "session-key"
    assert created[0].http_options == {"timeout": 60_000}
    assert created[0].models.calls == [
        {
            "model": PROVIDER_DEFAULTS[ProviderName.GEMINI].model,
            "contents": "practice",
            "config": {"max_output_tokens": 4_096},
        }
    ]
    assert "GEMINI_API_KEY" not in os.environ


def test_openai_uses_responses_api_without_server_storage(monkeypatch) -> None:
    created: list[FakeOpenAIClient] = []

    def factory(*, api_key, timeout):
        client = FakeOpenAIClient(api_key, timeout)
        created.append(client)
        return client

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider("session-key", client_factory=factory)

    assert provider.generate("evaluate") == "openai answer"
    assert created[0].api_key == "session-key"
    assert created[0].responses.calls == [
        {
            "model": PROVIDER_DEFAULTS[ProviderName.OPENAI].model,
            "input": "evaluate",
            "max_output_tokens": 4_096,
            "store": False,
        }
    ]
    assert "OPENAI_API_KEY" not in os.environ


def test_anthropic_uses_messages_api_with_bounded_output(monkeypatch) -> None:
    created: list[FakeAnthropicClient] = []

    def factory(*, api_key, timeout):
        client = FakeAnthropicClient(api_key, timeout)
        created.append(client)
        return client

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    provider = AnthropicProvider("session-key", client_factory=factory)

    assert provider.generate("refine") == "claude answer"
    assert created[0].api_key == "session-key"
    assert created[0].messages.calls == [
        {
            "model": PROVIDER_DEFAULTS[ProviderName.ANTHROPIC].model,
            "max_tokens": 4_096,
            "messages": [{"role": "user", "content": "refine"}],
        }
    ]
    assert "ANTHROPIC_API_KEY" not in os.environ


@pytest.mark.parametrize(
    ("provider", "message"),
    [
        (GeminiProvider, "Google"),
        (OpenAIProvider, "OpenAI"),
        (AnthropicProvider, "Anthropic"),
    ],
)
def test_providers_reject_blank_keys(provider, message) -> None:
    with pytest.raises(ValueError, match=message):
        provider("   ")


@pytest.mark.parametrize(
    "provider",
    [
        lambda: GeminiProvider("key", max_response_characters=3, client_factory=FakeGeminiClient),
        lambda: OpenAIProvider("key", max_response_characters=3, client_factory=FakeOpenAIClient),
        lambda: AnthropicProvider(
            "key", max_response_characters=3, client_factory=FakeAnthropicClient
        ),
    ],
)
def test_all_providers_bound_response_size(provider) -> None:
    with pytest.raises(RuntimeError, match="application limit"):
        provider().generate("test")
