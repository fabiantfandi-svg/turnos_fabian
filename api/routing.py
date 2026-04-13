# api/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # QUITA el .as_view()
    re_path(r'ws/alertas/$', consumers.AlertaConsumer.as_asgi()), 
]