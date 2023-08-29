import json
from .models import Game
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_room = f"game_{self.game_id}"

        await self.channel_layer.group_add(self.game_room, self.channel_name)

        try:
            await self.get_game()
            print(f"\n\nJoin\n")
            if self.game.players_count < 2:
                await self.accept()
                await self.send(text_data=json.dumps(self.game.state))
                self.game.players_count += 1
                await sync_to_async(self.game.save)()
                await self.send(text_data="o")
            else:
                print(f"\n\nfull\n")
                await self.close()
        except Game.DoesNotExist:
            print(f"\n\nCreate")
            await self.create_game()
            await self.accept()
            await self.send(text_data="x")

    async def disconnect(self, code):
        if code != 1006:
            print("\n\ndis")
            await self.get_game()
            print(f"\n\n{self.game.players_count}\n")
            if self.game.players_count > 1:
                self.game.players_count -= 1
                await (sync_to_async(self.game.save)())
            else:
                print("Delete")
                await (sync_to_async(self.game.delete)())
        pass

    async def receive(self, text_data):
        game_id = self.scope["url_route"]["kwargs"]["game_id"]
        game_room = await sync_to_async(Game.objects.get)(game_id=game_id)
        text_data_json = json.loads(text_data)
        id = text_data_json["id"]
        value = text_data_json["value"]
        print(id, value)
        game_room.state[id] = value
        await sync_to_async(game_room.save)()
        print(game_room.state)
        await self.channel_layer.group_send(
            self.game_room, {
                "type": "play",
                "message": game_room.state
                }
        )
        # await self.send(text_data=json.dumps())
        # pass

    async def play(self, event):
        # send message to SebSocket (front-end)
        await self.send(text_data=json.dumps(event['message']))

    @sync_to_async
    def get_game(self):
        self.game = Game.objects.get(game_id=self.game_id)

    @sync_to_async
    def create_game(self):
        Game.objects.create(game_id=self.game_id, x_score=0, y_score=0, players_count=1)
