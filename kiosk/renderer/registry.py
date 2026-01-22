from pathlib import Path
from typing import Union

from .base import RenderedView
from .video import VideoRenderer
from .url import UrlRenderer
from .html import HtmlRenderer
from .image import ImageRenderer
from .heic import HeicRenderer
from .office import OfficeRenderer
from .pdf_image import PdfImageRenderer
from kiosk.config import TimingConfig

# Processing renderes above generic ones.
RENDERERS = [
    HeicRenderer(),  # Processed using pillow-heif
    OfficeRenderer(),  # Processes office files into PDF
    PdfImageRenderer(),  # Processed using pymupdf
    ImageRenderer(),
    VideoRenderer(),
    UrlRenderer(),
    HtmlRenderer(),
]


def render_path(path: Path, timing: TimingConfig) -> Union[
    RenderedView, list[RenderedView]]:
    for r in RENDERERS:
        if r.can_handle(path):
            return r.render(path, timing)

    raise ValueError(f'No renderer for {path}')
