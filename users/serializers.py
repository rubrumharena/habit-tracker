from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from common.serializers import BaseHabitSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email']



class UserHabitListSerializer(BaseHabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'logs']
