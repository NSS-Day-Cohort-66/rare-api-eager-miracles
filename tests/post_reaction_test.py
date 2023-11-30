import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import PostReaction, Post, Reaction, RareUser
from django.contrib.auth.models import User

class PostReactionTests(APITestCase):

    fixtures = ['user', 'token', 'rareusers', 'reactions', 'categories', 'posts', 'postreactions']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_post_reaction(self):

        url = "/postreactions"
        data = {
            "user": 1,
            "post": 1,
            "reaction": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["user_id"], 1)
        self.assertEqual(json_response["post_id"], 1)
        self.assertEqual(json_response["reaction_id"], 1)

    def test_list_post_reactions(self):

        response = self.client.get('/postreactions')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for obj in json_response:
            self.assertIn("user_id", obj)
            self.assertIn("post_id", obj)
            self.assertIn("reaction_id", obj)