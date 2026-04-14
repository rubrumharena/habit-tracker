from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path('<str:username>/habits/', views.UserHabitCreateListView.as_view(), name='user_habits'),
]