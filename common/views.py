from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from common.cache_keys import HabitsCacheKey
from common.filters import HabitFilter
from habits.models import Habit


class HabitListMixin:
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    filterset_class = HabitFilter

    def get_queryset(self):
        cache_key = HabitsCacheKey.habits(**self.request.GET)
        queryset = cache.get(cache_key)

        if queryset is not None:
            return cache.get(cache_key)

        queryset = Habit.objects.prefetch_related('logs').select_related('user')

        cache.set(cache_key, queryset, 30)
        return queryset