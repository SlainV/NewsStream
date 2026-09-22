from django.contrib.auth.models import AbstractUser
from django.db import models

from publishers.models import Publisher


class User(AbstractUser):
    """
    Custom user model for NewsStream.
    """

    publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name="users")

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
