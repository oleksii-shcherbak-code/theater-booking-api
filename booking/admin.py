from django.contrib import admin
from django.db.models import Count, F, Sum
from django.utils.translation import gettext_lazy as _

from booking.models import Booking, Ticket
from booking.services import confirm_booking


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ("performance", "row", "seat")
    autocomplete_fields = ("performance",)
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_confirmed:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "is_confirmed",
        "tickets_count",
        "total_price",
        "created_at",
    )
    list_filter = (
        "is_confirmed",
        "created_at",
    )
    search_fields = (
        "id",
        "user__email",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    autocomplete_fields = ("user",)
    inlines = (TicketInline,)
    actions = ("confirm_bookings",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user")
            .prefetch_related("tickets__performance")
            .annotate(
                _tickets_count=Count("tickets", distinct=True),
                _total_price=Sum(
                    F("tickets__performance__ticket_price"),
                ),
            )
        )

    @admin.display(description=_("Tickets count"))
    def tickets_count(self, obj):
        return obj._tickets_count

    @admin.display(description=_("Total price"))
    def total_price(self, obj):
        return obj._total_price or 0

    @admin.action(description=_("Confirm selected bookings"))
    def confirm_bookings(self, request, queryset):
        confirmed = 0
        for booking in queryset:
            if not booking.is_confirmed:
                confirm_booking(booking=booking)
                confirmed += 1
        self.message_user(
            request,
            _("%d bookings were successfully confirmed.") % confirmed,
        )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking",
        "performance",
        "row",
        "seat",
    )
    list_filter = (
        "performance__theatre_hall",
        "performance__starts_at",
    )
    search_fields = (
        "booking__id",
        "booking__user__email",
        "performance__play__title",
    )
    autocomplete_fields = (
        "booking",
        "performance",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "booking",
                "booking__user",
                "performance",
                "performance__play",
                "performance__theatre_hall",
            )
        )
