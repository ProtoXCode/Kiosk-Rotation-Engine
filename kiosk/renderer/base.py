from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Protocol, Any


@dataclass
class RenderedView:
    kind: Literal['iframe', 'image', 'video']
    src: str
    duration: int = 15  # TODO: Replace with config loader
    meta: dict[str, Any] = field(default_factory=dict)


class Renderer(Protocol):
    def can_handle(self, path: Path) -> bool: ...

    def render(self, path: Path) -> RenderedView: ...
