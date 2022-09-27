from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from quiz.models import Quiz, TakenQuiz, AttemptedQuestion
from quiz.serializers import QuizSerializer, AttemptedQuestionSerializer
from quiz.permissions import IsOwner

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


class NextQuestionAPIView(APIView):
    permission_classes = [IsOwner, ]

    def get(self, request, *args, **kwargs):
        taken_quiz = get_object_or_404(TakenQuiz, pk=kwargs['pk'])

        self.check_object_permissions(request, taken_quiz)

        if taken_quiz.has_next_question:
            question = taken_quiz.get_next_question()
            attempted_question = AttemptedQuestion.objects.create(
                question=question,
                taken_quiz=taken_quiz
            )
            return Response(
                AttemptedQuestionSerializer(attempted_question).data
            )
        else:
            return Response(
                {"message": "quiz has no next question"}, 
                status=status.HTTP_400_BAD_REQUEST
            )