from rest_framework import serializers

from plays.models import Actor, Genre, Play
from plays.services import create_play, update_play


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
    )
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
    )

    def create(self, validated_data):
        return create_play(
            title=validated_data["title"],
            description=validated_data["description"],
            genres=validated_data["genre_ids"],
            actors=validated_data["actor_ids"],
        )

    def update(self, instance, validated_data):
        return update_play(
            play=instance,
            title=validated_data["title"],
            description=validated_data["description"],
            genres=validated_data["genre_ids"],
            actors=validated_data["actor_ids"],
        )
