from django.contrib import admin

from habits.models import Habit, HabitLog

# Register your models here.


admin.site.register(Habit)
admin.site.register(HabitLog)