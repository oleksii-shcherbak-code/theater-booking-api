"""
Selectors for schedule domain.

Contains optimized read-only queries for performances.
"""

from django.db.models import QuerySet

from schedule.models import Performance


def performance_list() -> QuerySet[Performance]:
    """
    Return queryset for listing performances.

    Returns:
        QuerySet of Performance objects.
    """
    return (
        Performance.objects
        .select_related("play", "theatre_hall")
        .order_by("starts_at")
    )
