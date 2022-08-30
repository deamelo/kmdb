from rest_framework import serializers
from genres.serializers import GenreSerializer
from genres.models import Genre

from .models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification= serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict) -> Movie:
        genres_key = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre in genres_key:
            genre_data, _ = Genre.objects.get_or_create(**genre)

            movie.genres.add(genre_data)

        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        instance.title = validated_data.get('title', instance.title)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.premiere = validated_data.get('premiere', instance.premiere)
        instance.classification = validated_data.get('classification', instance.classification)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)

        genres = []
        for name in validated_data.get("genres"):

            genres.append(Genre.objects.get_or_create(name=name["name"])[0].id)
        if genres:
            instance.genres.set(genres)

        instance.save()

        return instance
