from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ResourceReceived:
    color: int
    amount: int
    tile_index: int
    resource_type: int


@dataclass
class Robbed:
    thief: int
    victim: int
    stolen_card: int


@dataclass
class ResourceBought:
    card: int
    buyer: int


@dataclass
class ResourceAmount:
    resource: int
    amount: int


@dataclass
class TradeCompleted:
    giving_cards: List[ResourceAmount]
    receiving_cards: List[ResourceAmount]
    giving_player: int
    receiving_player: Optional[int]  # None indicates trading with the bank
