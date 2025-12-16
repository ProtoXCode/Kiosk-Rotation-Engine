from dataclasses import dataclass
from typing import Literal

ViewType = Literal['url', 'html', 'image', 'video', 'folder']


@dataclass
class View:
    type: ViewType
    source: str
    name: str
