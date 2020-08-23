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
        # there could be an observer style architecture
        # where all the messages flow through a pipeline which observers can subscribe to
        # each one can decide whether to update its internal state based on the message
        # also need to be careful not to waste time on things that are only relevant to the offline ingested data
        # each observer can actually register for each individual message type separately... or together and perform
        # actions given the message
        # how will we handle the temporary state of the observers?
        # redis comes to mind, but database should work just as well
        # app starts up -> observers instantiate and subscribe -> so state can be held in memory on each observer
        # but observers should be able to dump to storage and be restored (later)
        # but also need separate observers for each game... instantiated and held separately
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
