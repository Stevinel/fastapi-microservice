from django.db import models

from callback.utils import name_regex


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Player(BaseModel, models.Model):
    name = models.CharField(validators=[name_regex()], max_length=54, default="", unique=True)
    email = models.EmailField(max_length=54, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"


class Game(BaseModel, models.Model):
    name = models.CharField(max_length=254, default="", unique=True)
    players = models.ManyToManyField(Player, blank=True, related_name="player_games")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"