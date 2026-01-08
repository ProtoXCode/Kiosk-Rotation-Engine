from pathlib import Path

from .base import RenderedView
from kiosk.logger import logger
from kiosk.config import TimingConfig


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

        for line in text.splitlines():
            if line.startswith('URL='):
                url = line[4:].strip()
                break

        else:
            logger.warning(f'No URL found in {path}')
            raise ValueError(f'No URL= found in {path}')

        return RenderedView(
            kind='iframe',
            src=url,
            duration=timing.default_duration  # TODO
        )
