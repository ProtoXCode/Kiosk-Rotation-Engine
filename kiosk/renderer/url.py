from pathlib import Path

from .base import RenderedView
from kiosk.logger import logger
from kiosk.config import TimingConfig
from kiosk.renderer.extractors.url_text import extract_text_from_url
from .utils import estimate_duration


class UrlRenderer:
    """
    Renderer for .url files.

    A .url file is expected to contain a single URL as plain text.
    The kiosk will render it as a fullscreen iframe.
    """

    EXTENSIONS = {'.url'}

    def can_handle(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path, timing: TimingConfig) -> RenderedView:
        text = path.read_text(encoding='utf-8', errors='ignore')

        url = None
        for line in text.splitlines():
            if line.startswith('URL='):
                url = line[4:].strip()
                break

        if not url:
            logger.warning(f'No URL found in {path}')
            raise ValueError(f'No URL= found in {path}')

        duration = timing.default_duration
        meta = {}

        try:
            word_count = extract_text_from_url(url)
            duration = estimate_duration(word_count, timing)
            meta['estimated_words'] = word_count
            meta['duration_source'] = 'url_word_estimate'
            logger.debug(f'URL {url}: {word_count} words -> {duration}s')
        except Exception as e:
            logger.info(f'URL word estimation failed for {url}, '
                        f'using default duration: {e}')
            meta['duration_source'] = 'default'

        return RenderedView(
            kind='iframe',
            src=url,
            duration=duration,
            meta=meta
        )
