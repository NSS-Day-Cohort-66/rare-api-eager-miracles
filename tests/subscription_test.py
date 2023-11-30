import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import Post, Category, RareUser, Subscription
from django.contrib.auth.models import User


class SubscriptionTest(APITestCase):

    fixtures = ['user', 'token', 'rareusers', 'subscriptions']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_subscription(self):

        author = RareUser.objects.get(id=1)
        follower = RareUser.objects.get(id=1)

        sub = Subscription()
        sub.author = author
        sub.follower = follower
        sub.save()

        # Initiate request and store response
        response = self.client.get(f"/subscriptions/{sub.id}")
        # Parse the JSON in the response body
        json_response = json.loads(response.content)
        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the fields are correct
        self.assertIn("author", json_response)
        self.assertIn("follower", json_response)

    def test_get_all_subscriptions(self):

        response = self.client.get('/subscriptions')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("author", json_response[0])
        self.assertIn("follower", json_response[0])

    def test_create(self):

        url = "/subscriptions"

        data = {
            "author": 1,
            "follower": 1
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["author"]["id"], 1)
        self.assertEqual(json_response["follower"]["id"], 1)

    def test_delete(self):

        author = RareUser.objects.get(id=1)
        follower = RareUser.objects.get(id=1)

        sub = Subscription()
        sub.author = author
        sub.follower = follower
        sub.save()

        # DELETE the game you just created
        response = self.client.delete(f"/subscriptions/{sub.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/subscriptions/{sub.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
