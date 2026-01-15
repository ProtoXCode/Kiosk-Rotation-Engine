from pathlib import Path
from PIL import Image
import pillow_heif

from .base import RenderedView
from kiosk.config import TimingConfig
from kiosk.logger import logger


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
        # rotation/.cache/<filename>
        cache_root = path.parent / '.cache'
        cache_dir = cache_root / path.stem
        cache_dir.mkdir(parents=True, exist_ok=True)

        output = cache_dir / f'{path.stem}.jpg'

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
            src=f'/rotation/.cache/{path.stem}/{output.name}',
            duration=timing.image_duration,
            consumes_source=True
        )
