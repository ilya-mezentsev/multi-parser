from typing import (
    Optional,
    Mapping,
    Any,
)

import aiohttp

from multi_parser.channels.shared import (
    IHttpRequester,
    HttpResponse,
)


__all__ = [
    'HttpRequester',
]


class HttpRequester(IHttpRequester):
    async def get(
            self,
            url: str,
            headers: Optional[Mapping[str, Any]] = None
    ) -> HttpResponse:

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                headers=headers,
            ) as response:

                return HttpResponse(
                    body=(await response.text()),
                    is_ok=response.ok,
                )
