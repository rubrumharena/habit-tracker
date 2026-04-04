from django.urls import path

from habits import views

app_name = 'habits'

urlpatterns = [
    path('', views.HabitListCreateView.as_view(), name='habits'),
    path('<int:id>/', views.HabitRetrieveUpdateDestroyView.as_view(), name='habit'),
    path('<int:id>/logs/', views.HabitLogListView.as_view(), name='habit_logs'),
    path('<int:id>/toggle/', views.ToggleTodayHabitCompletionView.as_view(), name='toggle'),
]