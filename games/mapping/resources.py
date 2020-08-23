from typing import Dict

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
