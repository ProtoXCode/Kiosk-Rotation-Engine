from pathlib import Path

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
    def render(path: Path) -> RenderedView:
        # The app decides how paths are exposed over HTTP
        # Render only declares intent
        src = f'/rotation/{path.name}'

        return RenderedView(
            kind='iframe',
            src=src,
            duration=10
        )
