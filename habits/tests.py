from datetime import timedelta

from django.utils import timezone
from django.test import TestCase

from habits.models import Habit, HabitLog


# Create your tests here.


class HabitModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        random_date = today - timedelta(days=10)

        habits = [Habit(title=f'Title {i}') for i in range(5)]
        Habit.objects.bulk_create(habits)

        habit_objs = Habit.objects.all()

        cls.streaked_today_habit = habit_objs[0]
        streaked_log = [HabitLog(habit=cls.streaked_today_habit, date=today - timedelta(days=i)) for i in range(5)]
        HabitLog.objects.bulk_create(streaked_log)

        cls.broken_habit = habit_objs[1]
        HabitLog.objects.create(habit=cls.broken_habit, date=random_date)

        cls.streaked_yesterday_habit = habit_objs[2]
        HabitLog.objects.create(habit=cls.streaked_yesterday_habit, date=yesterday)

        cls.single_today_habit = habit_objs[3]
        HabitLog.objects.create(habit=cls.single_today_habit, date=today)
        HabitLog.objects.create(habit=cls.single_today_habit, date=random_date)

        cls.single_yesterday_habit = habit_objs[4]
        HabitLog.objects.create(habit=cls.single_yesterday_habit, date=yesterday)
        HabitLog.objects.create(habit=cls.single_yesterday_habit, date=random_date)

    def test_outputs_streak_at_today_record(self):
        habit = self.streaked_today_habit
        self.assertEqual(habit.streak, HabitLog.objects.filter(habit=habit).count())

    def test_outputs_streak_at_yesterday_record(self):
        habit = self.streaked_yesterday_habit
        self.assertEqual(habit.streak, HabitLog.objects.filter(habit=habit).count())

    def test_streak_equals_0_if_streak_is_broken(self):
        habit = self.broken_habit
        self.assertEqual(habit.streak, 0)

    def test_outputs_streak_if_gap_between_today_and_date(self):
        habit = self.single_today_habit
        self.assertEqual(habit.streak, 1)

    def test_outputs_streak_if_gap_between_yesterday_and_date(self):
        habit = self.single_yesterday_habit
        self.assertEqual(habit.streak, 1)