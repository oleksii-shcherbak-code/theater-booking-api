from django.db.models import QuerySet

from plays.models import Play


def play_list() -> QuerySet[Play]:
    return (
        Play.objects
        .prefetch_related("genres", "actors")
        .order_by("title")
    )


def play_detail(play_id: int) -> Play:
    return (
        Play.objects
        .prefetch_related("genres", "actors")
        .get(id=play_id)
    )
