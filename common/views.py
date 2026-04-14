from django.core.cache import cache

from common.cache_keys import HabitsCacheKey
from habits.models import Habit


class HabitListMixin:
    def get_queryset(self):
        ordering = self.request.GET.get('ordering')

        cache_key = HabitsCacheKey.habits(ordering)
        queryset = cache.get(cache_key)

        if queryset is not None:
            return cache.get(cache_key)

        queryset = Habit.objects.prefetch_related('logs').select_related('user')
        if ordering:
            queryset = queryset.order_by(ordering)

        cache.set(cache_key, queryset, 30)
        return queryset