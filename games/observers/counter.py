from typing import Dict

from games.observers.base import MessageObserver


class Counter(MessageObserver):
    def __init__(self):
        self.quantity = 0

    async def receive_default(self, message: Dict) -> None:
        self.quantity += 1
        print(f"Counter {id(self)}: {self.quantity}")
