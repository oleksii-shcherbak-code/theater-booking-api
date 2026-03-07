from django.db.models import QuerySet

from schedule.models import Performance


def performance_list() -> QuerySet[Performance]:
    return (
        Performance.objects
        .select_related("play", "theatre_hall")
        .order_by("starts_at")
    )


def performance_detail(performance_id: int) -> Performance:
    return (
        Performance.objects
        .select_related("play", "theatre_hall")
        .get(id=performance_id)
    )
