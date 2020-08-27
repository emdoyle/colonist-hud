from typing import Dict

from games.dataclasses.game import (
    GameBoard,
    GameTileCorner,
    GameTileEdge,
    GameTile,
    Point2D,
    Point3D,
)
from utils.serialization import keys_to_snake
from games.dataclasses import (
    ResourceReceived,
    Robbed,
    ResourceBought,
    TradeCompleted,
    ResourceAmount,
)


def deserialize_resource_received(json_data: Dict) -> ResourceReceived:
    return ResourceReceived(**keys_to_snake(json_data))


def deserialize_robbed(json_data: Dict) -> Robbed:
    return Robbed(**keys_to_snake(json_data))


def deserialize_resource_bought(json_data: Dict) -> ResourceBought:
    return ResourceBought(**keys_to_snake(json_data))


def deserialize_trade_completed(json_data: Dict) -> TradeCompleted:
    return TradeCompleted(
        giving_player=json_data["givingPlayer"],
        receiving_player=json_data["receivingPlayer"],
        giving_cards=[
            ResourceAmount(**resource_data)
            for resource_data in json_data["givingCards"]
        ],
        receiving_cards=[
            ResourceAmount(**resource_data)
            for resource_data in json_data["receivingCards"]
        ],
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
        has_robber=json_data["hasRobber"],
        dice_number=json_data["_diceNumber"],
        dice_probability=json_data["_diceProbability"],
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
