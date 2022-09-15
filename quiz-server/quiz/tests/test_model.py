from datetime import datetime
from django.test import TestCase
from django.db.utils import IntegrityError
from quiz.models import *


class CategoryAndQuizModelTest(TestCase):
    def test_saving_category_and_quiz(self):
        category = Category.objects.create(
            title="Sport"
        )

        quiz1 = Quiz.objects.create(
            title="Football",
            description="Some description ...",
            category=category,
            pass_mark=5,
            is_published=True
        )

        quiz2 = Quiz.objects.create(
            title="Basketball",
            category=category,
            pass_mark=6,
        )

        saved_category = Category.objects.last()

        self.assertEqual(category, saved_category)

        saved_quizzes = Quiz.objects.all()

        self.assertEqual(saved_quizzes.count(), 2)
        self.assertEqual(saved_category.quiz_set.count(), 2)

        first_saved_quiz = saved_quizzes[0]
        second_saved_quiz = saved_quizzes[1]

        self.assertEqual(first_saved_quiz.title, "Football")
        self.assertEqual(first_saved_quiz.category, category)
        self.assertEqual(first_saved_quiz.pass_mark, 5)
        self.assertEqual(first_saved_quiz.is_published, True)
        self.assertEqual(first_saved_quiz.description, "Some description ...")

        self.assertEqual(second_saved_quiz.title, "Basketball")
        self.assertEqual(second_saved_quiz.category, category)
        self.assertEqual(second_saved_quiz.pass_mark, 6)
        self.assertEqual(second_saved_quiz.is_published, False)
        self.assertEqual(second_saved_quiz.description, None)



class QuestionAndAnswerModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            title="Sport"
        )
        self.quiz = Quiz.objects.create(
            title="Basketball",
            category=category,
            pass_mark=6,
        )

    def test_saving_question_and_answers(self):
        question = Question.objects.create(
            text = "Questions one ..",
            quiz=self.quiz
        )

        answer1 = Answer.objects.create(
            question=question,
            is_correct=True,
            text="Answer One"
        )

        answer2 = Answer.objects.create(
            question=question,
            text="Answer two"
        )

        answer3 = Answer.objects.create(
            question=question,
            text="Answer three"
        )

        saved_question = Question.objects.last()
        self.assertEqual(saved_question, question)

        saved_answers = Answer.objects.all()        
        self.assertEqual(saved_answers.count(), 3)
        self.assertEqual(saved_question.answers.count(), 3)
        self.assertIn(answer1, saved_answers)
        self.assertIn(answer2, saved_answers)
        self.assertIn(answer3, saved_answers)

    def test_duplicate_questions_are_invalid(self):
        Question.objects.create(
            text = "Questions one ..",
            quiz=self.quiz
        )

        with self.assertRaises(IntegrityError):
            Question.objects.create(
                text = "Questions one ..",
                quiz=self.quiz
            )

    def test_duplicate_answers_are_invalid(self):
        question = Question.objects.create(
            text = "Questions one ..",
            quiz=self.quiz
        )

        Answer.objects.create(
            question=question,
            text="Answer one"
        )

        with self.assertRaises(IntegrityError):
            Answer.objects.create(
                question=question,
                text="Answer one"
            )

    def test_cannot_save_multiple_correct_answers(self):
        question = Question.objects.create(
            text = "Questions one ..",
            quiz=self.quiz
        )

        Answer.objects.create(
            question=question,
            text="Answer one"
        )

        with self.assertRaises(IntegrityError):
            Answer.objects.create(
                question=question,
                text="Answer one"
            )


class TakenQuizModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            title="Sport"
        )
        self.quiz = Quiz.objects.create(
            title="Basketball",
            category=category,
            pass_mark=6,
        )
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password')
    

    def test_saving_takenquiz(self):
        taken_quiz = TakenQuiz.objects.create(
            user=self.user,
            quiz=self.quiz 
        )

        saved_taken_quiz = TakenQuiz.objects.last()


        self.assertEqual(saved_taken_quiz, taken_quiz)
        self.assertEqual(saved_taken_quiz.current_score, 0)
        self.assertNotEqual(saved_taken_quiz.start, None)
        self.assertEqual(saved_taken_quiz.end, None)
        self.assertEqual(saved_taken_quiz.quiz, self.quiz)
        self.assertEqual(saved_taken_quiz.completed, False)
        self.assertEqual(saved_taken_quiz.user, self.user)

    
    def test_cannot_take_quiz_twice(self):
        TakenQuiz.objects.create(
            user=self.user,
            quiz=self.quiz
        )
        
        with self.assertRaises(IntegrityError):
            TakenQuiz.objects.create(
                user=self.user,
                quiz=self.quiz
            )
            