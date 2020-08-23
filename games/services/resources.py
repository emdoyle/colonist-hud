from typing import Dict, List

from games.dataclasses import ResourceMessage


class ResourceStatsService:
    @classmethod
    def get_total_income_per_player(
        cls, messages: List[ResourceMessage]
    ) -> Dict[int, int]:
        total_income_per_player = {}
        for message in messages:
            total_income_per_player.update(message.get_income_updates())
        return total_income_per_player
