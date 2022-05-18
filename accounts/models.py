from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    introduction = models.TextField(max_length=300, null=True, blank=True)
    email =  models.EmailField(max_length=45, unique=True)