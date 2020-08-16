from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=300)
    is_bot = models.BooleanField(default=False)


class Game(models.Model):
    slug = models.CharField(max_length=300)
    players = models.ManyToManyField(
        to="games.Player", through="games.PlayerInGame", related_name="games",
    )


class PlayerInGame(models.Model):
    player = models.ForeignKey(
        to="games.Player", on_delete=models.CASCADE, related_name="game_relations",
    )
    game = models.ForeignKey(
        to="games.Game", on_delete=models.CASCADE, related_name="player_relations",
    )


class GameStateChange(models.Model):
    message = models.JSONField(default=dict)
