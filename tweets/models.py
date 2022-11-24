import random

from django.db import models


class Tweet(models.Model):
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to="images/", null=True, blank=True)

    def serialize(self):
        return {
            "id": self.pk,
            "content": self.content,
            "likes": random.randint(0, 100)
        }
