from rest_framework import serializers
from django.conf import settings
from tweets import models

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = str.lower(value)
        if value not in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not valid action for Tweets")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Tweet
        fields = ["id", "content", "likes"]

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    # content = serializers.SerializerMethodField(read_only=True, required=False)
    parent = TweetCreateSerializer(read_only=True)

    # is_retweet = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Tweet
        fields = ["id", "content", "likes", "is_retweet", "parent"]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_is_retweet(self, obj):
        return obj.is_retweet
