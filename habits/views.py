from http import HTTPStatus

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from common.cache_keys import HabitsCacheKey
from habits.models import Habit, HabitLog
from habits.serializers import HabitListSerializer, HabitDetailSerializer, HabitLogSerializer


# Create your views here.


class HabitListCreateView(ListCreateAPIView):
    queryset = Habit.objects.prefetch_related('logs').select_related('user')
    serializer_class = HabitListSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3

    def get(self, request, *args, **kwargs):
        if not cache.get('my_key'):
            cache.set("my_key", "hello, world!", 30)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        ordering = self.request.GET.get('ordering')

        cache_key = HabitsCacheKey.habits(ordering)
        queryset = cache.get(cache_key)

        if queryset is not None:
            return cache.get(cache_key)

        queryset = super().get_queryset()
        if ordering:
            queryset = queryset.order_by(ordering)

        cache.set(cache_key, queryset, 30)
        return queryset


class HabitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Habit.objects.prefetch_related('logs').select_related('user')
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
        habit_id = self.kwargs.get('id')
        cache_key = HabitsCacheKey.logs(habit_id)
        queryset = cache.get(cache_key)

        if queryset is not None:
            return cache.get(cache_key)

        queryset = HabitLog.objects.filter(habit_id=habit_id).order_by('-date')
        cache.set(cache_key, queryset, 30)

        return queryset