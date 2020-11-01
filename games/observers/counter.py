from collections import defaultdict
from typing import Dict, Optional, Any

from games.dataclasses.game import GameState
from games.mapping.dice import deserialize_dice_state_change
from games.mapping.resources import deserialize_resource_received
from games.observers.base import MessageObserver

# TODO not just integers


class Counter(MessageObserver):
    KEY = "counter"

    def __init__(self, game_state: GameState, quantity: Optional[int] = None):
        super().__init__(game_state=game_state)
        self.quantity = quantity if quantity is not None else 0

    def __repr__(self):
        return f"{type(self).__name__}(id={id(self)}, quantity={self.quantity})"

    @property
    def data(self) -> Dict:
        return {self.KEY: self.quantity}


class CounterByKey(MessageObserver):
    KEY = "counter_by_key"

    def __init__(self, game_state: GameState):
        super().__init__(game_state=game_state)
        self.quantities = defaultdict(int)

    def __repr__(self):
        return (
            f"{type(self).__name__}(id={id(self)}, quantities={dict(self.quantities)})"
        )

    @property
    def data(self) -> Dict:
        return {self.KEY: self.quantities}


class IncomeByPlayer(CounterByKey):
    KEY = "income_by_player"

    async def receive_resource_received(self, message: Dict):
        resource_received = deserialize_resource_received(message)
        try:
            self.quantities[
                self.game_state.player_for_color(resource_received.color).username
            ] += resource_received.amount
            return self.data
        except AttributeError:
            print("Couldnt update quantities")


class Turns(Counter):
    KEY = "turns"

    def __init__(self, game_state: GameState, quantity: Optional[int] = None):
        super().__init__(game_state=game_state, quantity=quantity)
        self.previous_player_color = None

    async def receive_turn_state_change(self, message: Dict):
        current_player_color = message["currentTurnPlayerColor"]
        if current_player_color != self.previous_player_color:
            self.quantity += 1
            self.previous_player_color = current_player_color
            return self.data


class Dice(CounterByKey):
    KEY = "dice"

    async def receive_dice_state_change(self, message: Dict):
        dice_change = deserialize_dice_state_change(message)
        if dice_change.dice_thrown:
            self.quantities[dice_change.total_roll] += 1
            return self.data
