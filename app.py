from pathlib import Path

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

# Prevent unsupported files to be analyzed
UNSUPPORTED = ['.md']

app = FastAPI(title='Kiosk Rotation Engine')

# Serve rotation content (html, images, rendered output later)
app.mount('/rotation', StaticFiles(directory=ROTATION_DIR), name='rotation')

# Serve static assets (player.html, CSS, JS)
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


@app.get('/', response_class=HTMLResponse)
def player():
    """
    Fullscreen kiosk player.
    Broser is expected to run in kiosk / fullscreen mode.
    """
    return (STATIC_DIR / 'player.html').read_text(encoding='utf-8')


@app.get('/playlist')
def playlist() -> list[RenderedView]:
    """ Build the rotation playlist from filesystem content. """
    views: list[RenderedView] = []
    seen_srcs: set[str] = set()

    for path in sorted(ROTATION_DIR.iterdir()):
        if not path.is_file() or path.suffix.lower() in UNSUPPORTED:
            continue

        try:
            view = render_path(path, TIMING)
        except Exception as e:
            # MVP rule: fail soft, never crash the kiosk
            logger.info(f'Skipping {path.name}: {e}')
            continue

        if view.src in seen_srcs:
            continue

        seen_srcs.add(view.src)
        views.append(view)

    return views
