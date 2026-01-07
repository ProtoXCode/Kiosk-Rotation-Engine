from pathlib import Path

from .base import RenderedView
from .video import VideoRenderer
from .url import UrlRenderer
from .html import HtmlRenderer
from .image import ImageRenderer

RENDERERS = [
    ImageRenderer(),
    VideoRenderer(),
    UrlRenderer(),
    HtmlRenderer(),
]


def render_path(path: Path) -> RenderedView:
    for r in RENDERERS:
        if r.can_handle(path):
            return r.render(path)

    raise ValueError(f'No renderer for {path}')
