import django_filters
from quiz.models import Quiz


class QuizFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Quiz
        fields = ['title', ]