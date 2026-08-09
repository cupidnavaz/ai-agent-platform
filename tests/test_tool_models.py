"""Tests for shared tool models."""

import unittest

from app.providers.models import (
    ToolCall,
    ToolDefinition,
    ToolResult,
)


class ToolModelTests(unittest.TestCase):
    """Shared tool model tests."""

    def test_tool_definition(self):
        tool = ToolDefinition(
            name="get_weather",
            description="Get the current weather.",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                    },
                },
                "required": ["location"],
            },
        )

        self.assertEqual(
            tool.name,
            "get_weather",
        )
        self.assertEqual(
            tool.description,
            "Get the current weather.",
        )
        self.assertEqual(
            tool.parameters["type"],
            "object",
        )

    def test_tool_definition_defaults(self):
        tool = ToolDefinition(
            name="ping",
            description="Ping a service.",
        )

        self.assertEqual(
            tool.parameters,
            {},
        )

    def test_tool_call(self):
        call = ToolCall(
            id="call_123",
            name="get_weather",
            arguments={
                "location": "Lagos",
            },
        )

        self.assertEqual(
            call.id,
            "call_123",
        )
        self.assertEqual(
            call.name,
            "get_weather",
        )
        self.assertEqual(
            call.arguments["location"],
            "Lagos",
        )

    def test_tool_call_defaults(self):
        call = ToolCall(
            id="call_123",
            name="ping",
        )

        self.assertEqual(
            call.arguments,
            {},
        )

    def test_tool_result(self):
        result = ToolResult(
            tool_call_id="call_123",
            content="The weather is sunny.",
        )

        self.assertEqual(
            result.tool_call_id,
            "call_123",
        )
        self.assertEqual(
            result.content,
            "The weather is sunny.",
        )


if __name__ == "__main__":
    unittest.main()
