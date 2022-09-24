from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory
from .models import *


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    password = "PaSsWordd!"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)
        

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: 'Category %d' % n)


class QuizFactory(DjangoModelFactory):
    class Meta:
        model = Quiz

    title = factory.Sequence(lambda n: 'Quiz %d' % n)
    description = FuzzyText()
    category = factory.SubFactory(CategoryFactory)
    pass_mark = 5
    is_published = True


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question
    
    text = factory.Sequence(lambda n: 'Question %d' % n)
    quiz = factory.SubFactory(QuizFactory)


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer
    
    text = FuzzyText(length=100, prefix="answer ")
    is_correct = False
    question = factory.SubFactory(QuestionFactory)