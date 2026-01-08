from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from kiosk.renderer.registry import render_path
from kiosk.renderer.base import RenderedView
from kiosk.logger import logger
from kiosk.config import load_config

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG = load_config(BASE_DIR / 'config.yaml')
TIMING = CONFIG.timing

ROTATION_DIR = CONFIG.timing.media_directory
STATIC_DIR = Path('static')

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

    for path in sorted(ROTATION_DIR.iterdir()):
        if not path.is_file():
            continue

        try:
            view = render_path(path, TIMING)
            views.append(view)
        except Exception as e:
            # MVP rule: fail soft, never crash the kiosk
            logger.info(f'Skipping {path.name}: {e}')

    return views
