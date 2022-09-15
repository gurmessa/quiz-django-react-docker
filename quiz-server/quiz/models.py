from django.db import models
from django.db.models import Q, UniqueConstraint

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    title = models.CharField(max_length=155)


class Quiz(TimeStampedModel):
    title = models.CharField(max_length=155)
    description = models.TextField(null=True, blank=True)
    pass_mark = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)


class Question(TimeStampedModel):
    text = models.CharField(unique=True, max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(TimeStampedModel):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['is_correct', 'question'], condition=Q(is_correct=True), name='unique_correct_answer')
        ]
        unique_together = ('text', 'question',)