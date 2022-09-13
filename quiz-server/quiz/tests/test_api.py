from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class AuthenticationTest(APITestCase):
    def test_user_can_login(self):
        username = "testuser"
        password = "pAssw0rd!"
        user = get_user_model().objects.create_user(
            username=username, password=password)
    
        response = self.client.post('/api/auth/login/', 
            {'username': username, 'password': password}, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data['key'])