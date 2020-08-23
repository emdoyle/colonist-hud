from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path("ws/api/game/<slug:game_slug>/", consumers.GameEventConsumer)
]
