import asyncio
import json
from collections import defaultdict
from itertools import chain
from typing import Optional, List, Iterable, Dict

from channels.generic.websocket import AsyncWebsocketConsumer

from games.dataclasses.game import GameState
from games.observers.base import MessageObserver
from games.observers.counter import IncomeByPlayer, Turns, Dice
from games.observers.game_state import GameStateWriter
from ingestion.constants import Opcode


class GameEventConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.subscribers = defaultdict(list)
        self.broadcast_subscribers = []
        self.game_state = GameState()
        super().__init__(*args, **kwargs)

    def subscribe(
        self, subscriber: "MessageObserver", opcodes: Optional[List["Opcode"]] = None
    ) -> None:
        if opcodes is None:
            self.broadcast_subscribers.append(subscriber)
        else:
            for opcode in opcodes:
                self.subscribers[opcode].append(subscriber)

    @property
    def all_subscribers(self) -> Iterable:
        return chain(*self.subscribers.values(), self.broadcast_subscribers)

    @property
    def subscriber_data(self) -> Dict:
        return {
            key: value
            for subscriber in self.all_subscribers
            for key, value in subscriber.data.items()
            if subscriber.data
        }

    async def connect(self):
        self.subscribe(GameStateWriter.from_game_state(game_state=self.game_state))
        self.subscribe(
            IncomeByPlayer.from_game_state(game_state=self.game_state),
            opcodes=[Opcode.RESOURCE_RECEIVED],
        )
        self.subscribe(
            Turns.from_game_state(game_state=self.game_state),
            opcodes=[Opcode.TURN_STATE_CHANGE],
        )
        self.subscribe(
            Dice.from_game_state(game_state=self.game_state),
            opcodes=[Opcode.DICE_STATE_CHANGE],
        )
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(
        self, text_data: Optional[str] = None, bytes_data: Optional[bytes] = None
    ):
        text_data_json = json.loads(text_data)
        try:
            opcode = Opcode(int(text_data_json["id"]))
        except KeyError:
            if "recv" in text_data_json:
                await self.send(json.dumps(self.subscriber_data))
                return
            await self.send(
                json.dumps({"data": "Unrecognized message (looking for key 'id')"})
            )
            return
        except ValueError:
            print(f"This opcode is not catalogued {text_data_json['id']}")
            return
        coros = []
        for subscriber in chain(self.subscribers[opcode], self.broadcast_subscribers):
            coros.append(subscriber.receive(text_data_json))
        await asyncio.gather(*coros)
