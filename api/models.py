from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class Hobby(models.Model):
    """
    Represents a hobby. Each hobby can be linked to multiple users through a ManyToMany relationship.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hobbies"


class CustomUser(AbstractUser):
    """
    Extends the default Django User model to include additional fields.
    """
    name = models.CharField("Full Name", max_length=255)
    email = models.EmailField("Email Address", unique=True)
    date_of_birth = models.DateField("Date of Birth", null=True, blank=True)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    user_hobbies = models.ManyToManyField(
        Hobby,
        related_name="hobby_users",  # Unique related_name
        blank=True
    )

    def get_age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def __str__(self):
        return self.username


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


class FriendRequest(models.Model):
    """
    Model to represent friend requests between users.
    """
    from_user = models.ForeignKey(
        CustomUser, related_name="sent_requests", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser, related_name="received_requests", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"], name="unique_friend_request"
            ),
            models.UniqueConstraint(
                fields=["to_user", "from_user"], name="unique_reverse_friend_request"
            ),
        ]
        verbose_name_plural = "Friend Requests"

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"


class Friendship(models.Model):
    """
    Model to represent friendships between users.
    """
    user1 = models.ForeignKey(CustomUser, related_name="friends1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name="friends2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user1", "user2"], name="unique_friendship"
            ),
            models.UniqueConstraint(
                fields=["user2", "user1"], name="unique_reverse_friendship"
            ),
        ]
        verbose_name_plural = "Friendships"

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"
