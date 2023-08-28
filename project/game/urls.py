from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="game"

urlpatterns = [
    path("", views.create_game, {}),
    path("game/<str:game_id>", views.game, {})
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
