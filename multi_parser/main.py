import logging
import os

from multi_parser.channels.shared import HttpRequester
from multi_parser.channels import ChannelHelper, I18n
from multi_parser.entrypoints import (
    web_run,
    telegram_run,
)
from multi_parser.logs import configure_logging
from multi_parser.settings import (
    cli_arguments,
    CLISettings,
    parse_resources,
)


__all__ = [
    'main',
]


class AppModes:
    WEB = 'web'
    TELEGRAM = 'telegram'

    ALL = {
        WEB,
        TELEGRAM,
    }


def _run_telegram(
    bot_token: str,
    states_lifetime: int,
    args: CLISettings,
    channel_helper: ChannelHelper,
) -> None:
    channel_to_locales = parse_resources(args.resources_path)
    i18n = I18n(channel_to_locales)

    telegram_run(
        bot_token=bot_token,
        states_lifetime=states_lifetime,
        available_channels=channel_helper.available_channels_types(),
        channel_helper=channel_helper,
        i18n=i18n,
    )


def main() -> None:
    args = cli_arguments()

    if args.mode not in AppModes.ALL:
        logging.error(f'Unknown mode - {args.mode}')
        return

    configure_logging(args.logging_level)

    channel_helper = ChannelHelper(
        http_requester=HttpRequester(),
        channel_to_token={
            ChannelHelper.vk_channel_type(): os.environ.get('VK_ACCESS_TOKEN')
        },
    )

    logging.info(f'Starting in mode: {args.mode}')

    if args.mode == AppModes.WEB:
        web_run(channel_helper)

    elif args.mode == AppModes.TELEGRAM:
        if 'TELEGRAM_BOT_TOKEN' in os.environ:
            _run_telegram(
                bot_token=os.environ['TELEGRAM_BOT_TOKEN'],
                states_lifetime=int(os.environ.get(
                    'TELEGRAM_USER_STATES_LIFETIME', 10)),
                args=args,
                channel_helper=channel_helper,
            )

        else:
            logging.error('Unable to start telegram bot without token')
