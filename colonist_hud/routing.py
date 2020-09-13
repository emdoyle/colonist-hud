import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter

import games.routing
from colonist_hud.lifespan import LifespanApplication

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colonist_hud.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "lifespan": LifespanApplication,
        "websocket": URLRouter(games.routing.websocket_urlpatterns),
    }
)
