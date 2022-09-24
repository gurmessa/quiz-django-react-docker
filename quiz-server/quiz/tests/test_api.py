from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from quiz.factories import *


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


class QuizApiTest(APITestCase):
    def setUp(self):
        self.PASSWORD = "PassWord"
        self.user = UserFactory(password=self.PASSWORD)

        
    def test_cannot_list_quizzes_for_unauthenticated_user(self):
        response = self.client.get('/api/quizzes')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


    def test_user_can_list_quizzes(self):
        self.client.login(username=self.user.username, password=self.PASSWORD)  

        quiz1 = QuizFactory()
        quiz2 = QuizFactory()
        quiz3 = QuizFactory()

        TakenQuiz.objects.create(
            user=self.user,
            quiz=quiz3
        )

        response = self.client.get('/api/quizzes')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_quiz_ids = [quiz1.id, quiz2.id, quiz3.id]
        act_quiz_ids = [quiz.get('id') for quiz in response.data]
        self.assertCountEqual(act_quiz_ids, exp_quiz_ids)

        exp_quiz1 = response.data[0]

        self.assertEqual(quiz1.title, exp_quiz1['title'])
        self.assertEqual(quiz1.description, exp_quiz1['description'])
        self.assertEqual(quiz1.category.title, exp_quiz1['category'])
        self.assertFalse(exp_quiz1['taken'])
        

        exp_quiz3 = response.data[2]
        self.assertTrue(exp_quiz3['taken'])


    def test_unpublished_quizzes_arenot_listed(self):
        self.client.login(username=self.user.username, password=self.PASSWORD)  

        quiz1 = QuizFactory()
        quiz2 = QuizFactory(is_published=False)

        response = self.client.get('/api/quizzes')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))