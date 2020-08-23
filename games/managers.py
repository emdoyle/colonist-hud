from django.db import models
from ingestion.constants import Opcode


class GameStateChangeManager(models.Manager):
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
