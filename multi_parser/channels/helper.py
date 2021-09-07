from typing import Mapping, Union

from multi_parser.channels.shared import IHttpRequester, ChannelToToken
from multi_parser.channels.adapters import (
    IChannelAdapter,
    GithubChannelAdapter,
    VkChannelAdapter,
)
from multi_parser.shared import (
    ParsingRequest,
    ParsingResponse,
    ParsingError,
)


__all__ = [
    'ChannelHelper',
]


class ChannelHelper:

    _channel_type_to_adapter: Mapping[str, IChannelAdapter]

    def __init__(
            self,
            http_requester: IHttpRequester,
            channel_to_token: ChannelToToken,
    ) -> None:

        self._channel_type_to_adapter = {
            VkChannelAdapter.CHANNEL_TYPE: VkChannelAdapter(
                http_requester=http_requester,
                channel_to_token=channel_to_token,
            ),
            GithubChannelAdapter.CHANNEL_TYPE: GithubChannelAdapter(
                http_requester=http_requester,
                channel_to_token=channel_to_token,
            ),
        }

    @staticmethod
    def vk_channel_type() -> str:
        return VkChannelAdapter.CHANNEL_TYPE

    async def parse(self, request: ParsingRequest) -> Union[ParsingResponse, ParsingError]:

        channel_adapter = self._channel_type_to_adapter.get(request.channel)

        if channel_adapter is None:
            return ParsingError('invalid-channel')
        else:
            return await channel_adapter.parse(request)
