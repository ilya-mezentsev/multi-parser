from typing import (
    Optional,
    Mapping,
    Any,
)

from .base import BaseChannelAdapter


__all__ = [
    'GithubChannelAdapter',
]


class GithubChannelAdapter(BaseChannelAdapter):

    CHANNEL_TYPE = 'github'

    def url(self, user_id: str) -> str:
        return f'https://api.github.com/users/{user_id}'

    @staticmethod
    def headers() -> Optional[Mapping[str, Any]]:
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5'
            '37.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
