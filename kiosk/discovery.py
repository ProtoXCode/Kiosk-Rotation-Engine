from pathlib import Path

from .models import View

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}
VIDEO_EXTS = {'.mp4', '.mov', '.webm'}


def discover_views(rotation_dir: Path) -> list[View]:
    views: list[View] = []

    if not rotation_dir.exists():
        return views

    for item in sorted(rotation_dir.iterdir()):
        if item.name.startswith('.'):
            continue

        # --- URL files -------------------------------------------------------
        if item.is_file() and item.suffix == '.url':
            url = item.read_text(encoding='utf-8').strip()
            if url:
                views.append(
                    View(
                        type='url',
                        source=url,
                        name=item.name
                    )
                )
            continue

        # --- Static HTML files -----------------------------------------------
        if item.is_file() and item.suffix == '.html':
            views.append(
                View(
                    type='html',
                    source=str(item),
                    name=item.name
                )
            )
            continue

        # --- Images ----------------------------------------------------------
        if item.is_file() and item.suffix.lower() in IMAGE_EXTS:
            views.append(
                View(
                    type='image',
                    source=str(item),
                    name=item.name
                )
            )
            continue

        # --- Videos ----------------------------------------------------------
        if item.is_file() and item.suffix in VIDEO_EXTS:
            views.append(
                View(
                    type='video',
                    source=str(item),
                    name=item.name
                )
            )
            continue

        # --- Folder with index.html ------------------------------------------
        if item.is_dir():
            index = item / 'index.html'
            if index.exists():
                views.append(
                    View(
                        type='folder',
                        source=str(index),
                        name=index.name
                    )
                )

    return views
