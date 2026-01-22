from pathlib import Path
import re

import pymupdf

from kiosk.config import TimingConfig
from kiosk.logger import logger
from .utils import estimate_duration
from .base import RenderedView


class PdfImageRenderer:
    """
    Renderer for .pdf files.

    PDFs are converted to image before rendering.
    """

    EXTENSIONS = {".pdf"}

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(pdf_path: Path, timing: TimingConfig) -> list[RenderedView]:
        cache_dir = resolve_pdf_cache_dir(pdf_path)

        doc = pymupdf.open(pdf_path)
        views: list[RenderedView] = []

        for i in range(doc.page_count):
            page = doc.load_page(i)
            img_path = cache_dir / f'page_{i:03}.png'
            text = page.get_text('text')
            word_count = count_words(text)

            if word_count == 0:
                duration = timing.default_duration
                reason = 'default'
            else:
                duration = estimate_duration(word_count, timing)
                reason = 'wpm'

            logger.debug(
                f'PDF {pdf_path.name}: {word_count} words -> {duration}s')

            if not img_path.exists():
                pix = page.get_pixmap(dpi=150)
                pix.save(img_path)

            views.append(
                RenderedView(
                    kind='image',
                    src=f'/rotation/.cache/{pdf_path.stem}/{img_path.name}',
                    duration=duration,
                    meta={
                        'word_count': word_count,
                        'duration_reason': reason
                    }
                )
            )

        return views


def count_words(text: str) -> int:
    return len(re.findall(r'\b\w+\b', text))


def resolve_pdf_cache_dir(pdf_path: Path) -> Path:
    # Case 1: Already inside a cache namespace
    if pdf_path.parent.name == pdf_path.stem:
        return pdf_path.parent

    # Case 2: Direct PDF -> Create cache
    cache_dir = pdf_path.parent / '.cache' / pdf_path.stem
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir
