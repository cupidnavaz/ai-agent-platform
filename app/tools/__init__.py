from app.tools.tool import Tool
from app.tools.registry import ToolRegistry
from app.tools.executor import ToolExecutor

from app.tools.calculator import CalculatorTool
from app.tools.file_reader import FileReaderTool

registry = ToolRegistry()

registry.register(CalculatorTool())
registry.register(FileReaderTool())

executor = ToolExecutor(registry)
