
from django.urls import path
from quiz import views
from quiz.models import TakenQuiz
urlpatterns = [
    path("quizzes", views.QuizListAPIView.as_view(), name="quizzes"),
    path("quiz/<pk>/register", views.TakenQuizAPIView.as_view(), name="quiz-register"),
    path("quiz/<pk>/next-question", views.NextQuestionAPIView.as_view(), name="next-question")
]
