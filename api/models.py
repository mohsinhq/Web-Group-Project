from django.contrib.auth.models import AbstractUser
from django.db import models


class PageView(models.Model):
    """
    Tracks the number of views for specific pages by users.
    """
    user = models.ForeignKey(
        'CustomUser', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    page_name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.page_name}: {self.count} views"


class CustomUser(AbstractUser):
    """
    Extends the default Django User model to include additional fields.
    """
    name = models.CharField("Full Name", max_length=255)
    email = models.EmailField("Email Address", unique=True)
    date_of_birth = models.DateField("Date of Birth", null=True, blank=True)

    def __str__(self):
        return self.username


class Hobby(models.Model):
    """
    Represents a hobby. Each hobby can be linked to multiple users through a ManyToMany relationship.
    """
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(
        CustomUser, 
        related_name="user_hobbies", 
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hobbies"
