from pathlib import Path

from pypdf import PdfReader

from .base import RenderedView
from kiosk.config import TimingConfig


class PdfIframeRenderer:
    """
    Renderer for .pdf files.

    PDFs are rendered using the browser's native PDF viewer
    inside a fullscreen iframe.

    NOTE:
    This kinda works, but barely. On multipage PDF's half the pages are black,
    most likely due to render pipeline, also it seems to only work on Firefox.
    """

    EXTENSIONS = {'.pdf'}

    def can_handle(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path, timing: TimingConfig) -> list[RenderedView]:
        page_count = get_pdf_page_count(path)

        # MVP time...
        per_page_duration = timing.default_duration

        views: list[RenderedView] = []

        for page in range(1, page_count + 1):
            views.append(
                RenderedView(
                    kind='iframe',
                    src=f'/rotation/{path.name}#page={page}',
                    duration=per_page_duration,
                    meta={
                        'type': 'pdf',
                        'page': page,
                        'pages': page_count
                    }
                )
            )
        return views


def get_pdf_page_count(path: Path) -> int:
    reader = PdfReader(str(path))
    return len(reader.pages)
