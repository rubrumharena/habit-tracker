from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class BaseHabitSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()

    def get_user(self, obj):
        from users.serializers import UserSerializer
        return UserSerializer(obj.user).data

    def get_logs(self, obj):
        from habits.serializers import HabitLogSerializer
        return HabitLogSerializer(obj.logs.all(), read_only=True, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logs'] = [log['date'] for log in data['logs']]

        return data