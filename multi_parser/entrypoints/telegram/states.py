import time
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from dataclasses import dataclass

from asyncio import locks
from typing import Optional


class IStateManager(metaclass=ABCMeta):

    @abstractmethod
    async def on_user_input(
            self,
            user_id: int,
            data: str,
    ) -> None:

        raise NotImplementedError()

    @abstractmethod
    async def should_send_available_channels(self, user_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def should_request_user_id(self, user_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def should_parse_user_data(self, user_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def clean_state(self, user_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def all_provided_data(self, user_id: int) -> Optional['AllDataProvidedState']:
        raise NotImplementedError()


class StatesManager(IStateManager):
    _user_states: defaultdict[int, 'UserState']

    def __init__(self) -> None:
        self._user_states = defaultdict(self._create_initial_state)
        self._user_states_lock = locks.Lock()

    @staticmethod
    def _create_initial_state() -> 'UserState':
        return InitialState(
            last_update_ts=time.time(),
        )

    async def clean_expired_states(self, lifetime: float) -> int:
        now = time.time()
        clean_user_ids = []

        async with self._user_states_lock:
            for user_id, state in self._user_states.items():
                if state.last_update_ts + lifetime < now:
                    clean_user_ids.append(user_id)

            for clean_user_id in clean_user_ids:
                self._user_states.pop(clean_user_id)

        return len(clean_user_ids)

    async def on_user_input(
            self,
            user_id: int,
            data: str,
    ) -> None:

        async with self._user_states_lock:
            self._on_user_input(
                user_id=user_id,
                data=data,
            )

    def _on_user_input(
            self,
            user_id: int,
            data: str,
    ) -> None:

        assert self._user_states_lock.locked()

        current_state = self._user_states[user_id]
        now = time.time()
        new_state: UserState

        if isinstance(current_state, InitialState):
            new_state = ChannelSelectedState(
                channel=data,
                last_update_ts=now,
            )

        elif isinstance(current_state, ChannelSelectedState):
            new_state = AllDataProvidedState(
                channel=current_state.channel,
                user_id=data,
                last_update_ts=now,
            )

        else:
            new_state = self._create_initial_state()

        self._user_states[user_id] = new_state

    async def should_send_available_channels(self, user_id: int) -> bool:
        async with self._user_states_lock:
            return isinstance(self._user_states[user_id], InitialState)

    async def should_request_user_id(self, user_id: int) -> bool:
        async with self._user_states_lock:
            return isinstance(self._user_states[user_id], ChannelSelectedState)

    async def should_parse_user_data(self, user_id: int) -> bool:
        async with self._user_states_lock:
            return isinstance(self._user_states[user_id], AllDataProvidedState)

    async def clean_state(self, user_id: int) -> None:
        async with self._user_states_lock:
            self._user_states[user_id] = self._create_initial_state()

    async def all_provided_data(self, user_id: int) -> Optional['AllDataProvidedState']:
        async with self._user_states_lock:
            current_state = self._user_states[user_id]

            if isinstance(current_state, AllDataProvidedState):
                return current_state

            else:
                return None


@dataclass
class UserState(metaclass=ABCMeta):
    last_update_ts: float


@dataclass
class InitialState(UserState):
    pass


@dataclass
class ChannelSelectedState(UserState):
    channel: str


@dataclass
class AllDataProvidedState(UserState):
    channel: str
    user_id: str
