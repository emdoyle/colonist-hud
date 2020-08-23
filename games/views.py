from django import views
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from games.mapping.resources import RESOURCE_OPCODE_DISPATCH
from games.models import Game, GameStateChange


class TotalIncomeAPIView(views.View):
    # provided a game slug
    # lookup the game, raise 404 if not found
    # run a query for all resource related messages
    # deserialize all of these messages
    # run functions on the deserialized messages to get {<player_id>: int}
    def get(self, request, game_slug: str, *args, **kwargs):
        get_object_or_404(Game, slug=game_slug)
        resource_messages = GameStateChange.objects.resource_income_for_game(
            game_slug=game_slug
        )
        deserialized_messages = [
            RESOURCE_OPCODE_DISPATCH[int(message["id"])](message["data"])
            for message in resource_messages
        ]
        return JsonResponse(
            {"data": [str(message) for message in deserialized_messages]}
        )
