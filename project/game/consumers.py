import json
from .models import Game
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # self.game_id = self.scope['url_route']['kwargs']['game_id']
        
        # try:
        #     game = Game.objects.get(game_id=self.game_id)
        #     print("\n\nJoin")
        #     game.players_count += 1
        #     game.save() 
        #     if game.players_count<=2:
        #         self.accept()
        #     else:
        #         self.send(text_data="full")
        # except Game.DoesNotExist:
        #     print(f"\n\nCreate")
        #     Game.objects.create(game_id=self.game_id, x_score=0, y_score=0, players_count=1)
        #     self.accept()
        # game = Game.objects.get(game_id=self.game_id)
        # game.save()

    async def disconnect(self, close_code):
        game = Game.objects.get(game_id=self.game_id)
        print(f"{game.players_count}sad")
        if game.players_count>0:
            game.players_count -= 1
            game.save()
        if game.players_count<=0:
            print("Delete")
            game.delete()
            game.save()

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]
    #     self.send(text_data=json.dumps({"message": message}))
