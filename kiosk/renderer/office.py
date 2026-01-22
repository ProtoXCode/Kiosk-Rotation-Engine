from pathlib import Path

from kiosk.config import TimingConfig
from kiosk.logger import logger
from kiosk.renderer.extractors.office_to_pdf import convert_office_to_pdf
from .base import RenderedView
from .pdf_image import PdfImageRenderer


class OfficeRenderer:
    EXTENSIONS = {
        '.doc', '.docx',
        '.ppt', '.pptx',
        '.xls', '.xlsx'
    }

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.EXTENSIONS

    @staticmethod
    def render(path: Path, timing: TimingConfig) -> list[RenderedView]:
        cache_dir = path.parent / '.cache' / path.stem
        cache_dir.mkdir(parents=True, exist_ok=True)

        pdf_path = convert_office_to_pdf(path, cache_dir)

        if not pdf_path or not pdf_path.exists():
            raise ValueError('Office -> PDF conversion failed')

        logger.debug(f'Office converted to PDF: {pdf_path.name}')

        # Delegate rendering to existing PDF renderer
        return PdfImageRenderer().render(pdf_path, timing)
