import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter

import games.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colonist_hud.settings")
django.setup()

application = ProtocolTypeRouter(
    {"websocket": URLRouter(games.routing.websocket_urlpatterns)}
)
