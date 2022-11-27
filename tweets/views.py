from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import JsonResponse
from . import models, forms


def tweet_list_view_pd(request, *args, **kwargs):
    tweets = models.Tweet.objects.all()
    qs = [t.serialize() for t in tweets]
    data = {
        "response": qs
    }
    return JsonResponse(data)


def tweet_create_view_pd(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return settings.LOGIN_URL
    form = forms.TweetForm(request.POST or None)
    next_url = request.POST.get("next", None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url is not None and is_safe_url(next_url, settings.ALLOWED_HOSTS):
            return redirect(next_url)
        form = forms.TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, "components/forms.html", context={"form": form})


def tweet_detail_view_pd(request, tweet_id, *args, **kwargs):
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
