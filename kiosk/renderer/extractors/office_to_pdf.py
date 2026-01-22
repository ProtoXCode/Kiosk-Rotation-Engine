from pathlib import Path
import subprocess
import platform
import shutil


def convert_office_to_pdf(input_file: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    soffice = find_libreoffice()

    subprocess.run([
        soffice,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', str(output_dir),
        str(input_file)
    ], check=True, timeout=120)

    return output_dir / (input_file.stem + '.pdf')


def find_libreoffice() -> str:
    """ Locate LibreOffice / soffice executable across all platforms """
    # 1. PATH lookup (Linux, macOS, Windows if added)
    exe = shutil.which('libreoffice') or shutil.which('soffice')
    if exe:
        return exe

    system = platform.system()

    # 2. windows fallback paths
    if system == 'Windows':
        candidates = [
            r'C:\Program Files\LibreOffice\program\soffice.exe',
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe'
        ]

        for win_path in candidates:
            if Path(win_path).exists():
                return win_path

    # 3. macOS fallback
    if system == 'Darwin':
        mac_path = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        if Path(mac_path).exists():
            return mac_path

    raise FileNotFoundError(
        'LibreOffice not found. Install LibreOffice and ensure '
        '"libreoffice" or "soffice" is available on PATH.'
    )
