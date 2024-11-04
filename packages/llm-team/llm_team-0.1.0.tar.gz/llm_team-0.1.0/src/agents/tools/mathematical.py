import logging
from typing import Literal

from pydantic import BaseModel

from src.agents.tools import AnthropicTool

log = logging.getLogger(__name__)

__all__ = ["calculator_tool"]


def safe_calculate(
    x: float,
    y: float,
    operation: Literal['+', '-', '*', '/'],
) -> float:
    try:
        x = float(x)
        y = float(y)
    except TypeError as E:
        raise E

    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else float('inf')
    }

    return operations[operation](x, y)


calculator_tool = AnthropicTool(
    name="Calculator",
    description="Perform basic arithmetic operations safely",
    function=safe_calculate)
