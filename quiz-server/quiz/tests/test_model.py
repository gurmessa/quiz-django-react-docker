from unicodedata import category
from django.test import TestCase
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


