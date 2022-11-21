from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={})


def home_detail_view(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
    }
    try:
        tweet = models.Tweet.objects.get(id=tweet_id)
        status = 200
        data['content'] = tweet.content
    except models.Tweet.DoesNotExist:
        data["message"] = "Not found"
        status = 404

    return JsonResponse(data, status=status)
