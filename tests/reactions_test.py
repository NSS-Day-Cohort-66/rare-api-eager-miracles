import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import Reaction
from django.contrib.auth.models import User

class ReactionsTests(APITestCase):
    
    fixtures = ['user', 'token', 'reactions' ]
    
    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    def test_create_reaction(self):
        
        url = "/reactions"
        
        data = {
            "label": "Nick",
            "image_url": "www.testreaction.com"
        }
        
        response = self.client.post(url, data, format='json')
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(json_response["label"], "Nick")
        self.assertEqual(json_response["image_url"], "www.testreaction.com")

    def test_get_reaction(self):

        reaction = Reaction.objects.first()

        response = self.client.get(f'/reactions/{reaction.id}')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response['label'], "love")
        self.assertEqual(json_response["image_url"], "https://images.emojiterra.com/google/noto-emoji/unicode-15.1/color/1024px/2764.png")
    
    def test_get_reactions(self):

        response = self.client.get('/reactions')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response[0]["label"], "love")
        self.assertEqual(json_response[1]["label"], "mindblown")
        self.assertEqual(json_response[0]["image_url"], "https://images.emojiterra.com/google/noto-emoji/unicode-15.1/color/1024px/2764.png")
        self.assertEqual(json_response[1]["image_url"], "https://images.emojiterra.com/google/noto-emoji/unicode-15.1/color/1024px/1f92f.png")

    def test_change_reaction(self):

        reaction = Reaction()
        reaction.label = 'Nick'
        reaction.image_url = "www.testreaction.com"

        reaction.save()
        
        data = {
            "label": "New Nick!",
            "image_url": "www.testchangereaction.com" 
        }

        response = self.client.put(f'/reactions/{reaction.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/reactions/{reaction.id}')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['label'], 'New Nick!')
        self.assertEqual(json_response['image_url'], 'www.testchangereaction.com')
        
    def test_delete_reaction(self):

        reaction = Reaction()
        reaction.label = "Nick"
        reaction.image_url = "www.testreaction.com"

        reaction.save()

        response = self.client.delete(f"/reactions/{reaction.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/reactions/{reaction.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)