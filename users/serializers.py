from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from habits.models import Habit
from common.serializers import BaseHabitSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email']



class UserHabitListSerializer(BaseHabitSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'logs', 'user']


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')

        if username and '@' in username:
            try:
                user = User.objects.get(email=username)
                attrs['username'] = user.username
            except User.DoesNotExist:
                pass
        return super().validate(attrs)
