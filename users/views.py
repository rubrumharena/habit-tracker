from http import HTTPStatus

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from common.permissions import IsOwner
from common.views import HabitListMixin
from users.serializers import UserHabitListSerializer, UserRegisterSerializer, CustomTokenSerializer


class UserHabitListCreateView(HabitListMixin, ListCreateAPIView):
    serializer_class = UserHabitListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(user__username=self.kwargs.get('username'))


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response({'errors': serializer.errors}, status=HTTPStatus.BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer