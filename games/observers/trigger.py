from typing import Dict

from games.dataclasses.game import GameState
from games.observers.base import MessageObserver


class Trigger(MessageObserver):
    def __init__(self, game_state: GameState, trigger: bool = False):
        super().__init__(game_state=game_state)
        self.trigger = trigger

    async def receive_default(self, message: Dict) -> None:
        print(f"Trigger {id(self)}: {self.trigger}")
