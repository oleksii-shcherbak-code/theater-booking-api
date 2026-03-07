from django.contrib import admin

from plays.models import Actor, Genre, Play


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    filter_horizontal = ("genres", "actors")
