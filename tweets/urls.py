from django.urls import path
from . import views

app_name = "tweets"

urlpatterns = [
    path("", views.tweet_list_view_pd, name="list"),
    path("create/", views.tweet_create_view_pd, name="create"),
    path("detail/", views.tweet_detail_view_pd, name="detail"),
]
