from typing import Dict

from games.dataclasses.game import (
    GameBoard,
    GameTileCorner,
    GameTileEdge,
    GameTile,
    Point2D,
    Point3D,
)


def deserialize_tile_corner(json_data: Dict) -> GameTileCorner:
    return GameTileCorner(
        owner=json_data["owner"],
        hex_corner=Point3D.from_dict(json_data["hexCorner"]),
        harbor_type=json_data["harborType"],
        building_type=json_data["buildingType"],
    )


def deserialize_tile_edge(json_data: Dict) -> GameTileEdge:
    return GameTileEdge(
        type=json_data["type"],
        owner=json_data["owner"],
        hex_edge=Point3D.from_dict(json_data["hexEdge"]),
    )


def deserialize_game_tile(json_data: Dict) -> GameTile:
    return GameTile(
        hex_face=Point2D.from_dict(json_data["hexFace"]),
        tile_type=json_data["tileType"],
        tile_piece_types=json_data["tilePieceTypes"],
        dice_number=json_data["_diceNumber"],
        dice_probability=json_data.get("_diceProbability"),
    )


def deserialize_game_board(json_data: Dict) -> GameBoard:
    return GameBoard(
        tiles=[deserialize_game_tile(tile_data) for tile_data in json_data["tiles"]],
        tile_edges=[
            deserialize_tile_edge(tile_edge_data)
            for tile_edge_data in json_data["tileEdges"]
        ],
        tile_corners=[
            deserialize_tile_corner(tile_corner_data)
            for tile_corner_data in json_data["tileCorners"]
        ],
    )
