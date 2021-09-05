from abc import abstractmethod
from dataclasses import dataclass
from typing import (
    Optional,
    Mapping,
    Any,
)


__all__ = [
    'IHttpRequester',
    'HttpResponse',
]


class IHttpRequester:
    @abstractmethod
    async def get(
            self,
            url: str,
            headers: Optional[Mapping[str, Any]] = None,
    ) -> 'HttpResponse':

        raise NotImplementedError()


@dataclass
class HttpResponse:
    is_ok: bool
    body: str
