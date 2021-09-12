import json
from typing import Union

from aiohttp import web

from multi_parser.channels import IChannelAdapter
from multi_parser.shared import (
    ParsingRequest,
    ParsingResponse,
    ParsingError,
)


__all__ = [
    'Controller',
]


class Controller:

    def __init__(
            self,
            channel_helper: IChannelAdapter,
    ) -> None:

        self._channel_helper = channel_helper

    async def parse_channel_user_data(
            self,
            request: web.Request,
    ) -> web.Response:

        channel = request.match_info.get('channel', '')
        user_id = request.match_info.get('user_id', '')

        response = await self._channel_helper.parse(ParsingRequest(
            channel=channel,
            user_id=user_id,
        ))

        return self._make_response(response)

    @staticmethod
    def _make_response(response: Union[ParsingResponse, ParsingError]) -> web.Response:

        if isinstance(response, ParsingResponse):
            return web.Response(
                status=web.HTTPOk.status_code,
                body=json.dumps({
                    'channel_user_data': response.channel_user_data,
                }),
                content_type='application/json',
            )

        elif isinstance(response, ParsingError):
            return web.Response(
                status=web.HTTPBadRequest.status_code,
                body=json.dumps({
                    'description': response.description,
                }),
                content_type='application/json',
            )

        else:
            raise RuntimeError(f'Unknown response type: {type(response)!r}')
