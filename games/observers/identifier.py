from typing import Dict, Optional

from games.dataclasses.game import GameState
from games.observers.base import MessageObserver


class Identifier(MessageObserver):
    def __init__(self, game_state: GameState, identifier: Optional[str] = None):
        super().__init__(game_state=game_state)
        self.identifier = identifier

    def __repr__(self):
        return f"{type(self).__name__}(id={id(self)}, identifier={self.identifier})"

    async def receive_default(self, message: Dict) -> None:
        self.identifier = message.get("player")  # unlikely to be correct behavior
