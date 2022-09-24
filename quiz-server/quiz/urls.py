
from django.urls import path
from quiz import views
from quiz.models import TakenQuiz
urlpatterns = [
    path("quizzes", views.QuizListAPIView.as_view(),name="quizzes"),
    path("quiz/<pk>/register", views.TakenQuizAPIView.as_view(),name="quizzes")
]
