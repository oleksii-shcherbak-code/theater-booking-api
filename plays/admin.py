from django.contrib import admin

from plays.models import Actor, Genre, Play


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genres_count", "actors_count")
    search_fields = ("title",)
    autocomplete_fields = ("genres", "actors")
    ordering = ("title",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("genres", "actors")
        )

    @admin.display(description="Genres")
    def genres_count(self, obj):
        return obj.genres.count()

    @admin.display(description="Actors")
    def actors_count(self, obj):
        return obj.actors.count()
