from dataclasses import dataclass


@dataclass
class DiceChange:
    dice_thrown: bool
    last_dice_1: int
    last_dice_2: int

    @property
    def total_roll(self) -> int:
        return self.last_dice_1 + self.last_dice_2
