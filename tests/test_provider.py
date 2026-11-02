import os
from dataclasses import dataclass

import pytest

from sparkprompt.providers import GeminiProvider


@dataclass
class Chunk:
    content: str


class FakeClient:
    def __init__(self, *, api_key: str) -> None:
        self.api_key = api_key
        self.messages = []

    def stream(self, messages):
        self.messages.append(messages)
        return [Chunk("first "), Chunk("second")]


def test_gemini_provider_uses_an_isolated_client_per_api_key(monkeypatch) -> None:
    created = []

    def factory(*, model, google_api_key):
        client = FakeClient(api_key=google_api_key)
        created.append((model, client))
        return client

    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    first = GeminiProvider("key-one", client_factory=factory)
    second = GeminiProvider("key-two", client_factory=factory)

    assert first.generate("one") == "first second"
    assert second.generate("two") == "first second"
    assert created[0][1] is not created[1][1]
    assert [item[1].api_key for item in created] == ["key-one", "key-two"]
    assert "GOOGLE_API_KEY" not in os.environ


def test_gemini_provider_rejects_blank_key() -> None:
    with pytest.raises(ValueError, match="required"):
        GeminiProvider("   ")
