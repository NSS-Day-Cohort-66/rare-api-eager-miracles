import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import Tag
from django.contrib.auth.models import User


class PostTests(APITestCase):

    fixtures = ['user', 'token', 'posts', 'categories', 'rareusers']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_post(self):

        url = "/posts"

        data = {
            "user": 1,
            "category": 1,
            "title": "Exploring National Parks",
            "image_url": "https://cdn.aarp.net/content/dam/aarp/travel/destinations/2020/09/1140-yosemite-hero.imgcache.rev.web.1914.1100.jpg",
            "content": "Exploring national parks is a wonderful way to connect with nature and experience the beauty of the great outdoors. From hiking through lush forests to witnessing breathtaking vistas, national parks offer a wide range of adventures for nature enthusiasts. Whether you're into wildlife photography, camping, or simply enjoying a peaceful escape, national parks have something to offer for everyone.",
            "approved": "true",
            # "pub_date": "2023-11-21"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["user"]["id"], 1)
        self.assertEqual(json_response["category"]["id"], 1)
        self.assertEqual(
            json_response["title"], "Exploring National Parks")
        self.assertEqual(json_response["content"], "Exploring national parks is a wonderful way to connect with nature and experience the beauty of the great outdoors. From hiking through lush forests to witnessing breathtaking vistas, national parks offer a wide range of adventures for nature enthusiasts. Whether you're into wildlife photography, camping, or simply enjoying a peaceful escape, national parks have something to offer for everyone.")
        # self.assertEqual(json_response["approved"], "approved")
        # self.assertEqual(json_response["pub_date"], "2023-11-21")
