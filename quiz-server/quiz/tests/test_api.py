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

    def test_user_can_signup(self):
        username = "testuser"
        password1 = "pAssw0rd!"
        password2 = "pAssw0rd!"
        email = "test@test.com"

        response = self.client.post('/api/auth/registration/', 
            {
                'username': username, 
                'password1': password1,
                'password2': password2,
                'email': email
            })

        self.assertEqual(get_user_model().objects.count(), 1)
        user = get_user_model().objects.last()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        print(response.data)
        

      