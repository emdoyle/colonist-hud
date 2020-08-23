from dataclasses import dataclass


@dataclass
class PlayerData:
    username: str
    is_bot: bool = False
