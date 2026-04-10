from rest_framework import serializers


from habits.models import Habit, HabitLog
from users.serializers import UserSerializer


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['habit', 'date']


class BaseHabitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    logs = HabitLogSerializer(read_only=True, many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['logs'] = [log['date'] for log in data['logs']]

        return data


class HabitDetailSerializer(BaseHabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'user', 'logs', 'streak']


class HabitListSerializer(BaseHabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'user', 'logs']
