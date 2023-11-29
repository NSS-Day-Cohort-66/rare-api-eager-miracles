import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import Tag
from django.contrib.auth.models import User

class TagTests(APITestCase):
    
    fixtures = ['user', 'token', 'tags' ]
    
    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    def test_create_tag(self):

        url = "/tags"

        data = {
            "label": "Nick"
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Nick")

    def test_get_tags(self):

        response = self.client.get(f"/tags")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response[0]["label"], "Coding")
        self.assertEqual(json_response[2]["label"], "Gadgets")
        self.assertEqual(json_response[4]["label"], "Biology")

    def test_get_tag(self):
        tag = Tag()
        tag.label = "Nick"
        tag.save()
        
        response = self.client.get(f"/tags/{tag.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Nick")

    def test_change_tag(self):
        
        tag = Tag()
        tag.label = "Nick"
        tag.save()
        
        data = {
            "label": "Luke"
        }
        
        response = self.client.put(f"/tags/{tag.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        response = self.client.get(f"/tags/{tag.id}")
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Luke")

    def test_delete_tag(self):
        tag = Tag()
        tag.label = "Nick"
        tag.save()
        
        response = self.client.delete(f"/tags/{tag.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        response = self.client.get(f"/tags/{tag.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)