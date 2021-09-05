import json
from abc import abstractmethod
from typing import (
    Union,
    Optional,
    Mapping,
    Any,
)

from multi_parser.channels.shared import (
    IHttpRequester,
    HttpResponse,
    HttpError,
    ChannelToToken,
)
from multi_parser.shared import (
    ParsingRequest,
    ParsingResponse,
    ParsingError,
)


__all__ = [
    'IChannelAdapter',
    'BaseChannelAdapter',
]


class IChannelAdapter:
    @abstractmethod
    async def parse(self, request: ParsingRequest) -> Union[ParsingResponse, ParsingError]:

        raise NotImplementedError()


class BaseChannelAdapter(IChannelAdapter):
    CHANNEL_TYPE: str

    def __init__(
            self,
            http_requester: IHttpRequester,
            channel_to_token: ChannelToToken,
    ) -> None:

        self._http_requester = http_requester
        self._channel_to_token = channel_to_token

    async def parse(self, request: ParsingRequest) -> Union[ParsingResponse, ParsingError]:

        response = await self._http_requester.get(
            url=self.url(request.user_id), headers=self.headers()
        )

        if isinstance(response, HttpResponse):
            return ParsingResponse(channel_user_data=json.loads(response.body),)

        elif isinstance(response, HttpError):
            return ParsingError(description=response.description,)

        else:
            raise RuntimeError(
                f'Unknown http response type: {type(response)}!r')

    @abstractmethod
    def url(self, user_id: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def headers() -> Optional[Mapping[str, Any]]:
        return None