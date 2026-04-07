from datetime import timedelta

from django.db import models
from django.utils import timezone

# Create your models here.

class Habit(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def streak(self) -> int:
        dates = set(HabitLog.objects.filter(habit=self).values_list('date', flat=True))

        if not dates:
            return 0

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        if today in dates:
            anchor = today
        elif yesterday in dates:
            anchor = yesterday
        else:
            return 0

        streak = 0
        cur_date = anchor

        while cur_date in dates:
            streak += 1
            cur_date = cur_date - timedelta(days=1)

        return streak

    def __str__(self):
        return self.title


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f'{self.habit} | {self.date}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['habit', 'date'],
                name='unique_habit'
            )
        ]