from pathlib import Path

from kiosk.config import TimingConfig
from kiosk.logger import logger
from kiosk.renderer.extractors.html_text import extract_text_from_html
from .utils import estimate_duration
from .base import RenderedView


class HtmlRenderer:
    """
    Render for standalone .html files.

    These are rendered as fullscreeen iframes.
    Assets (CSS/JS) are expected to be handled by the server.
    """

    EXTENSIONS = {'.html'}

    def can_handle(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path, timing: TimingConfig) -> RenderedView:
        # The app decides how paths are exposed over HTTP
        # Render only declares intent

        word_count = extract_text_from_html(path)

        if word_count == 0:
            duration = timing.default_duration
            reason = 'default'
        else:
            duration = estimate_duration(word_count, timing)
            reason = 'wpm'

        logger.debug(f'HTML {path.name}: {word_count} words -> {duration}s')

        return RenderedView(
            kind='iframe',
            src=f'/rotation/{path.name}',
            duration=duration,
            meta={
                'word_count': word_count,
                'duration_reason': reason,
                'autoscroll': True
            }
        )
