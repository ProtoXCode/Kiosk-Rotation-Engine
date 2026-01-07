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
        return path.is_file() and path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path) -> RenderedView:
        text = path.read_text(encoding='utf-8', errors='ignore')

        for line in text.splitlines():
            if line.startswith('URL='):
                url = line[4:].strip()
                break

        else:
            raise ValueError(f'No URL= found in {path}')

        return RenderedView(
            kind='iframe',
            src=url,
            duration=10
        )
