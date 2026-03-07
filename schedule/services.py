from schedule.models import Performance


def create_performance(
    *,
    play,
    theatre_hall,
    starts_at,
    ticket_price,
) -> Performance:
    return Performance.objects.create(
        play=play,
        theatre_hall=theatre_hall,
        starts_at=starts_at,
        ticket_price=ticket_price,
    )
