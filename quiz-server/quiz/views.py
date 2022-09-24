from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from quiz.models import Quiz
from quiz.serializers import QuizSerializer


class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.published()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, ]