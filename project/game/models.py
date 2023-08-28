from django.db import models

class Game(models.Model):
    game_id = models.CharField(primary_key=True, max_length=255)
    x_score = models.CharField(max_length=1)
    y_score = models.CharField(max_length=1)
    players_count = models.IntegerField()
    
    def __str__(self) -> str:
        return self.game_id