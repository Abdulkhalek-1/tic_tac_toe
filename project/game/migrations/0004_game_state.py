# Generated by Django 4.2.4 on 2023-08-29 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_game_players_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='state',
            field=models.JSONField(default={'11': '', '12': '', '13': '', '21': '', '22': '', '23': '', '31': '', '32': '', '33': ''}, verbose_name='status'),
        ),
    ]