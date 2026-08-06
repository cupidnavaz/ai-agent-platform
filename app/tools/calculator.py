"""Calculator tool."""

from app.tools.tool import Tool


class CalculatorTool(Tool):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Evaluate simple Python arithmetic expressions.",
        )

    def run(self, expression: str):
        try:
            return eval(
                expression,
                {"__builtins__": {}},
                {},
            )
        except Exception as exc:
            return str(exc)

