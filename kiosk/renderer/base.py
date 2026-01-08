from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Protocol, Any

from kiosk.config import TimingConfig


@dataclass
class RenderedView:
    kind: Literal['iframe', 'image', 'video']
    src: str
    duration: int = TimingConfig.default_duration
    meta: dict[str, Any] = field(default_factory=dict)


class Renderer(Protocol):
    def can_handle(self, path: Path) -> bool: ...

    def render(self, path: Path, timing: TimingConfig) -> RenderedView: ...
