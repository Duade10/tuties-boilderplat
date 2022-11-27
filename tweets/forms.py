from django.conf import settings
from django import forms
from . import models

MAXCHAR_LENGTH = settings.MAX_TWEET_LENGTH


class TweetForm(forms.ModelForm):
    class Meta:
        model = models.Tweet
        fields = ["content", ]

    def clean_content(self):
        content = self.cleaned_data.get("content", None)
        if len(content) > MAXCHAR_LENGTH:
            raise forms.ValidationError("This tweet is too long!")
        return content
