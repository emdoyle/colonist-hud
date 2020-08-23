import asyncio
import json
from collections import defaultdict
from typing import Optional, List

from channels.generic.websocket import AsyncWebsocketConsumer

from games.observers.base import MessageObserver
from games.observers.counter import Counter
from games.observers.identifier import Identifier
from games.observers.trigger import Trigger
from ingestion.constants import Opcode


# TODO subscribers need to be instantiated and registered at the beginning of a websocket connection (or during)


class GameEventConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.subscribers = defaultdict(list)
        super().__init__(*args, **kwargs)

    def subscribe(
        self, subscriber: "MessageObserver", opcodes: Optional[List["Opcode"]] = None
    ) -> None:
        if opcodes is None:
            opcodes = [None]
        for opcode in opcodes:
            self.subscribers[opcode].append(subscriber)

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(
        self, text_data: Optional[str] = None, bytes_data: Optional[bytes] = None
    ):
        self.subscribe(Counter(), [Opcode.INIT_ONE])
        self.subscribe(Identifier(), [Opcode.INIT_ONE])
        self.subscribe(Trigger(), [Opcode.INIT_ONE])
        text_data_json = json.loads(text_data)
        opcode = Opcode(text_data_json["id"]) if "id" in text_data_json else None
        coros = []
        for subscriber in self.subscribers[opcode]:
            coros.append(subscriber.receive(text_data_json))
        await asyncio.gather(*coros)
