from django.shortcuts import render, redirect
from uuid import uuid4

def create_game(request):
    return redirect(f"game/{str(uuid4())}")

def game(request, game_id):
    return render(request, "game.html", {"game_id": game_id})