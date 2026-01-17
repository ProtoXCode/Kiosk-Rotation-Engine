from typing import Any
import shutil
from urllib.parse import urlparse
from pathlib import Path
import subprocess
import hashlib

from yt_dlp import YoutubeDL

from kiosk.logger import logger

# TODO: WIP

def extract_video_from_url(url: str, cache_dir: Path) -> Path | None:
    """
    If URL is a supported video source, download to cache and return path.
    Otherwise, return None.

    Kinda works, kinda don't...

    """
    if not is_youtube(url):
        return None

    output = cache_dir / cache_name(url)

    if output.exists():
        logger.debug(f'Video {url} already downloaded to {output}')
        return output

    try:
        try:
            download_youtube_py(url, output)
        except Exception as e:
            logger.error(f'download_youtube_py failed to download {url}: {e}')
            if has_yt_dlp_binary():
                download_youtube_cli(url, output)
            else:
                raise

        return output

    except Exception as e:
        logger.error(f'Error downloading video {url}: {e}')
        return None


def cache_name(url: str) -> str:
    h = hashlib.sha256(url.encode()).hexdigest()[:12]
    return f'yt_{h}.mp4'


def is_youtube(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return host in {
        'youtube.com',
        'www.youtube.com',
        'youtu.be',
        'm.youtube.com'
    }


def download_youtube_py(url: str, output: Path) -> None:
    ydl_opts: Any = {
        'outtmpl': str(output.with_suffix('.%(ext)s')),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_youtube_cli(url: str, output: Path) -> None:
    subprocess.run(
        [
            'yt-dlp',
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            '--merge-output-format', 'mp4',
            '--no-playlist',
            '-o', str(output.with_suffix('.%(ext)s')),
            url
        ],
        check=True,
        timeout=120
    )


def has_yt_dlp_binary() -> bool:
    return shutil.which('yt-dlp') is not None
