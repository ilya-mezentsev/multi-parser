from dataclasses import dataclass


__all__ = [
    'ParsingRequest',
]


@dataclass
class ParsingRequest:
    user_id: str
    channel: str
