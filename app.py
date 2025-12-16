from pathlib import Path

from kiosk.discovery import discover_views

views = discover_views(Path(__file__).parent / 'rotation')

for v in views:
    print(v)
