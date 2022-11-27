from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions

from tweets import models
from .permissions import IsObjectUser
from . import serializers


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    tweets = models.Tweet.objects.all()
    serializer = serializers.TweetSerializer(tweets, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([permissions.IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = serializers.TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    try:
        tweets = models.Tweet.objects.get(id=tweet_id)
    except models.Tweet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.TweetSerializer(tweets)
    return Response(serializer.data)


@api_view(['DELETE', 'POST'])
@permission_classes([IsObjectUser, permissions.IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    try:
        tweet = models.Tweet.objects.get(id=tweet_id)
    except models.Tweet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if tweet.user.id is request.user.id:
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = serializers.TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        tweet_id = serializer.validated_data.get("id", None)
        action = serializer.validated_data.get("action", None)
        # content = serializer.validated_data("content", None)
        try:
            tweet = models.Tweet.objects.get(id=tweet_id)
        except models.Tweet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if action == "like":
            tweet.likes.add(request.user)
            serializer = serializers.TweetSerializer(tweet)
            return Response(serializer.data)
        elif action == "unlike":
            tweet.likes.remove(request.user)
            serializer = serializers.TweetSerializer(tweet)
            return Response(serializer.data)
        elif action == "retweet":
            new_tweet = models.Tweet.objects.create(user=request.user, parent=tweet, content=None)
            serializer = serializers.TweetSerializer(new_tweet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
