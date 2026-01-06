from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class TimingConfig:
    default_duration: int
    min_duration: int
    max_duration: int
    words_per_minute: int


@dataclass
class AppConfig:
    timing: TimingConfig


def load_config(path: Path) -> AppConfig:
    data = yaml.safe_load(path.read_text())

    return AppConfig(
        timing=TimingConfig(
            default_duration=data['rotation']['default_rotation'],
            min_duration=data['rotation']['min_rotation'],
            max_duration=data['rotation']['max_rotation'],
            words_per_minute=data['rotation']['words_per_minute']
        )
    )
