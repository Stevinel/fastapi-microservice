from django.contrib import admin
from django.contrib.admin.decorators import display

from .models import Game, Player


class PlayerInline(admin.TabularInline):
    model = Game.players.through
    extra = 0
    max_num = 5


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
        "created_date",
        "modified_date"
    ]
    search_fields = ["email"]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "get_players",
        "created_date",
        "modified_date"
    ]
    exclude = ["players"]

    @display(description="players")
    def get_players(self, obj):
        return [player.name for player in obj.players.all()]

    def get_inlines(self, request, obj=None):
        if obj:
            return [PlayerInline]
        else:
            return []
