"""Model-provider adapters used by SparkPrompt."""

from collections.abc import Callable, Iterable
from typing import Any, Protocol

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


class TextProvider(Protocol):
    """Minimal model capability required by the application service."""

    def generate(self, prompt: str) -> str:
        """Generate text for one application-owned prompt."""


class StreamingChatModel(Protocol):
    def stream(self, messages: list[HumanMessage]) -> Iterable[Any]: ...


ChatModelFactory = Callable[..., StreamingChatModel]


class GeminiProvider:
    """Session-owned Gemini client.

    The API key is passed directly to the client. It is never copied into the
    process environment, a module global, or a cross-session cache.
    """

    def __init__(
        self,
        api_key: str,
        *,
        model: str = "models/gemini-2.0-flash",
        client_factory: ChatModelFactory = ChatGoogleGenerativeAI,
    ) -> None:
        if not api_key.strip():
            raise ValueError("A Google API key is required.")
        self._client = client_factory(model=model, google_api_key=api_key)

    def generate(self, prompt: str) -> str:
        chunks = self._client.stream([HumanMessage(content=prompt)])
        return "".join(str(chunk.content) for chunk in chunks)
