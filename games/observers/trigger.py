from games.dataclasses.game import GameState
from games.observers.base import MessageObserver


class Trigger(MessageObserver):
    def __init__(self, game_state: GameState, trigger: bool = False):
        super().__init__(game_state=game_state)
        self.trigger = trigger

    def __repr__(self):
        return f"{type(self).__name__}(id={id(self)}, trigger={self.trigger})"
