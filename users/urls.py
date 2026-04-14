from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views
from users.views import RegisterView

app_name = 'users'

urlpatterns = [
    path('<str:username>/habits/', views.UserHabitListCreateView.as_view(), name='user_habits'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]