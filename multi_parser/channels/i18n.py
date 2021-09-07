from multi_parser.settings import ChannelToLocales
from multi_parser.shared import (
    ParsingResponse,
    LocalizedParsingResponse,
    ParsingRequest,
)


class I18n:

    _DEFAULT_LOCALE = 'en'

    def __init__(
            self,
            channel_to_locales: ChannelToLocales,
    ) -> None:

        self._channel_to_locales = channel_to_locales

    def translate_channel_user_data(
            self,
            request: ParsingRequest,
            parsing_response: ParsingResponse
    ) -> LocalizedParsingResponse:

        localized_channel_user_data = {}
        if request.channel in self._channel_to_locales:
            channel_locales = self._channel_to_locales[request.channel]
            for field, locale_field in channel_locales.items():
                localized_channel_user_data[locale_field[self._DEFAULT_LOCALE]] = \
                    parsing_response.channel_user_data[field]

        return LocalizedParsingResponse(
            localized_channel_user_data=localized_channel_user_data or parsing_response.channel_user_data,
        )
