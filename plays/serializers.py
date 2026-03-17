from typing import Any, Dict

from rest_framework import serializers

from plays.models import Actor, Genre, Play


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class PlayListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Play
        fields = ("id", "title", "genres", "actors")


class PlayDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
    )
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
        write_only=True,
    )
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    def create(self, validated_data: Dict[str, Any]) -> Play:
        genres = validated_data.pop("genre_ids", [])
        actors = validated_data.pop("actor_ids", [])
        from plays.services import create_play
        return create_play(
            title=validated_data["title"],
            description=validated_data["description"],
            genres=genres,
            actors=actors,
        )

    def update(self, instance: Play, validated_data: Dict[str, Any]) -> Play:
        genres = validated_data.pop("genre_ids", [])
        actors = validated_data.pop("actor_ids", [])
        from plays.services import update_play
        return update_play(
            play=instance,
            title=validated_data.get("title", instance.title),
            description=validated_data.get("description", instance.description),
            genres=genres,
            actors=actors,
        )
