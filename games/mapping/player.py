from typing import Dict, List

from games.dataclasses import PlayerData


def deserialize_player_data(json_data: Dict) -> List["PlayerData"]:
    return [
        PlayerData(username=data["playerName"], is_bot=data["isBot"])
        for data in json_data
    ]
