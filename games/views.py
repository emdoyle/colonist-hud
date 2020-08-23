from django import views
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from games.models import Game


class TotalIncomeAPIView(views.View):
    # provided a game slug
    # lookup the game, raise 404 if not found
    # run a query for all resource related messages
    # deserialize all of these messages
    # run functions on the deserialized messages to get {<player_id>: int}
    def get(self, request, game_slug: str, *args, **kwargs):
        game = get_object_or_404(Game, slug=game_slug)
        return JsonResponse({"data": str(game)})
