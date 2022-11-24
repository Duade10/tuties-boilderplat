from django import forms

from . import models

MAXCHAR_LENGTH = 240


class TweetForm(forms.ModelForm):
    class Meta:
        model = models.Tweet
        fields = ["content", ]

    def clean_content(self):
        content = self.cleaned_data.get("content", None)
        if len(content) > MAXCHAR_LENGTH:
            raise forms.ValidationError("This tweet is too long!")
        return content
