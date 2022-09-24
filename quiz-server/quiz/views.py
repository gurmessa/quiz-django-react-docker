from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quiz.models import Quiz, TakenQuiz
from quiz.serializers import QuizSerializer


class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.published()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, ]


class TakenQuizAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        if not TakenQuiz.objects.filter(
            user=self.request.user,
            quiz=quiz
        ).exists():
            taken_quiz = TakenQuiz.objects.create(
                user=self.request.user,
                quiz=quiz
            )
            return Response({
                "id":taken_quiz.pk,
                "message": "Registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({"message": "You cannot taken a quiz twice"}, status=status.HTTP_400_BAD_REQUEST)