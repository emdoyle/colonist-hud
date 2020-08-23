from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict


class ResourceMessage(ABC):
    @abstractmethod
    def get_income_updates(self) -> Dict[int, int]:
        ...


@dataclass
class ResourceReceived(ResourceMessage):
    color: int
    amount: int
    tile_index: int
    resource_type: int

    def get_income_updates(self) -> Dict[int, int]:
        # TODO: think about where this logic belongs. this message does not have enough info to tie to a player
        return {}


@dataclass
class Robbed(ResourceMessage):
    thief: int
    victim: int
    stolen_card: int

    def get_income_updates(self) -> Dict[int, int]:
        return {self.thief: 1}


@dataclass
class ResourceBought(ResourceMessage):
    card: int
    buyer: int

    def get_income_updates(self) -> Dict[int, int]:
        # TODO: need to find the payment made in another message
        return {self.buyer: 1}


@dataclass
class ResourceAmount:
    resource: int
    amount: int


@dataclass
class TradeCompleted(ResourceMessage):
    giving_cards: List[ResourceAmount]
    receiving_cards: List[ResourceAmount]
    giving_player: int
    receiving_player: Optional[int]  # None indicates trading with the bank

    def get_income_updates(self) -> Dict[int, int]:
        if self.receiving_player is not None:
            return {self.receiving_player: len(self.receiving_cards)}
        return {}
