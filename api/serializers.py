from rest_framework import serializers
from clubs.models import Club, Player, News


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name", "position", "photo", "club"]


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ["id", "name", "city", "founded", "titles", "logo"]


class ClubDetailSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True, source="players")

    class Meta:
        model = Club
        fields = ["id", "name", "city", "founded", "titles", "logo", "players"]


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "excerpt", "image", "published_at", "is_published", "source_url"]



