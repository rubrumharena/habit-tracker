from http import HTTPStatus

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.cache_keys import HabitsCacheKey
from common.permissions import IsOwner
from common.views import HabitListMixin
from habits.models import Habit, HabitLog
from habits.serializers import HabitListSerializer, HabitDetailSerializer, HabitLogSerializer


class HabitListCreateView(HabitListMixin, ListAPIView):
    serializer_class = HabitListSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3
    permission_classes = [IsAdminUser]


class HabitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Habit.objects.prefetch_related('logs').select_related('user')
    serializer_class = HabitDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwner]


class ToggleTodayHabitCompletionView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

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
