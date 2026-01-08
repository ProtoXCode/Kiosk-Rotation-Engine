from pathlib import Path

from .base import RenderedView
from kiosk.config import TimingConfig


class VideoRenderer:
    EXTENSIONS = ['.mp4', '.webm', '.ogg']

    def can_handle(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path, timing: TimingConfig) -> RenderedView:
        return RenderedView(
            kind='video',
            src=f'/rotation/{path.name}',
            duration=0,  # Plays entire video
            meta={
                'autoplay': True,
                'muted': timing.video_mute
            }
        )
