from abc import ABC, abstractmethod
from typing import Dict, Coroutine


class BaseMessageObserver(ABC):
    @abstractmethod
    async def receive(self, message: Dict) -> None:
        ...


class MessageObserver(BaseMessageObserver):
    BEHAVIOR_MAP = {}  # type: Dict[int, Coroutine]

    async def receive_default(self, message: Dict) -> None:
        pass

    async def receive(self, message: Dict) -> None:
        await self.BEHAVIOR_MAP.get(int(message.get("id", "-1")), self.receive_default)(
            message.get("data", {})
        )
