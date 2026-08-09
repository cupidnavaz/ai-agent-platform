"""Tests for the provider-neutral tool registry."""

import unittest

from app.providers.models import (
    ToolCall,
    ToolDefinition,
)
from app.providers.tools import ToolRegistry


class ToolRegistryTests(unittest.TestCase):
    """Tool registry tests."""

    def test_register_and_get(self):
        registry = ToolRegistry()

        definition = ToolDefinition(
            name="add",
            description="Add two numbers.",
        )

        registry.register(
            definition,
            lambda a, b: a + b,
        )

        self.assertIs(
            registry.get("add"),
            definition,
        )

    def test_definitions(self):
        registry = ToolRegistry()

        first = ToolDefinition(
            name="first",
            description="First tool.",
        )

        second = ToolDefinition(
            name="second",
            description="Second tool.",
        )

        registry.register(
            first,
            lambda: "one",
        )

        registry.register(
            second,
            lambda: "two",
        )

        self.assertEqual(
            registry.definitions(),
            [first, second],
        )

    def test_execute(self):
        registry = ToolRegistry()

        registry.register(
            ToolDefinition(
                name="add",
                description="Add two numbers.",
            ),
            lambda a, b: a + b,
        )

        result = registry.execute(
            ToolCall(
                id="call_123",
                name="add",
                arguments={
                    "a": 2,
                    "b": 3,
                },
            ),
        )

        self.assertEqual(
            result.tool_call_id,
            "call_123",
        )

        self.assertEqual(
            result.content,
            "5",
        )

    def test_string_result(self):
        registry = ToolRegistry()

        registry.register(
            ToolDefinition(
                name="hello",
                description="Say hello.",
            ),
            lambda: "hello world",
        )

        result = registry.execute(
            ToolCall(
                id="call_456",
                name="hello",
            ),
        )

        self.assertEqual(
            result.content,
            "hello world",
        )

    def test_empty_name_rejected(self):
        registry = ToolRegistry()

        with self.assertRaises(ValueError):
            registry.register(
                ToolDefinition(
                    name="",
                    description="Invalid tool.",
                ),
                lambda: "invalid",
            )

    def test_duplicate_tool_rejected(self):
        registry = ToolRegistry()

        definition = ToolDefinition(
            name="ping",
            description="Ping.",
        )

        registry.register(
            definition,
            lambda: "pong",
        )

        with self.assertRaises(ValueError):
            registry.register(
                definition,
                lambda: "pong",
            )

    def test_unknown_tool_get(self):
        registry = ToolRegistry()

        with self.assertRaises(KeyError):
            registry.get("missing")

    def test_unknown_tool_execute(self):
        registry = ToolRegistry()

        with self.assertRaises(KeyError):
            registry.execute(
                ToolCall(
                    id="call_missing",
                    name="missing",
                ),
            )

    def test_handler_error(self):
        registry = ToolRegistry()

        def failing_tool() -> str:
            raise ValueError("boom")

        registry.register(
            ToolDefinition(
                name="failing",
                description="Always fails.",
            ),
            failing_tool,
        )

        with self.assertRaises(RuntimeError):
            registry.execute(
                ToolCall(
                    id="call_error",
                    name="failing",
                ),
            )


if __name__ == "__main__":
    unittest.main()
