from django.contrib.auth.models import AbstractUser
from django.db import models


class PageView(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    page_name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.page_name}: {self.count} views"


class CustomUser(AbstractUser):
    name = models.CharField("Full Name", max_length=255)
    email = models.EmailField("Email Address", unique=True)
    date_of_birth = models.DateField("Date of Birth", null=True, blank=True)

    # Removed TextField 'hobbies' to avoid redundancy since a ManyToMany relation is defined in `Hobby`.
    # Users' hobbies will be accessed through the related_name `user_hobbies`.

    def __str__(self):
        return self.username


class Hobby(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(CustomUser, related_name="user_hobbies", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hobbies"
