from typing import Dict

from games.dataclasses.dice import DiceChange


def deserialize_dice_state_change(json_data: Dict) -> DiceChange:
    return DiceChange(
        dice_thrown=json_data["diceThrown"],
        last_dice_1=int(json_data["lastDice1"]),
        last_dice_2=int(json_data["lastDice2"]),
    )
