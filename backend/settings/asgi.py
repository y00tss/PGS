"""
ASGI config for PAF project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from tasks.consumers import TaskConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/tasks/", TaskConsumer.as_asgi()),
    ]),
})
