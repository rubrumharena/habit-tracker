from django.contrib.auth.models import AbstractUser
from django.db import models

from habits.models import Habit


class User(AbstractUser):
    name = models.CharField(max_length=100)

    first_name = None
    last_name = None
    
    def __str__(self):
        return self.username