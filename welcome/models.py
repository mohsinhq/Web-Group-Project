from django.db import models

# Create your models here.


class PageView(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ip_address}:{self.timestamp}"
