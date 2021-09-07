from aiohttp import web

from multi_parser.channels import ChannelHelper
from multi_parser.entrypoints.web.controller import Controller


__all__ = [
    'run',
]


def run(
        channel_helper: ChannelHelper,
) -> None:

    app = web.Application()

    controller = Controller(
        channel_helper=channel_helper,
    )

    app.add_routes([
        web.get('/{channel}/{user_id}', controller.parse_channel_user_data)
    ])

    web.run_app(app)
