from django.urls import path
from . import views

app_name = "tweets_api"

urlpatterns = [
    path("", views.tweet_list_view, name="list"),
    path("create/", views.tweet_create_view, name="create"),
    path("action/", views.tweet_action_view, name="action"),
    path("<int:tweet_id>/", views.tweet_detail_view, name="detail"),
    path("delete/<int:tweet_id>/", views.tweet_delete_view, name="delete"),
]
