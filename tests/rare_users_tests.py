import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rareapi.models import RareUser
from django.contrib.auth.models import User

class RareUserTests(APITestCase):

    fixtures = ['user', 'token', 'rareusers']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_rareusers(self):

        response = self.client.get('/rareusers')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('id', json_response[0])
        self.assertIn('user', json_response[0])
        self.assertIn('id', json_response[0])
        self.assertIn('full_name', json_response[0]['user'])
        self.assertIn('email', json_response[0]['user'])
        self.assertIn('user_profile_type', json_response[0]['user'])
        self.assertIn('date_joined', json_response[0]['user'])
        self.assertIn('image_avatar', json_response[0])

        self.assertEqual(len(json_response), 5)

    def test_get_rareusers(self):

        rareuser = RareUser.objects.first()

        response = self.client.get(f'/rareusers/{rareuser.id}')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('id', json_response)
        self.assertIn('full_name', json_response['user'])
        self.assertIn('email', json_response['user'])
        self.assertIn('user_profile_type', json_response['user'])
        self.assertIn('date_joined', json_response['user'])
        self.assertIn('image_avatar', json_response)
    
    