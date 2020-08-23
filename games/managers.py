from typing import Dict, List

from django.db import models
from ingestion.constants import Opcode


class GameStateChangeQuerySet(models.QuerySet):
    RESOURCE_INCOME_OPCODES = [
        str(opcode.value)
        for opcode in (
            Opcode.RESOURCE_RECEIVED,
            Opcode.ROBBED,
            Opcode.RESOURCE_BOUGHT,
            Opcode.TRADE_COMPLETED,
        )
    ]

    def for_resource_income(self) -> "models.QuerySet":
        return self.filter(message__id__in=self.RESOURCE_INCOME_OPCODES)

    def for_game(self, game_slug: str) -> "models.QuerySet":
        return self.filter(game__slug=game_slug)


class GameStateChangeManager(models.Manager.from_queryset(GameStateChangeQuerySet)):
    def resource_income_for_game(self, game_slug: str) -> List[Dict]:
        return list(
            self.for_game(game_slug=game_slug)
            .for_resource_income()
            .values_list("message", flat=True)
        )
