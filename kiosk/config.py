from dataclasses import dataclass
from pathlib import Path

import yaml

from kiosk.logger import logger

# Default settings
DEFAULT_DURATION = 10
MINIMUM_DURATION = 5
MAXIMUM_DURATION = 60
IMAGE_DURATION = 10
WORDS_PER_MINUTE = 180
VIDEO_MUTE = True
MEDIA_DIRECTORY = Path(__file__).resolve().parent.parent / 'rotation'
PLAYLIST_SCAN = 60


@dataclass
class TimingConfig:
    default_duration: int = DEFAULT_DURATION
    min_duration: int = MINIMUM_DURATION
    max_duration: int = MAXIMUM_DURATION
    image_duration: int = IMAGE_DURATION
    words_per_minute: int = WORDS_PER_MINUTE
    video_mute: bool = VIDEO_MUTE
    media_directory: Path = MEDIA_DIRECTORY
    playlist_scan: int = PLAYLIST_SCAN


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
                    'media_directory': str(default.timing.media_directory),
                    'playlist_scan': default.timing.playlist_scan
                }
            }),
            encoding='utf-8'
        )
        return default

    data = yaml.safe_load(path.read_text()) or {}
    logger.info(f'Using config file: {path.resolve()}')

    rotation = data.get('rotation', {})

    return AppConfig(timing=TimingConfig(
        default_duration=rotation.get('default_duration', DEFAULT_DURATION),
        min_duration=rotation.get('min_duration', MINIMUM_DURATION),
        max_duration=rotation.get('max_duration', MAXIMUM_DURATION),
        image_duration=rotation.get('image_duration', IMAGE_DURATION),
        words_per_minute=rotation.get('words_per_minute', WORDS_PER_MINUTE),
        video_mute=rotation.get('video_mute', VIDEO_MUTE),
        media_directory=Path(rotation.get('media_directory', MEDIA_DIRECTORY)),
        playlist_scan=rotation.get('playlist_scan', PLAYLIST_SCAN)
    ))
