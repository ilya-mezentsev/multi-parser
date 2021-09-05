import os

import asyncio

from multi_parser.channels import HttpRequester, ChannelHelper
from multi_parser.shared import ParsingRequest


__all__ = [
    'main',
]


async def run_app() -> None:
    http_requester = HttpRequester()
    channel_to_token = {
        ChannelHelper.vk_channel_type(): os.environ['VK_ACCESS_TOKEN']
    }

    channel_helper = ChannelHelper(
        http_requester=http_requester,
        channel_to_token=channel_to_token,
    )

    response = await channel_helper.parse(ParsingRequest(
        channel='github',
        user_id='ilya-mezentsev',
    ))

    print(f'{response!r}')


def main() -> None:
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_app())
