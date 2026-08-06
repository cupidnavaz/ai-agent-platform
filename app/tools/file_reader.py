"""File Reader Tool."""

from pathlib import Path

from app.tools.tool import Tool


class FileReaderTool(Tool):
    """Reads text files."""

    def __init__(self):
        super().__init__(
            name="file_reader",
            description="Read a text file.",
        )

    def run(self, path: str):
        file_path = Path(path)

        if not file_path.exists():
            return f"File not found: {path}"

        if not file_path.is_file():
            return f"Not a file: {path}"

        try:
            return file_path.read_text(encoding="utf-8")
        except Exception as exc:
            return str(exc)
