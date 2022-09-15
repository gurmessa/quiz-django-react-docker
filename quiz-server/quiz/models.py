from django.db import models

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