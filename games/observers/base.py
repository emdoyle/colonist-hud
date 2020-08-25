from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Type

from games.dataclasses.game import GameState
from ingestion.constants import Opcode

T = TypeVar("T")


class BaseMessageObserver(ABC):
    @classmethod
    @abstractmethod
    def from_game_state(cls: Type[T], game_state: GameState) -> T:
        ...

    @abstractmethod
    async def receive(self, message: Dict) -> None:
        ...


class MessageObserver(BaseMessageObserver):
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    @classmethod
    def from_game_state(cls: Type[T], game_state: GameState) -> T:
        return cls(game_state=game_state)

    async def receive_default(self, message: Dict) -> None:
        pass

    async def receive(self, message: Dict) -> None:
        try:
            opcode = Opcode(int(message.get("id", "-1")))
            data = message.get("data", {})
        except TypeError:
            return
        await getattr(self, f"receive_{opcode.name.lower()}", self.receive_default)(
            data
        )
