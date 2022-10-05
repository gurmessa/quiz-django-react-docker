from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from quiz.models import Quiz, TakenQuiz, AttemptedQuestion, Answer
from quiz.serializers import QuizSerializer, AttemptedQuestionSerializer, \
    AttemptQuestionSerializer, TakenQuizResultSerializer
from quiz.permissions import IsOwner
from quiz.filters import QuizFilter


class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.published()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuizFilter


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


class AttemptQuestionAPIView(APIView):
    permission_classes = [IsOwner, ]

    def post(self, request, *args, **kwargs):
        attempted_question = get_object_or_404(AttemptedQuestion, pk=kwargs['pk'])
        
        self.check_object_permissions(request, attempted_question.taken_quiz)
        
        serializer = AttemptQuestionSerializer(data=request.data)

        if serializer.is_valid():
            answer_id = serializer.data['answer_id']
            answer = get_object_or_404(Answer, pk=answer_id)

            if answer.question != attempted_question.question:
                return Response(
                    {"message": "Invalid answer"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif attempted_question.answer is not None:
                return Response(
                    {"message": "Question is already attempted"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            taken_quiz = attempted_question.taken_quiz

            if taken_quiz.completed:
                return Response(
                    {"message": "Quiz is already completed"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            attempted_question.answer = answer
            attempted_question.save()

 
            if attempted_question.answer.is_correct:
                taken_quiz.current_score +=1
                taken_quiz.save()
            
            if not taken_quiz.has_next_question:
                taken_quiz.completed = True
                taken_quiz.save()
            data = {
                "quiz_completed": taken_quiz.completed
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TakenQuizResultAPIView(generics.RetrieveAPIView):
    permission_classes = [IsOwner]
    serializer_class = TakenQuizResultSerializer

    def get_object(self):
        taken_quiz = TakenQuiz.objects.get(pk=self.kwargs['pk'])

        if not taken_quiz.completed:
            raise PermissionDenied({"quiz not completed"})

        return taken_quiz