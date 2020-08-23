import json

import requests
import re

import websocket
from typing import Optional, List, Any

from asgiref.sync import sync_to_async

from games.dataclasses import PlayerData
from games.mapping.player import deserialize_player_data
from games.models import Player, Game, PlayerInGame, GameStateChange
from ingestion.constants import OPCODES_BY_VALUE, Opcode, SendingOpcode


class WebsocketIngest:
    def __init__(self, cookie: Optional[str] = None):
        self.cookie = cookie or ""
        self.websocket = None
        self.game_slug = ""
        self.game_id = None

    def _get_cookie(self, http_target: str) -> str:
        response = requests.get(http_target)
        if response.status_code != 200:
            print("Could not get cookie!")
            raise ValueError
        full_cookie = response.headers["set-cookie"]
        jwt = re.search(r"jwt=[^\s]*;", full_cookie)
        return jwt.group(0)

    def _create_initial_game_objects(self, players: List["PlayerData"]) -> None:
        game = Game.objects.create(slug=self.game_slug)
        self.game_id = game.id
        for player in players:
            new_player = Player.objects.create(
                username=player.username, is_bot=player.is_bot
            )
            PlayerInGame.objects.create(game=game, player=new_player)

    def _handle_text(self, message: str) -> None:
        if "game not found" in message.lower():
            self.game_slug = None

    def _on_message(self, message):
        json_message = json.loads(message)
        json_data = json_message.get("data")
        json_id = json_message.get("id", "-1")
        opcode = OPCODES_BY_VALUE.get(json_id, Opcode.UNKNOWN)
        if opcode is Opcode.SINGLE_GAME_LISTING and not self.game_slug:
            self.game_slug = json_data
            self._send(data=json_data, opcode=SendingOpcode.JOIN_GAME)
        elif opcode is Opcode.TEXT:
            self._handle_text(json_data.get("text", ""))
        elif opcode is Opcode.PLAYER_INFO and not self.game_id:
            player_data = deserialize_player_data(json_data=json_data)
            self._create_initial_game_objects(players=player_data)
        elif opcode is Opcode.UNKNOWN:
            print(f"Unknown message: {json_id}")
            if self.game_id is not None:
                GameStateChange.objects.create(
                    game_id=self.game_id, message={"id": json_id, "data": json_data}
                )
            else:
                print(f"pre-game {json_data}")
        else:
            if self.game_id is not None:
                GameStateChange.objects.create(
                    game_id=self.game_id, message={"id": json_id, "data": json_data}
                )

    def _on_error(self, error):
        print(f"Websocket error!\n{error}")
        self.websocket.close()

    def _on_close(self):
        print("Websocket closed!")

    def _on_open(self):
        print("Websocket opened!")
        self._send(data=True, opcode=SendingOpcode.INIT_ONE)
        self._send(data=True, opcode=SendingOpcode.INIT_TWO)

    def _send(self, data: Any, opcode: "SendingOpcode"):
        self.websocket.send(json.dumps({"id": opcode.value, "data": data}))

    @sync_to_async
    def open(self, target: str, http_target: str) -> None:
        self.websocket = websocket.WebSocketApp(
            target,
            cookie=self._get_cookie(http_target=http_target),
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self.websocket.on_open = self._on_open
        self.websocket.run_forever()
