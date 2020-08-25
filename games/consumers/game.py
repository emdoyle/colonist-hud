import asyncio
import json
from collections import defaultdict
from itertools import chain
from typing import Optional, List

from channels.generic.websocket import AsyncWebsocketConsumer

from games.dataclasses import PlayerData
from games.dataclasses.game import GameState, GameSettings, GameBoard
from games.observers.base import MessageObserver
from games.observers.counter import IncomeByPlayer
from ingestion.constants import Opcode


class GameEventConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.subscribers = defaultdict(list)
        self.broadcast_subscribers = []
        # TODO: this is actually built from messages... might need a special gamestatewriter observer
        self.game_state = GameState(
            players=[
                PlayerData(username="Jeff Bezos"),
                PlayerData(username="Joe Schmoe"),
            ],
            board=GameBoard(),
            settings=GameSettings(),
        )
        super().__init__(*args, **kwargs)

    def subscribe(
        self, subscriber: "MessageObserver", opcodes: Optional[List["Opcode"]] = None
    ) -> None:
        if opcodes is None:
            self.broadcast_subscribers.append(subscriber)
        else:
            for opcode in opcodes:
                self.subscribers[opcode].append(subscriber)

    async def connect(self):
        self.subscribe(IncomeByPlayer.from_game_state(game_state=self.game_state))
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(
        self, text_data: Optional[str] = None, bytes_data: Optional[bytes] = None
    ):
        text_data_json = json.loads(text_data)
        try:
            opcode = Opcode(text_data_json["id"])
        except TypeError:
            await self.send(
                json.dumps({"data": "Unrecognized message (looking for key 'id')"})
            )
            return
        coros = []
        for subscriber in chain(self.subscribers[opcode], self.broadcast_subscribers):
            coros.append(subscriber.receive(text_data_json))
        await asyncio.gather(*coros)
