from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from games.mapping.resources import RESOURCE_OPCODE_DISPATCH
from games.models import Game, GameStateChange
from games.services.resources import ResourceStatsService


async def total_income_api_view(request, game_slug: str, *args, **kwargs):
    await sync_to_async(get_object_or_404)(Game, slug=game_slug)
    resource_messages = await sync_to_async(
        GameStateChange.objects.resource_income_for_game
    )(game_slug=game_slug)
    deserialized_messages = [
        RESOURCE_OPCODE_DISPATCH[int(message["id"])](message["data"])
        for message in resource_messages
    ]
    total_income_per_player = await sync_to_async(
        ResourceStatsService.get_total_income_per_player
    )(messages=deserialized_messages)
    return JsonResponse({"data": total_income_per_player})
