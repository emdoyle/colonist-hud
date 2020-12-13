from dataclasses import dataclass, field
from typing import List, Dict, Optional

from .player import PlayerData


@dataclass
class Point3D:
    x: int
    y: int
    z: int

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(x=data["x"], y=data["y"], z=data["z"])


@dataclass
class Point2D:
    x: int
    y: int

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(x=data["x"], y=data["y"])


@dataclass
class GameTileCorner:
    owner: int
    hex_corner: Point3D
    harbor_type: int
    building_type: int


@dataclass
class GameTileEdge:
    type: int
    owner: int
    hex_edge: Point3D


@dataclass
class GameTile:
    hex_face: Point2D
    tile_type: int
    tile_piece_types: int
    dice_number: int
    dice_probability: Optional[int]

    @property
    def has_robber(self) -> bool:
        return self.tile_piece_types == 1


@dataclass
class GameBoard:
    tiles: List[GameTile] = field(default_factory=list)
    tile_edges: List[GameTileEdge] = field(default_factory=list)
    tile_corners: List[GameTileCorner] = field(default_factory=list)


@dataclass
class GameSettings:
    ...


@dataclass
class GameState:
    players: List[PlayerData] = field(default_factory=list)
    board: GameBoard = field(default_factory=GameBoard)
    settings: GameSettings = field(default_factory=GameSettings)
    initialized: bool = False

    def player_for_color(self, color: int) -> Optional[PlayerData]:
        return next((player for player in self.players if player.color == color), None)
