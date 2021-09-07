import logging
from typing import (
    Mapping,
    Any,
    Union,
)

from multi_parser.channels.adapters import BaseChannelAdapter
from multi_parser.shared import (
    ParsingError,
    ParsingRequest,
    ParsingResponse,
)


__all__ = [
    'VkChannelAdapter',
]


class VkChannelAdapter(BaseChannelAdapter):

    CHANNEL_TYPE = 'vk'

    class ErrorCode:
        INVALID_USER_ID = 113

    def _url(self, user_id: str) -> str:
        return (
            f'https://api.vk.com/method/users.get?v=5.131&user_ids={user_id}'
            f'&access_token={self._channel_to_token[self.CHANNEL_TYPE]}'
            f'&fields=bdate,screen_name,sex,timezone,photo_max_orig,online'
        )

    def _adapt_success_parsing_response(
            self,
            request: ParsingRequest,
            response_data: Mapping[str, Any],
    ) -> Union[ParsingResponse, ParsingError]:

        if 'error' in response_data:
            return self._on_error_response(response_data)

        elif 'response' in response_data:
            return ParsingResponse(
                channel_user_data=response_data['response'][0],
            )

        else:
            logging.error(
                f'Got unexpected response from VK API: {response_data}')

            return self._make_unknown_error()

    def _on_error_response(
            self,
            response_data: Mapping[str, Any],
    ) -> ParsingError:

        assert 'error' in response_data

        if response_data['error'].get('error_code') == self.ErrorCode.INVALID_USER_ID:
            return ParsingError(
                description=response_data['error']['error_msg'],
            )

        else:
            return self._make_unknown_error()
