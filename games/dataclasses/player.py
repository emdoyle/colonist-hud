from dataclasses import dataclass


@dataclass
class PlayerData:
    username: str
    color: int
    is_bot: bool = False
