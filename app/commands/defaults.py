"""Default commands."""

from app.commands import router
from app.tools.manager import manager


def calculator(argument: str):
    result = manager.execute(
        "calculator",
        argument,
    )

    return f"Calculator result: {result}"


router.register("/calc", calculator)
