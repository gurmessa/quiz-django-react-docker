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


class TakenQuizApiTest(APITestCase):
    def setUp(self):
        self.PASSWORD = "PassWord"
        self.user = UserFactory(password=self.PASSWORD)
        self.quiz1 = QuizFactory()
    
    def test_unauthenticated_user_cannot_register_to_test(self):
        response = self.client.get(f'/api/quiz/{self.quiz1.id}/register')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_authenticated_user_can_register_to_test(self):
        self.client.login(username=self.user.username, password=self.PASSWORD)  
        response = self.client.post(f'/api/quiz/{self.quiz1.id}/register')
        
        exp_taken_quiz = TakenQuiz.objects.last()

        self.assertEqual(exp_taken_quiz.id, response.data['id'])
        self.assertEqual(exp_taken_quiz.user, self.user)
        self.assertEqual(exp_taken_quiz.quiz, self.quiz1)
        self.assertEqual(TakenQuiz.objects.count(), 1)

    def test_cannot_taken_quiz_again(self):
        self.client.login(username=self.user.username, password=self.PASSWORD)  
        self.client.post(f'/api/quiz/{self.quiz1.id}/register')

        response = self.client.post(f'/api/quiz/{self.quiz1.id}/register')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    
class QuizNextQuestionApiTest(APITestCase):
    def setUp(self):
        self.PASSWORD = "PassWord"
        self.user1 = UserFactory(password=self.PASSWORD)
        self.user2 = UserFactory(password=self.PASSWORD)
        self.quiz1 = QuizFactory()


        self.question1 = QuestionFactory(quiz=self.quiz1)
        AnswerFactory(is_correct=True, question=self.question1)
        AnswerFactory(question=self.question1)
        AnswerFactory(question=self.question1)

        self.question2 = QuestionFactory(quiz=self.quiz1)
        AnswerFactory(question=self.question2)
        AnswerFactory(is_correct=True, question=self.question2)
        AnswerFactory(question=self.question2)

        self.taken_quiz = TakenQuiz.objects.create(
            user=self.user1,
            quiz=self.quiz1,
            completed=True,
        )

        self.questions = [self.question1, self.question2]

    def test_unauthorized_user_cannot_get_next_question(self):
        response = self.client.get(f'/api/quiz/{self.taken_quiz.id}/next-question')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_authorized_user_can_get_next_question(self):
        self.client.login(username=self.user1.username, password=self.PASSWORD)  
        response = self.client.get(f'/api/quiz/{self.taken_quiz.id}/next-question')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        exp_attempted_question = AttemptedQuestion.objects.last()
       
        self.assertEqual(exp_attempted_question.taken_quiz, self.taken_quiz)
        self.assertEqual(exp_attempted_question.question, self.question1)
        self.assertIsNone(exp_attempted_question.answer)

        self.assertEqual(
            response.data['id'],
            self.taken_quiz.id
        )
        self.assertEqual(
            response.data['question']['text'],
            self.question1.text
        )
        self.assertEqual(
            response.data['question']['answers'],
            [{'id': answer.id, 'text':answer.text} for answer in self.question1.answers.all()]
        )
        self.assertTrue(response.data['has_next_question'])

        # get second question
        response = self.client.get(f'/api/quiz/{self.taken_quiz.id}/next-question')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        exp_attempted_question2 = AttemptedQuestion.objects.last()
       
        self.assertEqual(exp_attempted_question2.taken_quiz, self.taken_quiz)
        self.assertEqual(exp_attempted_question2.question, self.question2)
        self.assertIsNone(exp_attempted_question2.answer)

        self.assertEqual(
            response.data['id'],
            exp_attempted_question2.id
        )
        self.assertEqual(
            response.data['question']['text'],
            self.question2.text
        )
        self.assertEqual(
            response.data['question']['answers'],
            [{'id': answer.id, 'text':answer.text} for answer in self.question2.answers.all()]
        )
        self.assertFalse(response.data['has_next_question'])


    def test_get_next_question_raises_exception_no_next_question(self):
        self.client.login(username=self.user1.username, password=self.PASSWORD)  
        # get first question
        response = self.client.get(f'/api/quiz/{self.taken_quiz.id}/next-question')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        # get second question
        response = self.client.get(f'/api/quiz/{self.taken_quiz.id}/next-question')
        
        # raise exception since there is no 3rd question
        response = self.client.get(f'/api/quiz/{self.taken_quiz.id}/next-question')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       
    def test_user_cannot_access_other_users_quiz(self):
        self.client.login(username=self.user2.username, password=self.PASSWORD)

        response = self.client.get(f'/api/quiz/{self.taken_quiz.id}/next-question')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
       