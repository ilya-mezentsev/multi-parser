from .base import BaseChannelAdapter


__all__ = [
    'VkChannelAdapter',
]


class VkChannelAdapter(BaseChannelAdapter):

    CHANNEL_TYPE = 'vk'

    def url(self, user_id: str) -> str:
        return (
            f'https://api.vk.com/method/users.get?v=5.131&user_ids={user_id}'
            f'&access_token={self._channel_to_token[self.CHANNEL_TYPE]}'
            f'&fields=bdate,screen_name,sex,timezone,photo_max_orig,online'
        )
