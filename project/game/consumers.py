import json, time
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
                # await self.send(text_data=json.dumps({"message": self.game.state}))
                # await self.send(text_data=json.dumps(self.game.state))
                await self.channel_layer.group_send(
                    self.game_room,
                    {
                        "type": "play",
                        "message": self.game.state,
                        "current_turn": self.game.turn,
                        "game_result": "still playing",
                        "x_score": self.game.x_score,
                        "o_score": self.game.o_score,
                    },
                )
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
            if self.game.players_count > 1:
                self.game.players_count -= 1
                await sync_to_async(self.game.save)()
            else:
                print("Delete")
                await sync_to_async(self.game.delete)()
        pass

    async def receive(self, text_data):
        game_id = self.scope["url_route"]["kwargs"]["game_id"]
        game_room = await sync_to_async(Game.objects.get)(game_id=game_id)
        text_data_json = json.loads(text_data)
        id = text_data_json["id"]
        value = text_data_json["value"]
        ct = text_data_json["current_turn"]
        if id not in [
            "11",
            "12",
            "13",
            "21",
            "22",
            "23",
            "31",
            "32",
            "33",
        ] or value.lower() not in ["x", "o"]:
            print("Error")
            await self.close()
            return
        current_turn = "x" if ct.lower() == "o" else "o"
        game_room.turn = current_turn
        game_room.state[id] = value
        await sync_to_async(game_room.save)()
        game_result = self.game_result(game_room.state)
        if game_result.lower() == "x":
            game_room.x_score += 1
        elif game_result.lower() == "o":
            game_room.o_score += 1
        await sync_to_async(game_room.save)()
        await self.channel_layer.group_send(
            self.game_room,
            {
                "type": "play",
                "message": game_room.state,
                "current_turn": current_turn,
                "game_result": game_result,
                "x_score": game_room.x_score,
                "o_score": game_room.o_score,
            },
        )
        if game_result.lower() == "x" or game_result.lower() == "o" or game_result.lower()=="draw"  :
            game_room.state = {
                "11": "",
                "12": "",
                "13": "",
                "21": "",
                "22": "",
                "23": "",
                "31": "",
                "32": "",
                "33": "",
            }
            await self.channel_layer.group_send(
                self.game_room,
                {
                    "type": "play",
                    "message": game_room.state,
                    "current_turn": game_result,
                    "game_result": game_result if game_result.lower() in ["x", "o"] else current_turn,
                    "x_score": game_room.x_score,
                    "o_score": game_room.o_score,
                },
            )
            await sync_to_async(game_room.save)()

    async def play(self, event):
        # send message to SebSocket (front-end)
        await self.send(
            text_data=json.dumps(
                {
                    "state": event["message"],
                    "current_turn": event["current_turn"],
                    "game_result": event["game_result"],
                    "x_score": event["x_score"],
                    "o_score": event["o_score"],
                }
            )
        )

    @sync_to_async
    def get_game(self):
        self.game = Game.objects.get(game_id=self.game_id)

    @sync_to_async
    def create_game(self):
        Game.objects.create(game_id=self.game_id, x_score=0, o_score=0, players_count=1)

    def game_result(self, board):
        # Define winning combinations (rows, columns, diagonals)
        winning_combinations = [
            ["11", "12", "13"],
            ["21", "22", "23"],
            ["31", "32", "33"],  # Rows
            ["11", "21", "31"],
            ["12", "22", "32"],
            ["13", "23", "33"],  # Columns
            ["11", "22", "33"],
            ["13", "22", "31"],  # Diagonals
        ]

        # Check for a win
        for combination in winning_combinations:
            if all(board[pos] == "X" for pos in combination):
                return "X"
            elif all(board[pos] == "O" for pos in combination):
                return "O"

        # Check for a draw (if no empty spaces are left)
        if all(value != "" for value in board.values()):
            return "draw"

        # The game is still ongoing
        return "still playing"
