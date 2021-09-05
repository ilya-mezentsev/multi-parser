import json
from typing import Mapping


__all__ = [
    'ChannelToLocales',
    'parse_resources',
]


LocaleField = Mapping[str, str]
ChannelToLocales = Mapping[str, Mapping[str, LocaleField]]


def parse_resources(resources_file_path: str) -> ChannelToLocales:
    with open(resources_file_path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())
