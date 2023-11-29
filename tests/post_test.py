import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import Post, Category, RareUser
from django.contrib.auth.models import User


class PostTests(APITestCase):

    fixtures = ['user', 'token', 'posts', 'categories', 'rareusers']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_post(self):

        rare_user = RareUser.objects.get(id=1)
        category = Category.objects.get(id=2)

        post = Post()
        post.user = rare_user
        post.category = category
        post.title = "Exploring the Wonders of Machine Learning"
        post.content = "In this article, we delve into the fascinating world of machine learning, exploring its applications in various industries..."
        post.image_url = "https://www.fsm.ac.in/blog/wp-content/uploads/2022/08/ml-e1610553826718.jpg"
        post.approved = True
        post.save()

        response = self.client.get(f"/posts/{post.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            json_response["title"], "Exploring the Wonders of Machine Learning")
        self.assertEqual(
            json_response["content"], "In this article, we delve into the fascinating world of machine learning, exploring its applications in various industries...")
        self.assertEqual(
            json_response["image_url"], "https://www.fsm.ac.in/blog/wp-content/uploads/2022/08/ml-e1610553826718.jpg")
        self.assertEqual(json_response["approved"], True)

    def test_create_post(self):

        url = "/posts"

        data = {
            "user": 1,
            "category": 1,
            "title": "Exploring National Parks",
            "image_url": "https://cdn.aarp.net/content/dam/aarp/travel/destinations/2020/09/1140-yosemite-hero.imgcache.rev.web.1914.1100.jpg",
            "content": "Exploring national parks is a wonderful way to connect with nature and experience the beauty of the great outdoors. From hiking through lush forests to witnessing breathtaking vistas, national parks offer a wide range of adventures for nature enthusiasts. Whether you're into wildlife photography, camping, or simply enjoying a peaceful escape, national parks have something to offer for everyone.",
            "approved": "true",
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["user"]["id"], 1)
        self.assertEqual(json_response["category"]["id"], 1)
        self.assertEqual(
            json_response["title"], "Exploring National Parks")
        self.assertEqual(json_response["content"], "Exploring national parks is a wonderful way to connect with nature and experience the beauty of the great outdoors. From hiking through lush forests to witnessing breathtaking vistas, national parks offer a wide range of adventures for nature enthusiasts. Whether you're into wildlife photography, camping, or simply enjoying a peaceful escape, national parks have something to offer for everyone.")

    def test_delete_post(self):

        rare_user = RareUser.objects.get(pk=1)
        category = Category.objects.get(pk=2)

        post = Post()
        post.user = rare_user
        post.category = category
        post.title = "Hi"
        post.image_url = "http://www.Hi.jpg"
        post.content = "Hi"
        post.approved = True
        post.save()

        # DELETE the game you just created
        response = self.client.delete(f"/posts/{post.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        print(response.content)
        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/posts/{post.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
