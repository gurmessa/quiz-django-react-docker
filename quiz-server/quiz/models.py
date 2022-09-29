from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    title = models.CharField(max_length=155)


class QuizManager(models.Manager):
    def published(self):
        return self.filter(is_published=True)


class Quiz(TimeStampedModel):
    title = models.CharField(max_length=155)
    description = models.TextField(null=True, blank=True)
    pass_mark = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    objects = QuizManager()


class Question(TimeStampedModel):
    text = models.CharField(unique=True, max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")


class Answer(TimeStampedModel):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['is_correct', 'question'], condition=Q(is_correct=True), name='unique_correct_answer')
        ]
        unique_together = ('text', 'question',)


class TakenQuiz(TimeStampedModel):
    completed = models.BooleanField(default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="taken_quizzes")
    current_score = models.IntegerField(default=0)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'quiz',)

    @property
    def has_next_question(self):
        return self.quiz.questions.exclude(
            pk__in=self.attempted_questions.values_list('question__id', flat=True)
        ).count() > 0

    def get_next_question(self):
        return self.quiz.questions.exclude(
            pk__in=self.attempted_questions.values_list('question__id', flat=True)
        ).first()

    @property
    def has_passed(self):
        if self.completed:
            return self.current_score >= self.quiz.pass_mark
        return None
        
class AttemptedQuestion(TimeStampedModel):
    taken_quiz = models.ForeignKey(TakenQuiz, on_delete=models.CASCADE, related_name="attempted_questions")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('taken_quiz', 'question',)
