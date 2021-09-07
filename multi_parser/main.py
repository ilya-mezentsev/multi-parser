import os

from multi_parser.channels.shared import HttpRequester
from multi_parser.channels import ChannelHelper
from multi_parser.entrypoints import web
from multi_parser.logs import configure_logging
from multi_parser.settings import (
    cli_arguments,
    CLISettings,
    parse_resources,
)


__all__ = [
    'main',
]


def run_app(args: CLISettings) -> None:
    http_requester = HttpRequester()
    channel_to_token = {
        ChannelHelper.vk_channel_type(): os.environ['VK_ACCESS_TOKEN']
    }

    _channel_to_locales = parse_resources(args.resources_path)

    channel_helper = ChannelHelper(
        http_requester=http_requester,
        channel_to_token=channel_to_token,
    )

    web.run(
        channel_helper=channel_helper,
    )


def main() -> None:
    args = cli_arguments()

    configure_logging(args.logging_level)

    run_app(args)
