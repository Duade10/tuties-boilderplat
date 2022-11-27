import random

from django.db import models
from django.contrib.auth.models import User


class AbstractTimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TweetLike(AbstractTimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)


class Tweet(AbstractTimeStampedModel):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="images/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    likes = models.ManyToManyField(User, related_name="liked_tweets", blank=True, through=TweetLike)

    class Meta:
        ordering = ["-id", ]

    @property
    def is_retweet(self):
        return self.parent is not None

    def serialize(self):
        return {
            "id": self.pk,
            "content": self.content,
            "likes": random.randint(0, 100)
        }
