from abc import ABC, abstractmethod
from typing import Dict, TypeVar, Type, Any

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

    @property
    def data(self) -> Any:
        return None


class MessageObserver(BaseMessageObserver):
    """
    The base concrete implementation of a BaseMessageObserver.

    It adds game_state as an instance variable, and defines a simple mapping
    of methods to opcodes by name.

    When a message is received with an opcode named RESOURCE_RECEIVED for example,
    the class will look for a method called receive_resource_received, and otherwise use
    receive_default.

    The message is passed as the only argument to receiving functions.
    """

    def __init__(self, game_state: GameState):
        # TODO: fancy property/inheritance stuff to block writes except from GameStateWriter
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
