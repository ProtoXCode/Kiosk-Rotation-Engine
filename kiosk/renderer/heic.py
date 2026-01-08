from pathlib import Path
from PIL import Image
import pillow_heif

from .base import RenderedView
from kiosk.config import TimingConfig


class HeicRenderer:
    """
    Render for .heic and .heif image files

    Images are processed with pillow to be rendered.
    """

    EXTENSIONS = {'.heic', '.heif'}

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path, timing: TimingConfig) -> RenderedView:
        """ Convert once, cache result """
        output = path.with_suffix('.jpg')

        if not output.exists() or output.stat().st_mtime < path.stat().st_mtime:
            heif_file = pillow_heif.read_heif(path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                'raw'
            )
            image.save(output, format='JPEG', quality=90)

        return RenderedView(
            kind='image',
            src=f'/rotation/{output.name}',
            duration=timing.image_duration,
            consumes_source=True
        )
