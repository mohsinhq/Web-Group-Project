from django.contrib.auth.models import AbstractUser
from django.db import models

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)

class Hobby(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

