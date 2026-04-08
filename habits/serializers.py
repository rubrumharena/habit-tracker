from rest_framework import serializers

from habits.models import Habit, HabitLog
from users.serializers import UserSerializer


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['habit', 'date']


class HabitDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    logs = HabitLogSerializer(read_only=True, many=True)

    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'streak', 'logs']


class HabitListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    logs = HabitLogSerializer(read_only=True, many=True)

    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'user', 'logs']