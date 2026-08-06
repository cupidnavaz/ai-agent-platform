"""Calculator plugin."""

from app.plugins import Plugin


class CalculatorPlugin(Plugin):

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Registers calculator functionality.",
        )

    def setup(self) -> None:
        print("Calculator plugin loaded.")
