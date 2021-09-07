from typing import (
    Optional,
    Mapping,
    Any,
)

from multi_parser.shared import ParsingError
from multi_parser.channels.adapters import BaseChannelAdapter


__all__ = [
    'GithubChannelAdapter',
]


class GithubChannelAdapter(BaseChannelAdapter):

    CHANNEL_TYPE = 'github'

    def _url(self, user_id: str) -> str:
        return f'https://api.github.com/users/{user_id}'

    @staticmethod
    def _headers() -> Optional[Mapping[str, Any]]:
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5'
            '37.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }

    def _adapt_error_parsing_response(self, response_data: Mapping[str, Any]) -> ParsingError:
        if 'message' in response_data:
            return ParsingError(
                description=response_data['message'],
            )

        else:
            return self._make_unknown_error()
