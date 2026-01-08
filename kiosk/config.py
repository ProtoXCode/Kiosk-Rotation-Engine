from dataclasses import dataclass
from pathlib import Path

import yaml

from kiosk.logger import logger

# Default settings
DEF_DUR = 10
MIN_DUR = 5
MAX_DUR = 60
IMG_DUR = 10
WPM_DUR = 180
VID_MUTE = True
DIRECTORY = Path(__file__).resolve().parent.parent / 'rotation'


@dataclass
class TimingConfig:
    default_duration: int = DEF_DUR
    min_duration: int = MIN_DUR
    max_duration: int = MAX_DUR
    image_duration: int = IMG_DUR
    words_per_minute: int = WPM_DUR
    video_mute: bool = VID_MUTE
    media_directory: Path = DIRECTORY


@dataclass
class AppConfig:
    timing: TimingConfig


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        logger.info(f'No config file found at {path}, creating default')
        default = AppConfig(timing=TimingConfig())
        path.write_text(
            yaml.safe_dump({
                'rotation': {
                    'default_duration': default.timing.default_duration,
                    'min_duration': default.timing.min_duration,
                    'max_duration': default.timing.max_duration,
                    'image_duration': default.timing.image_duration,
                    'words_per_minute': default.timing.words_per_minute,
                    'video_mute': default.timing.video_mute,
                    'media_directory': str(default.timing.media_directory)
                }
            }),
            encoding='utf-8'
        )
        return default

    data = yaml.safe_load(path.read_text()) or {}

    rotation = data.get('rotation', {})

    return AppConfig(timing=TimingConfig(
        default_duration=rotation.get('default_duration', DEF_DUR),
        min_duration=rotation.get('min_duration', MIN_DUR),
        max_duration=rotation.get('max_duration', MAX_DUR),
        image_duration=rotation.get('image_duration', IMG_DUR),
        words_per_minute=rotation.get('words_per_minute', WPM_DUR),
        video_mute=rotation.get('video_mute', VID_MUTE),
        media_directory=Path(rotation.get('media_directory', DIRECTORY))
    ))
