from typing import Optional, Mapping, Any, Union

import aiohttp

from multi_parser.channels.shared import (
    IHttpRequester,
    HttpResponse,
    HttpError,
)


__all__ = [
    'HttpRequester',
]


class HttpRequester(IHttpRequester):
    async def get(
            self,
            url: str,
            headers: Optional[Mapping[str, Any]] = None
    ) -> Union[HttpResponse, HttpError]:

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                headers=headers,
            ) as response:

                return HttpResponse(
                    body=(await response.text())
                )
