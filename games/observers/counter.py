from typing import Dict, Optional

from games.dataclasses.game import GameState
from games.mapping.resources import deserialize_resource_received
from games.observers.base import MessageObserver

# TODO not just integers


class Counter(MessageObserver):
    def __init__(self, game_state: GameState, quantity: Optional[int] = None):
        super().__init__(game_state=game_state)
        self.quantity = quantity if quantity is not None else 0


class CounterByPlayer(MessageObserver):
    def __init__(self, game_state: GameState):
        super().__init__(game_state=game_state)
        self.quantities = {player.username: 0 for player in game_state.players}


class IncomeByPlayer(CounterByPlayer):
    async def receive_resource_received(self, message: Dict):
        resource_received = deserialize_resource_received(message)
        try:
            self.quantities[
                self.game_state.player_for_tile_index(
                    resource_received.tile_index
                ).username
            ] += resource_received.amount
            print(f"IncomeByPlayer ({id(self)}): {self.quantities}")
        except KeyError:
            # TODO: logging
            print("Couldnt update quantities")
            pass
