import os

from multi_parser.channels import HttpRequester, ChannelHelper
from multi_parser.entrypoints import web


__all__ = [
    'main',
]


def run_app() -> None:
    http_requester = HttpRequester()
    channel_to_token = {
        ChannelHelper.vk_channel_type(): os.environ['VK_ACCESS_TOKEN']
    }

    channel_helper = ChannelHelper(
        http_requester=http_requester,
        channel_to_token=channel_to_token,
    )

    web.run(
        channel_helper=channel_helper,
    )


def main() -> None:
    run_app()
