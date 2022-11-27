import random

from django.contrib import admin
from . import models


class TweetLikeAdmin(admin.TabularInline):
    model = models.TweetLike


class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_filter = ["user__username", ]
    search_fields = ["user__username", ]
    list_display = ["user", "content", "likes_count"]

    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = "Likes"


admin.site.register(models.Tweet, TweetAdmin)
