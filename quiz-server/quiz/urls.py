
from django.urls import path
from quiz import views
urlpatterns = [
    path("quizzes", views.QuizListAPIView.as_view(),name="quizzes")
]
