from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    photo = models.URLField()
    about = models.TextField()
    monoid = models.CharField(max_length=255)