from pathlib import Path

from .base import RenderedView
from .video import VideoRenderer
from .url import UrlRenderer
from .html import HtmlRenderer
from .image import ImageRenderer
from .heic import HeicRenderer
from kiosk.config import TimingConfig

# Processing renderes above generic ones.
RENDERERS = [
    HeicRenderer(),  # Processed using pillow-heif
    ImageRenderer(),
    VideoRenderer(),
    UrlRenderer(),
    HtmlRenderer(),
]


def render_path(path: Path, timing: TimingConfig) -> RenderedView:
    for r in RENDERERS:
        if r.can_handle(path):
            return r.render(path, timing)

    raise ValueError(f'No renderer for {path}')
