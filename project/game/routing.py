from django.urls import path, include
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:game_id>/', consumers.GameConsumer.as_asgi()),
]