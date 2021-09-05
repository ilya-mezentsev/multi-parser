from abc import abstractmethod
from dataclasses import dataclass
from typing import (
    Union,
    Optional,
    Mapping,
    Any,
)


__all__ = [
    'IHttpRequester',
    'HttpResponse',
    'HttpError',
]


class IHttpRequester:
    @abstractmethod
    async def get(
            self,
            url: str,
            headers: Optional[Mapping[str, Any]] = None,
    ) -> Union['HttpResponse', 'HttpError']:

        raise NotImplementedError()


@dataclass
class HttpResponse:
    body: str


@dataclass
class HttpError:
    description: str
