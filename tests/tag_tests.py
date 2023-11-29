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