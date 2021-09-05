from dataclasses import dataclass
from typing import (
    Mapping,
    Any,
)

__all__ = [
    'ParsingResponse',
    'ParsingError',
    'LocalizedParsingResponse',
]


@dataclass
class ParsingResponse:
    channel_user_data: Mapping[str, Any]


@dataclass
class LocalizedParsingResponse:
    localized_channel_user_data: Mapping[str, Any]


@dataclass
class ParsingError:
    description: str
