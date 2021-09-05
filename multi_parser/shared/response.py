from dataclasses import dataclass
from typing import Mapping, Any


__all__ = [
    'ParsingResponse',
    'ParsingError',
]


@dataclass
class ParsingResponse:
    channel_user_data: Mapping[str, Any]


@dataclass
class ParsingError:
    description: str
