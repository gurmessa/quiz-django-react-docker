from rest_framework import serializers
from quiz.models import Quiz, TakenQuiz

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