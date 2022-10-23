from rest_framework import serializers
from quiz.models import Quiz, TakenQuiz, Question, Answer, AttemptedQuestion, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title",)


class QuizSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")
    taken = serializers.SerializerMethodField()
    has_passed = serializers.SerializerMethodField()

    class Meta:
        model = Quiz 
        fields = ("id", "title", "description", "category", "taken", "has_passed")

    def get_taken(self, obj):
        user = self.context.get('request').user
        return TakenQuiz.objects.filter(
            user=user,
            quiz=obj
        ).exists()

    def get_has_passed(self, obj):
        user = self.context.get('request').user
        if TakenQuiz.objects.filter(
            user=user,
            quiz=obj
        ).exists():
            return TakenQuiz.objects.get(
                user=user,
                quiz=obj
            ).has_passed

        return None


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


class TakenQuizResultSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="quiz.title")
    description = serializers.CharField(source="quiz.description")

    class Meta:
        model = TakenQuiz
        fields = ("title", "description", "current_score" ,"has_passed", "start", "end")