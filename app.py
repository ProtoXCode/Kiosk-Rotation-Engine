from threading import Lock
from pathlib import Path
import threading
import time

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from kiosk.renderer.registry import render_path
from kiosk.renderer.base import RenderedView
from kiosk.logger import logger
from kiosk.config import load_config

CONFIG = load_config(Path(__file__).parent / 'config.yaml')

TIMING = CONFIG.timing
ROTATION_DIR = CONFIG.timing.media_directory
STATIC_DIR = Path('static')
PLAYLIST: list[RenderedView] = []
PLAYLIST_VERSION: int = 0
PLAYLIST_LOCK = Lock()

# Prevent unsupported files to be analyzed
SKIP_EXTENSIONS = ['.md']

app = FastAPI(title='Kiosk Rotation Engine')

# Serve rotation content (html, images, rendered output later)
app.mount('/rotation', StaticFiles(directory=ROTATION_DIR), name='rotation')

# Serve static assets (player.html, CSS, JS)
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def build_playlist() -> list[RenderedView]:
    """ Build the rotation playlist from filesystem content. """
    views: list[RenderedView] = []
    seen_srcs: set[str] = set()

    for path in sorted(ROTATION_DIR.iterdir()):
        if not path.is_file() or path.suffix.lower() in SKIP_EXTENSIONS:
            continue

        try:
            view = render_path(path, TIMING)
        except Exception as e:
            logger.info(f'Skipping {path.name}: {e}')
            continue

        if view.src in seen_srcs:
            continue

        seen_srcs.add(view.src)
        views.append(view)

    return views


def playlist_watcher(interval: int) -> None:
    """ Watch the rotation playlist for given interval. """
    global PLAYLIST, PLAYLIST_VERSION

    while True:
        try:
            new_playlist = build_playlist()
            with PLAYLIST_LOCK:
                if new_playlist != PLAYLIST:
                    PLAYLIST = new_playlist
                    PLAYLIST_VERSION += 1
                    logger.info(f'Playlist updated, '
                                f'items in rotation playlist: {len(PLAYLIST)}')
        except Exception as e:
            logger.error(f'Error updating rotation playlist: {e}')

        time.sleep(interval)


@app.on_event('startup')
def start_playlist_watcher():
    global PLAYLIST, PLAYLIST_VERSION

    # Build once synchronously
    initial = build_playlist()
    with PLAYLIST_LOCK:
        PLAYLIST = initial
        PLAYLIST_VERSION += 1

    logger.info(f'Initial playlist build: {len(PLAYLIST)} items')

    interval = max(CONFIG.timing.playlist_scan, 5)
    thread = threading.Thread(
        target=playlist_watcher,
        args=(interval,),
        daemon=True
    )
    thread.start()


@app.get('/', response_class=HTMLResponse)
def player():
    """
    Fullscreen kiosk player.
    Broser is expected to run in kiosk / fullscreen mode.
    """
    return (STATIC_DIR / 'player.html').read_text(encoding='utf-8')


@app.get('/playlist')
def playlist():
    with PLAYLIST_LOCK:
        return {
            'version': PLAYLIST_VERSION,
            'items': PLAYLIST
        }
