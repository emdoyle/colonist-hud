from django import views
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from games.mapping.resources import RESOURCE_OPCODE_DISPATCH
from games.models import Game, GameStateChange
from games.services.resources import ResourceStatsService


class TotalIncomeAPIView(views.View):
    def get(self, request, game_slug: str, *args, **kwargs):
        get_object_or_404(Game, slug=game_slug)
        resource_messages = GameStateChange.objects.resource_income_for_game(
            game_slug=game_slug
        )
        deserialized_messages = [
            RESOURCE_OPCODE_DISPATCH[int(message["id"])](message["data"])
            for message in resource_messages
        ]
        total_income_per_player = ResourceStatsService.get_total_income_per_player(
            messages=deserialized_messages
        )
        return JsonResponse({"data": total_income_per_player})
