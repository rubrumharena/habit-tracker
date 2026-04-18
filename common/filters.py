import django_filters

from habits.models import Habit


class HabitFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user__username')
    ordering_fields = ['user__username', 'title']

    class Meta:
        model = Habit
        fields = {
            'user__username': ['exact', 'icontains'],
            'title' : ['exact', 'icontains']
        }