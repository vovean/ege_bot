from django.db import models


# Create your models here.

class TGUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(primary_key=True)
    name = models.TextField()
    is_admin = models.BooleanField(default=False)


class Task(models.Model):
    number = models.IntegerField()
    problem_pic = models.FileField(null=True)
    problem_text = models.TextField(null=True)
    answer = models.TextField(null=True)
    link_to_lesson = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(problem_pic__isnull=False) | models.Q(problem_text__isnull=False),
                name='check_problem_not_null'
            )
        ]


class TaskAttempt(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(TGUser, on_delete=models.CASCADE)
    attempts_count = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['task', 'user', 'solved'])
        ]
