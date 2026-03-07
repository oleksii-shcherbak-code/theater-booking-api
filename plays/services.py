from plays.models import Play


def create_play(*, title: str, description: str, genres, actors) -> Play:
    play = Play.objects.create(
        title=title,
        description=description,
    )
    play.genres.set(genres)
    play.actors.set(actors)
    return play


def update_play(
    *,
    play: Play,
    title: str,
    description: str,
    genres,
    actors,
) -> Play:
    play.title = title
    play.description = description
    play.save(update_fields=("title", "description"))
    play.genres.set(genres)
    play.actors.set(actors)
    return play
