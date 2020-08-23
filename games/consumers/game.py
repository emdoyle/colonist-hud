import json
from typing import Optional

from channels.generic.websocket import WebsocketConsumer


class GameEventConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(
        self, text_data: Optional[str] = None, bytes_data: Optional[bytes] = None
    ):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
