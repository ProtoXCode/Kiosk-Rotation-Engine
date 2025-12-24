from pathlib import Path

from .base import RenderedView
from .url import UrlRenderer
from .html import HtmlRenderer
from .image import ImageRenderer

RENDERERS = [
    UrlRenderer(),
    HtmlRenderer(),
    ImageRenderer()
]


def render_path(path: Path) -> RenderedView:
    for r in RENDERERS:
        if r.can_render(path):
            return r.render(path)
    raise ValueError(f'No renderer for {path}')
