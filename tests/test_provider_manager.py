"""Tests for the provider manager."""

import unittest

from app.providers.manager import ProviderManager
from app.providers.mock import MockProvider
from app.providers.models import (
    ChatRequest,
    ChatResponse,
    Message,
    ProviderCapabilities,
)
from app.providers.provider_info import ProviderInfo
from app.providers.stream import ChatChunk


class ProviderManagerTests(unittest.TestCase):
    """Provider manager tests."""

    def setUp(self):
        self.manager = ProviderManager()
        self.provider = MockProvider()

    def test_register_provider(self):
        self.manager.register(self.provider)

        self.assertEqual(
            self.manager.list_providers(),
            ["mock"],
        )

    def test_get_provider(self):
        self.manager.register(self.provider)

        provider = self.manager.get("mock")

        self.assertIs(provider, self.provider)

    def test_active_provider(self):
        self.manager.register(self.provider)

        self.assertEqual(
            self.manager.active().name,
            "mock",
        )

    def test_set_active_provider(self):
        self.manager.register(self.provider)

        self.manager.set_active("mock")

        self.assertEqual(
            self.manager.active().name,
            "mock",
        )

    def test_remove_provider(self):
        self.manager.register(self.provider)

        self.manager.remove("mock")

        self.assertEqual(
            self.manager.list_providers(),
            [],
        )

    def test_health(self):
        self.manager.register(self.provider)

        self.assertEqual(
            self.manager.health(),
            {
                "mock": True,
            },
        )

    def test_summary(self):
        self.manager.register(self.provider)

        summary = self.manager.summary()

        self.assertEqual(
            len(summary),
            1,
        )

        info = summary[0]

        self.assertIsInstance(
            info,
            ProviderInfo,
        )

        self.assertEqual(
            info.name,
            "mock",
        )

        self.assertTrue(info.active)

        self.assertTrue(info.healthy)

        self.assertEqual(
            info.models,
            ["mock-v1"],
        )

        self.assertTrue(
            info.capabilities.chat,
        )

    def test_unknown_provider(self):
        with self.assertRaises(KeyError):
            self.manager.get("unknown")

    def test_unknown_active_provider(self):
        with self.assertRaises(KeyError):
            self.manager.set_active("unknown")

    def test_no_active_provider(self):
        with self.assertRaises(RuntimeError):
            self.manager.active()


class RoutingProvider(MockProvider):
    """Test provider used to verify manager routing."""

    def __init__(
        self,
        name: str,
        response_content: str,
    ) -> None:
        super().__init__()
        self._name = name
        self._response_content = response_content
        self.chat_requests = []
        self.stream_requests = []

    @property
    def name(self) -> str:
        """Return test provider name."""

        return self._name

    @property
    def capabilities(self) -> ProviderCapabilities:
        """Return streaming test capabilities."""

        return ProviderCapabilities(
            chat=True,
            streaming=True,
        )

    def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Record and respond to a chat request."""

        self.chat_requests.append(request)

        return ChatResponse(
            content=self._response_content,
            model="test-model",
        )

    def stream_chat(
        self,
        request: ChatRequest,
    ):
        """Record and stream a test response."""

        self.stream_requests.append(request)

        yield ChatChunk(
            content="Hello",
        )

        yield ChatChunk(
            content=" world",
        )

        yield ChatChunk(
            content="",
            finished=True,
        )


class ProviderManagerRoutingTests(unittest.TestCase):
    """Tests for manager request routing."""

    def setUp(self):
        self.manager = ProviderManager()

        self.first = RoutingProvider(
            "first",
            "First response",
        )

        self.second = RoutingProvider(
            "second",
            "Second response",
        )

        self.manager.register(self.first)
        self.manager.register(self.second)

    def test_chat_routes_to_active_provider(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                ),
            ],
        )

        response = self.manager.chat(request)

        self.assertEqual(
            response.content,
            "First response",
        )

        self.assertEqual(
            len(self.first.chat_requests),
            1,
        )

        self.assertEqual(
            self.first.chat_requests[0],
            request,
        )

        self.assertEqual(
            len(self.second.chat_requests),
            0,
        )

    def test_chat_routes_after_switching_provider(self):
        self.manager.set_active("second")

        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Hello",
                ),
            ],
        )

        response = self.manager.chat(request)

        self.assertEqual(
            response.content,
            "Second response",
        )

        self.assertEqual(
            len(self.second.chat_requests),
            1,
        )

        self.assertEqual(
            len(self.first.chat_requests),
            0,
        )

    def test_stream_routes_to_active_provider(self):
        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Say hello.",
                ),
            ],
        )

        chunks = list(
            self.manager.stream(request)
        )

        self.assertEqual(
            [chunk.content for chunk in chunks],
            [
                "Hello",
                " world",
                "",
            ],
        )

        self.assertTrue(
            chunks[-1].finished,
        )

        self.assertEqual(
            len(self.first.stream_requests),
            1,
        )

        self.assertEqual(
            self.first.stream_requests[0],
            request,
        )

    def test_stream_routes_after_switching_provider(self):
        self.manager.set_active("second")

        request = ChatRequest(
            messages=[
                Message(
                    role="user",
                    content="Say hello.",
                ),
            ],
        )

        chunks = list(
            self.manager.stream(request)
        )

        self.assertEqual(
            [chunk.content for chunk in chunks],
            [
                "Hello",
                " world",
                "",
            ],
        )

        self.assertEqual(
            len(self.second.stream_requests),
            1,
        )

        self.assertEqual(
            len(self.first.stream_requests),
            0,
        )


if __name__ == "__main__":
    unittest.main()
