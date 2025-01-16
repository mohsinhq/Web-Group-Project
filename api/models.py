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
    hobbies = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'hobbies': self.get_hobbies_list(),
        }

    def get_hobbies_list(self):
        return [hobby.strip() for hobby in self.hobbies.split(',') if hobby.strip()]
    
    def common_hobbies(self, other_user):
        hobbies_set = set(self.get_hobbies_list())
        other_hobbies_set = set(other_user.get_hobbies_list())
        return len(hobbies_set.intersection(other_hobbies_set))

    class Meta:
        ordering = ['name']


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
