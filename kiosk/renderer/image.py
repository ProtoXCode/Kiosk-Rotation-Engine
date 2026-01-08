from pathlib import Path

from .base import RenderedView
from kiosk.config import TimingConfig


class ImageRenderer:
    """
    Render for image files.

    Images are rendered fullscreen with no interaction.
    """

    EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}

    def can_handle(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path, timing: TimingConfig) -> RenderedView:
        return RenderedView(
            kind='image',
            src=f'/rotation/{path.name}',
            duration=timing.image_duration
        )
