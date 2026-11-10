from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


ToolHandler = Callable[[dict[str, Any]], Any]


@dataclass(frozen=True)
class Tool:
    """A named executable capability exposed to the runtime."""

    name: str
    description: str
    handler: ToolHandler

    def execute(self, input: dict[str, Any]) -> Any:
        return self.handler(input)


class ToolRegistry:
    """Deterministic tool lookup and execution boundary."""

    def __init__(self, tools: list[Tool] | None = None) -> None:
        self._tools: dict[str, Tool] = {}
        for tool in tools or []:
            self.register(tool)

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {name}") from exc

    def execute(self, name: str, input: dict[str, Any]) -> Any:
        return self.get(name).execute(input)
