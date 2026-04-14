from rest_framework import serializers

from common.serializers import BaseHabitSerializer
from habits.models import Habit, HabitLog
from users.serializers import UserSerializer


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['habit', 'date']


class HabitDetailSerializer(BaseHabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'user', 'logs', 'streak']


class HabitListSerializer(BaseHabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'user', 'logs']
