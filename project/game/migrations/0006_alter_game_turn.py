# Generated by Django 4.2.4 on 2023-08-29 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_game_turn_alter_game_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='turn',
            field=models.CharField(max_length=1),
        ),
    ]
