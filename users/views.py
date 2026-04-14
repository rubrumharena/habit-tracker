from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsOwner
from common.views import HabitListMixin
from users.serializers import UserHabitListSerializer


# Create your views here.


class UserHabitCreateListView(HabitListMixin, ListCreateAPIView):
    serializer_class = UserHabitListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return super().get_queryset().filter(user__username=self.kwargs.get('username'))
