from typing import Dict

from games.observers.base import MessageObserver


class Trigger(MessageObserver):
    def __init__(self):
        self.trigger = False

    async def receive_default(self, message: Dict) -> None:
        print(f"Trigger {id(self)}: {self.trigger}")
