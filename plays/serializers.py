from typing import Any, Dict, Iterable
from rest_framework import serializers
from plays.models import Actor, Genre, Play


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for Genre model.
    """
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    """
    Serializer for Actor model.
    """
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class PlayListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing plays with nested genres and actors.
    """
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Play
        fields = ("id", "title", "genres", "actors")


class PlayDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for play detail with description, genres and actors.
    """
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayCreateUpdateSerializer(serializers.Serializer):
    """
    Serializer for creating and updating plays.
    """
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
    )
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
    )

    def create(self, validated_data: Dict[str, Any]) -> Play:
        """
        Create a play using the service layer.
        """
        from plays.services import create_play

        genres: Iterable[Genre] = validated_data["genre_ids"]
        actors: Iterable[Actor] = validated_data["actor_ids"]

        return create_play(
            title=validated_data["title"],
            description=validated_data["description"],
            genres=genres,
            actors=actors,
        )

    def update(self, instance: Play, validated_data: Dict[str, Any]) -> Play:
        """
        Update a play using the service layer.
        """
        from plays.services import update_play

        genres: Iterable[Genre] = validated_data["genre_ids"]
        actors: Iterable[Actor] = validated_data["actor_ids"]

        return update_play(
            play=instance,
            title=validated_data["title"],
            description=validated_data["description"],
            genres=genres,
            actors=actors,
        )
