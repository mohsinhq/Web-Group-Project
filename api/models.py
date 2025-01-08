from django.db import models
from django.contrib.auth.models import AbstractUser


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


# Custom User Model

class CustomUser(AbstractUser):
    name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.TextField(blank=True)  # Store hobbies as comma-separated values for now

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

    def set_hobbies_from_list(self, hobbies_list):
        self.hobbies = ', '.join(hobbies_list)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['name']
