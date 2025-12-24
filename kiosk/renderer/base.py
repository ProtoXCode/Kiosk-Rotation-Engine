from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol


@dataclass
class RenderedView:
    kind: Literal['iframe', 'image', 'video']
    src: str
    duration: int = 15  # TODO: Replace with config loader


class Renderer(Protocol):
    def can_handle(self, path: Path) -> bool: ...

    def render(self, path: Path) -> RenderedView: ...
