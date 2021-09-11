import logging
from typing import Sequence

import asyncio
from aiogram import (  # type: ignore
    Bot,
    Dispatcher,
    executor,
)

from multi_parser.channels import IChannelAdapter, I18n
from .controller import Controller
from .states import StatesManager


__all__ = [
    'run',
]


async def _clean_expired_states(
        states_manager: StatesManager,
        states_lifetime: int,
) -> None:

    while True:
        await asyncio.sleep(states_lifetime * 2)

        cleaned_count = await states_manager.clean_expired_states(states_lifetime)
        logging.info(f'Cleaned {cleaned_count} expired states')


async def _clean_expired_states_periodically(
        states_manager: StatesManager,
        states_lifetime: int,
) -> None:

    loop = asyncio.get_event_loop()
    task = loop.create_task(_clean_expired_states(
        states_manager=states_manager,
        states_lifetime=states_lifetime,
    ))

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass


def run(
        bot_token: str,
        states_lifetime: int,
        available_channels: Sequence[str],
        channel_helper: IChannelAdapter,
        i18n: I18n,
) -> None:

    bot: Bot = Bot(token=bot_token)
    dispatcher: Dispatcher = Dispatcher(bot)
    states_manager = StatesManager()
    controller = Controller(
        bot=bot,
        states_manager=states_manager,
        available_channels=available_channels,
        channel_helper=channel_helper,
        i18n=i18n,
    )

    dispatcher.register_message_handler(controller.message_handler)
    dispatcher.register_callback_query_handler(controller.on_keyboard_button)

    asyncio.run_coroutine_threadsafe(
        coro=_clean_expired_states_periodically(
            states_manager=states_manager,
            states_lifetime=states_lifetime,
        ),
        loop=asyncio.get_event_loop(),
    )

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=True,
    )
