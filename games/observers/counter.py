from collections import defaultdict
from typing import Dict, Optional, Any

from games.dataclasses.game import GameState
from games.mapping.resources import deserialize_resource_received
from games.observers.base import MessageObserver

# TODO not just integers


class Counter(MessageObserver):
    def __init__(self, game_state: GameState, quantity: Optional[int] = None):
        super().__init__(game_state=game_state)
        self.quantity = quantity if quantity is not None else 0

    @property
    def data(self) -> Any:
        return self.quantity


class CounterByPlayer(MessageObserver):
    def __init__(self, game_state: GameState):
        super().__init__(game_state=game_state)
        self.quantities = defaultdict(int)

    @property
    def data(self) -> Any:
        return self.quantities


class IncomeByPlayer(CounterByPlayer):
    async def receive_resource_received(self, message: Dict):
        if not self.game_state.initialized:
            # build this into difference in type system
            return
        resource_received = deserialize_resource_received(message)
        try:
            self.quantities[
                self.game_state.player_for_color(resource_received.color).username
            ] += resource_received.amount
            print(f"IncomeByPlayer ({id(self)}): {self.quantities}")
        except AttributeError:
            # TODO: logging
            print("Couldnt update quantities")


class Turns(Counter):
    def __init__(self, game_state: GameState, quantity: Optional[int] = None):
        super().__init__(game_state=game_state)
        self.previous_player_color = None

    async def receive_turn_state_change(self, message: Dict):
        # need to check for change in player color
        current_player_color = message["currentTurnPlayerColor"]
        if current_player_color != self.previous_player_color:
            self.quantity += 1
            self.previous_player_color = current_player_color
            print(f"Turns ({id(self)}): {self.quantity}")
