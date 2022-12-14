
from django.urls import path
from quiz import views
from quiz.models import TakenQuiz
urlpatterns = [
    path("categories", views.CategoryListAPIView.as_view(), name="categories"),
    path("quizzes", views.QuizListAPIView.as_view(), name="quizzes"),
    path("quiz/<pk>/register", views.TakenQuizAPIView.as_view(), name="quiz-register"),
    path("quiz/<pk>/next-question", views.NextQuestionAPIView.as_view(), name="next-question"),
    path("quiz/question/<pk>/attempt", views.AttemptQuestionAPIView.as_view(), name="attempt-question"),
    path("quiz/<pk>/result", views.TakenQuizResultAPIView.as_view(), name="attempt-question")
]
