import os
import django
from channels.routing import ProtocolTypeRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colonist_hud.settings")
django.setup()

application = ProtocolTypeRouter({})
