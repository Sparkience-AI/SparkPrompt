"""Session-owned model-provider adapters used by SparkPrompt."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Protocol, cast


class TextProvider(Protocol):
    """Minimal model capability required by the application service."""

    def generate(self, prompt: str) -> str:
        """Generate text for one application-owned prompt."""


class ProviderName(StrEnum):
    GEMINI = "Google Gemini"
    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic Claude"


@dataclass(frozen=True, slots=True)
class ProviderDefaults:
    model: str
    key_label: str


PROVIDER_DEFAULTS = {
    ProviderName.GEMINI: ProviderDefaults("gemini-3.8-flash", "Google API key"),
    ProviderName.OPENAI: ProviderDefaults("gpt-6-luna", "OpenAI API key"),
    ProviderName.ANTHROPIC: ProviderDefaults("claude-haiku-5-5", "Anthropic API key"),
}

ClientFactory = Callable[..., Any]
DEFAULT_MAX_RESPONSE_CHARACTERS = 32_000
DEFAULT_MAX_OUTPUT_TOKENS = 4_096


def _require_key(api_key: str, provider: str) -> str:
    normalized = api_key.strip()
    if not normalized:
        raise ValueError(f"A {provider} API key is required.")
    return normalized


def _bounded_text(text: Any, limit: int, provider: str) -> str:
    if limit < 1:
        raise ValueError("The response character limit must be positive.")
    normalized = str(text) if text else ""
    if not normalized:
        raise RuntimeError(f"{provider} returned no text output.")
    if len(normalized) > limit:
        raise RuntimeError(f"{provider} returned a response above the application limit.")
    return normalized


class GeminiProvider:
    """Google Gemini adapter with a directly configured, session-owned key."""

    def __init__(
        self,
        api_key: str,
        *,
        model: str = PROVIDER_DEFAULTS[ProviderName.GEMINI].model,
        max_response_characters: int = DEFAULT_MAX_RESPONSE_CHARACTERS,
        max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
        timeout_seconds: float = 60.0,
        client_factory: ClientFactory | None = None,
    ) -> None:
        api_key = _require_key(api_key, "Google")
        if not model.strip():
            raise ValueError("A Gemini model is required.")
        if max_output_tokens < 1 or timeout_seconds <= 0:
            raise ValueError("Provider output and timeout limits must be positive.")
        if client_factory is None:
            from google import genai

            client_factory = genai.Client
        self.model = model.strip()
        self._client = client_factory(
            api_key=api_key,
            http_options={"timeout": int(timeout_seconds * 1_000)},
        )
        self._max_output_tokens = max_output_tokens
        self._max_response_characters = max_response_characters

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={"max_output_tokens": self._max_output_tokens},
        )
        return _bounded_text(
            getattr(response, "text", None), self._max_response_characters, "Gemini"
        )


class OpenAIProvider:
    """OpenAI Responses API adapter with storage disabled for each request."""

    def __init__(
        self,
        api_key: str,
        *,
        model: str = PROVIDER_DEFAULTS[ProviderName.OPENAI].model,
        max_response_characters: int = DEFAULT_MAX_RESPONSE_CHARACTERS,
        max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
        timeout_seconds: float = 60.0,
        client_factory: ClientFactory | None = None,
    ) -> None:
        api_key = _require_key(api_key, "OpenAI")
        if not model.strip():
            raise ValueError("An OpenAI model is required.")
        if max_output_tokens < 1 or timeout_seconds <= 0:
            raise ValueError("Provider output and timeout limits must be positive.")
        if client_factory is None:
            from openai import OpenAI

            client_factory = OpenAI
        self.model = model.strip()
        self._client = client_factory(api_key=api_key, timeout=timeout_seconds)
        self._max_output_tokens = max_output_tokens
        self._max_response_characters = max_response_characters

    def generate(self, prompt: str) -> str:
        response = self._client.responses.create(
            model=self.model,
            input=prompt,
            max_output_tokens=self._max_output_tokens,
            store=False,
        )
        return _bounded_text(
            getattr(response, "output_text", None), self._max_response_characters, "OpenAI"
        )


class AnthropicProvider:
    """Anthropic Messages API adapter with a directly configured key."""

    def __init__(
        self,
        api_key: str,
        *,
        model: str = PROVIDER_DEFAULTS[ProviderName.ANTHROPIC].model,
        max_response_characters: int = DEFAULT_MAX_RESPONSE_CHARACTERS,
        max_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS,
        timeout_seconds: float = 60.0,
        client_factory: ClientFactory | None = None,
    ) -> None:
        api_key = _require_key(api_key, "Anthropic")
        if not model.strip():
            raise ValueError("An Anthropic model is required.")
        if max_tokens < 1:
            raise ValueError("Anthropic max_tokens must be positive.")
        if timeout_seconds <= 0:
            raise ValueError("The provider timeout must be positive.")
        if client_factory is None:
            from anthropic import Anthropic

            client_factory = Anthropic
        self.model = model.strip()
        self.max_tokens = max_tokens
        self._client = client_factory(api_key=api_key, timeout=timeout_seconds)
        self._max_response_characters = max_response_characters

    def generate(self, prompt: str) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        parts = [
            str(block.text)
            for block in response.content
            if getattr(block, "type", None) == "text" and getattr(block, "text", None)
        ]
        return _bounded_text("".join(parts), self._max_response_characters, "Anthropic")


def create_provider(name: ProviderName | str, api_key: str, model: str) -> TextProvider:
    """Create the selected provider without persisting credentials or mutating the environment."""

    provider_name = ProviderName(name)
    factories: dict[ProviderName, type[GeminiProvider | OpenAIProvider | AnthropicProvider]] = {
        ProviderName.GEMINI: GeminiProvider,
        ProviderName.OPENAI: OpenAIProvider,
        ProviderName.ANTHROPIC: AnthropicProvider,
    }
    return cast(TextProvider, factories[provider_name](api_key, model=model))
