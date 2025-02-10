from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.IntegerField(null=True)  # Optional age field

    def __str__(self):
        return self.username
