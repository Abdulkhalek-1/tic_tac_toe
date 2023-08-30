from django.db import models

class Game(models.Model):
    
    def init_status():
        return {
        "11":"",
        "21":"",
        "31":"",
        "12":"",
        "22":"",
        "32":"",
        "13":"",
        "23":"",
        "33":""
    }
    game_id = models.CharField(primary_key=True, max_length=255)
    x_score = models.IntegerField()
    o_score = models.IntegerField()
    players_count = models.IntegerField()
    state = models.JSONField("status", default=init_status)
    turn = models.CharField(max_length=1)
    
    def __str__(self) -> str:
        return self.game_id
    