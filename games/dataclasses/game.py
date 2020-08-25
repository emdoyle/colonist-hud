from dataclasses import dataclass
from typing import List

from .player import PlayerData


@dataclass
class GameBoard:
    ...

    def player_for_tile_index(self, tile_index: int) -> PlayerData:
        return PlayerData(username="Jeff Bezos")


@dataclass
class GameSettings:
    ...


@dataclass
class GameState:
    players: List[PlayerData]
    board: GameBoard
    settings: GameSettings

    def player_for_tile_index(self, tile_index: int) -> PlayerData:
        return self.board.player_for_tile_index(tile_index)
