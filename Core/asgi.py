import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,

    'websocket': URLRouter(
        app.routing.websocket_urlpatterns
    )

})