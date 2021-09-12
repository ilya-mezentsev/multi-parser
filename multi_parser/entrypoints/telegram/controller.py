import logging
from typing import Sequence

from aiogram import Bot  # type: ignore
from aiogram.types import (  # type: ignore
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from multi_parser.channels import IChannelAdapter, I18n
from multi_parser.shared import (
    ParsingRequest,
    ParsingResponse,
    ParsingError,
)
from .states import IStateManager


__all__ = [
    'Controller',
]


class Controller:

    def __init__(
            self,
            bot: Bot,
            states_manager: IStateManager,
            available_channels: Sequence[str],
            channel_helper: IChannelAdapter,
            i18n: I18n,
    ) -> None:

        self._bot = bot
        self._available_channels = available_channels
        self._channel_helper = channel_helper
        self._i18n = i18n

        self._states_manager = states_manager

    async def on_keyboard_button(self, query: CallbackQuery) -> None:
        await self._on_user_input(
            chat_id=query.message.chat.id,
            user_id=query.from_user.id,
            data=query.data,
        )

    async def message_handler(self, message: Message):
        if message.text.startswith('/start'):
            await self._restart(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
            )

        else:
            await self._on_user_input(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                data=message.text,
            )

    async def _restart(
            self,
            chat_id: int,
            user_id: int,
    ) -> None:

        await self._states_manager.clean_state(user_id)

        await self._show_available_channels(chat_id)

    async def _show_available_channels(
            self,
            chat_id: int,
    ) -> None:

        keyboard_markup = InlineKeyboardMarkup(row_width=1)
        keyboard_markup.row(*(InlineKeyboardButton(
            text=channel_type,
            callback_data=channel_type,
        ) for channel_type in self._available_channels))

        await self._bot.send_message(
            chat_id=chat_id,
            text='Available channels:',
            reply_markup=keyboard_markup,
        )

    async def _on_user_input(
            self,
            chat_id: int,
            user_id: int,
            data: str,
    ) -> None:

        await self._states_manager.on_user_input(
            user_id=user_id,
            data=data,
        )

        if await self._states_manager.should_send_available_channels(user_id):
            await self._show_available_channels(chat_id)

        elif await self._states_manager.should_request_user_id(user_id):
            await self._request_user_id(chat_id)

        elif await self._states_manager.should_parse_user_data(user_id):
            await self._parse_channel_user_data(
                chat_id=chat_id,
                user_id=user_id,
            )

        else:
            logging.error(
                f'Unknown state (chat_id - {chat_id}, user_id - {user_id})')
            await self._on_unknown_situation(
                chat_id=chat_id,
                user_id=user_id,
            )

    async def _request_user_id(
            self,
            chat_id: int,
    ) -> None:

        await self._bot.send_message(
            chat_id=chat_id,
            text='Enter channel user id',
        )

    async def _parse_channel_user_data(
            self,
            chat_id: int,
            user_id: int,
    ) -> None:

        provided_data = await self._states_manager.all_provided_data(user_id)
        if provided_data is not None:
            request = ParsingRequest(
                channel=provided_data.channel,
                user_id=provided_data.user_id,
            )
            response = await self._channel_helper.parse(request)

            if isinstance(response, ParsingResponse):
                await self._bot.send_message(
                    chat_id=chat_id,
                    text=self._localize_parsing_response(
                        request=request,
                        response=response,
                    )
                )
                await self._restart(
                    chat_id=chat_id,
                    user_id=user_id,
                )

            elif isinstance(response, ParsingError):
                await self._bot.send_message(
                    chat_id=chat_id,
                    text=response.description,
                )

                await self._restart(
                    chat_id=chat_id,
                    user_id=user_id,
                )

            else:
                logging.error(f'Unknown response type: {type(response)!r}')
                await self._on_unknown_situation(
                    chat_id=chat_id,
                    user_id=user_id,
                )

        else:
            logging.error(
                f'provided_data is None but should not (chat_id - {chat_id}, user_id - {user_id})')
            await self._on_unknown_situation(
                chat_id=chat_id,
                user_id=user_id,
            )

    def _localize_parsing_response(
            self,
            request: ParsingRequest,
            response: ParsingResponse,
    ) -> str:

        localized_channel_user_data = self._i18n.translate_channel_user_data(
            request=request,
            parsing_response=response,
        ).localized_channel_user_data

        return '\n'.join([
            f'{key} - {value}'
            for key, value in localized_channel_user_data.items()
        ])

    async def _on_unknown_situation(
            self,
            chat_id: int,
            user_id: int,
    ) -> None:

        await self._bot.send_message(
            chat_id=chat_id,
            text='Something horrible happened. Please, try again.',
        )

        await self._restart(
            chat_id=chat_id,
            user_id=user_id,
        )
