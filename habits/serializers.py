from rest_framework import serializers

from habits.models import Habit, HabitLog


class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description']


class HabitDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'streak']


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['habit', 'date']