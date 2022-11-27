from django.test import TestCase
from django.contrib.auth.models import User
from . import models
from rest_framework.test import APIClient


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="OmoOniTest", password="Otintest")

    def test_user_created(self):
        self.assertEqual(self.user.username, "OmoOniTest")


class TweetTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testguy1", password="testguy111")
        self.user2 = User.objects.create_user(username="testguy3", password="testguy113")
        models.Tweet.objects.create(content="We testin out here!!! 1", user=self.user)
        models.Tweet.objects.create(content="We testin out here!!! 2", user=self.user)
        models.Tweet.objects.create(content="We testin out here!!! 3", user=self.user2)

    def test_tweet_create(self):
        user2 = User.objects.create_user(username="testguy2", password="testguy1111")
        tweet_1 = models.Tweet.objects.create(content="This is a test", user=self.user)
        tweet_2 = models.Tweet.objects.create(parent=tweet_1, user=user2)
        self.assertEqual(tweet_1.id, 4)
        self.assertEqual(tweet_1.user.username, self.user.username)
        self.assertEqual(tweet_2.user.username, user2.username)
        self.assertEqual(tweet_2.parent.id, tweet_1.id)
        tweet_1.delete()

    def get_client(self, n=None):
        if n is None:
            client = APIClient()
            client.login(username=self.user.username, password='testguy111')
        else:
            client = APIClient()
            client.login(username=self.user2.username, password="testguy113")
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_tweet_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {"id": 1, "action": "like"})
        self.assertEqual(models.Tweet.objects.get(id=1).likes.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_tweet_action_unlike(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {"id": 1, "action": "like"})
        print(response.json())
        self.assertEqual(response.json().get("likes"), 1)
        self.assertEqual(models.Tweet.objects.get(id=1).likes.count(), 1)
        self.assertEqual(response.status_code, 200)
        response = client.post('/api/tweets/action/', {"id": 1, "action": "unlike"})
        print(response.json())
        self.assertEqual(response.json().get("likes"), 0)
        self.assertEqual(models.Tweet.objects.get(id=1).likes.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_tweet_action_retweet(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {"id": 3, "action": "retweet"})
        last_tweet = models.Tweet.objects.first()
        print('Is retweet? ', last_tweet.is_retweet)
        self.assertEqual(last_tweet.user.id, self.user.id)
        self.assertEqual(response.status_code, 201)
        print(response.json())

    def test_tweet_create_api_view(self):
        client = self.get_client()
        response = client.post('/api/tweets/create/', {"content": "another tweet for test"})
        print(response.json())
        self.assertEqual(response.status_code, 201)

    def test_tweet_detail_api_view(self):
        tweet_id = 3
        client = self.get_client()
        response = client.get(f'/api/tweets/{tweet_id}/')
        print(response.json())
        self.assertEqual(response.json().get('id'), tweet_id)
        self.assertEqual(response.status_code, 200)

    def test_tweet_delete_api_view(self):
        tweet_id = 2
        client = self.get_client()
        client2 = self.get_client(n=1)
        response = client.delete(f'/api/tweets/delete/{tweet_id}/')
        self.assertEqual(response.status_code, 204)
        response = client.delete(f'/api/tweets/delete/{tweet_id}/')
        self.assertEqual(response.status_code, 404)
        response = client.delete('/api/tweets/delete/3/')
        self.assertEqual(response.status_code, 401)
        response = client2.post(f'/api/tweets/action/', data={"id": 1, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        new_retweet = models.Tweet.objects.first()
        print(new_retweet.user)
        print(new_retweet.parent.user)
        response = client.delete(f'/api/tweets/delete/{new_retweet.parent.id}/')
        self.assertEqual(response.status_code, 204)
