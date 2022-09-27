from rest_framework import serializers
from quiz.models import Quiz, TakenQuiz, Question, Answer, AttemptedQuestion

class QuizSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")
    taken = serializers.SerializerMethodField()

    class Meta:
        model = Quiz 
        fields = ("id", "title", "description", "category", "taken")

    def get_taken(self, obj):
        user = self.context.get('request').user
        return TakenQuiz.objects.filter(
            user=user,
            quiz=obj
        ).exists()


class AttemptedQuestionSerializer(serializers.ModelSerializer):
    has_next_question = serializers.SerializerMethodField()

    class QuestionSerializer(serializers.ModelSerializer):
        class AnswerSerializer(serializers.ModelSerializer):
            class Meta:
                model = Answer
                fields = ("id", "text",)

        answers = AnswerSerializer(many=True)

        class Meta:
            model = Question
            fields = ("text", "answers", )

    question = QuestionSerializer()

    class Meta:
        model = AttemptedQuestion
        fields = ("id", "question", "has_next_question")

    def get_has_next_question(self, obj):
        return obj.taken_quiz.has_next_question


class AttemptQuestionSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()
