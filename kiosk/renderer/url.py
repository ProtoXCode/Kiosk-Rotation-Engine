from pathlib import Path

from .base import RenderedView


class UrlRenderer:
    """
    Renderer for .url files.

    A .url file is expected to contain a single URL as plain text.
    The kiosk will render it as a fullscreen iframe.
    """

    EXTENSIONS = {'.url'}

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path) -> RenderedView:
        try:
            url = path.read_text(encoding='utf-8').strip()
        except Exception as e:
            raise RuntimeError(f'Failed to read {path}: {e}')

        if not url:
            raise ValueError(f'Empty URL file: {path}')

        return RenderedView(
            kind='iframe',
            src=url,
            duration=15
        )
