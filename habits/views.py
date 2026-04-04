from http import HTTPStatus

from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from habits.models import Habit, HabitLog
from habits.serializers import HabitListSerializer, HabitDetailSerializer, HabitLogSerializer


# Create your views here.


class HabitListCreateView(ListCreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitListSerializer


class HabitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitDetailSerializer
    lookup_field = 'id'


class ToggleTodayHabitCompletionView(APIView):
    def post(self, request, *args, **kwargs):
        habit = get_object_or_404(Habit, id=kwargs.get('id'))
        log, created = HabitLog.objects.get_or_create(habit=habit, date=timezone.localdate())

        if created:
            return Response(data=HabitLogSerializer(log).data, status=HTTPStatus.CREATED)

        log.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class HabitLogListView(ListAPIView):
    serializer_class = HabitLogSerializer

    def get_queryset(self):
        return HabitLog.objects.filter(habit_id=self.kwargs.get('id')).order_by('-date')