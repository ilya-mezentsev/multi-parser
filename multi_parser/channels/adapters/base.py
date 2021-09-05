import json
import logging
from abc import abstractmethod, ABCMeta
from typing import (
    Union,
    Optional,
    Mapping,
    Any,
)

from multi_parser.channels.shared import (
    IHttpRequester,
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


class BaseChannelAdapter(IChannelAdapter, metaclass=ABCMeta):
    CHANNEL_TYPE: str
    _DEFAULT_LOCALE = 'en'

    def __init__(
            self,
            http_requester: IHttpRequester,
            channel_to_token: ChannelToToken,
    ) -> None:

        self._http_requester = http_requester
        self._channel_to_token = channel_to_token

    async def parse(self, request: ParsingRequest) -> Union[ParsingResponse, ParsingError]:

        response = await self._http_requester.get(
            url=self._url(request.user_id),
            headers=self._headers(),
        )

        try:
            response_data = json.loads(response.body)
        except ValueError:
            logging.error(
                f'Unable to deserialize response data from {request.channel} channel: {response.body!r}')
            return self._make_unknown_error()

        if response.is_ok:
            return self._adapt_success_parsing_response(
                request=request,
                response_data=response_data,
            )

        else:
            logging.error(
                f'Got error from {request.channel} channel API: {response_data}')

            return self._adapt_error_parsing_response(response_data)

    @abstractmethod
    def _url(self, user_id: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def _headers() -> Optional[Mapping[str, Any]]:
        return None

    def _adapt_success_parsing_response(
            self,
            request: ParsingRequest,
            response_data: Mapping[str, Any],
    ) -> Union[ParsingResponse, ParsingError]:

        return ParsingResponse(
            channel_user_data=response_data,
        )

    def _adapt_error_parsing_response(self, response_data: Mapping[str, Any]) -> ParsingError:
        return self._make_unknown_error()

    @staticmethod
    def _make_unknown_error() -> ParsingError:
        return ParsingError(
            description='Unknown error',
        )
