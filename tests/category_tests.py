import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import Category
from django.contrib.auth.models import User

class CategoryTests(APITestCase):

    fixtures = ['user', 'token', 'categories']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_cat(self):

        url = "/categories"
        data = {
            "label": "Test Category"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Test Category")

    def test_get_cat(self):

        cat = Category()
        cat.label = "Test Category"
        cat.save()

        # Initiate request and store response
        response = self.client.get(f"/categories/{cat.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Test Category")
        
    def test_list_categories(self):

        response = self.client.get('/categories')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for obj in json_response:
            self.assertIn("label", obj)

    def test_delete_cat(self):
        """
        Ensure we can delete an existing game.
        """
        cat = Category()
        cat.label = "Test Category"
        cat.save()

        # DELETE the game you just created
        response = self.client.delete(f"/categories/{cat.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/categories/{cat.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_cat(self):
        """
        Ensure we can change an existing category.
        """
        cat = Category()
        cat.label = "Test Category"
        cat.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "label": "New Test Category"
        }

        response = self.client.put(f"/categories/{cat.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET game again to verify changes were made
        response = self.client.get(f"/categories/{cat.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
       
        self.assertEqual(json_response["label"], "New Test Category")
       