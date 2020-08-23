from typing import Dict

from games.observers.base import MessageObserver


class Identifier(MessageObserver):
    def __init__(self):
        self.identifier = None

    async def receive_default(self, message: Dict) -> None:
        self.identifier = message.get("player")  # unlikely to be correct behavior
        print(f"Identifier {id(self)}: {self.identifier}")
