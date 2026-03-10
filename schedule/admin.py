from django.contrib import admin

from schedule.models import Performance, TheatreHall


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rows", "seats_per_row")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "play",
        "theatre_hall",
        "starts_at",
        "ticket_price",
    )
    list_filter = (
        "theatre_hall",
        "starts_at",
    )
    search_fields = (
        "play__title",
        "theatre_hall__name",
    )
    autocomplete_fields = (
        "play",
        "theatre_hall",
    )
    ordering = ("starts_at",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("play", "theatre_hall")
        )
