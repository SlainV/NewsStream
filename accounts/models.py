from django.contrib.auth.models import AbstractUser
from django.db import models

from publishers.models import Publisher


class User(AbstractUser):
    """
    Custom user model for NewsStream.
    """

    class Role(models.TextChoices):
        READER = "Reader", "Reader"
        JOURNALIST = "Journalist", "Journalist"
        EDITOR = "Editor", "Editor"
        PUBLISHER_MANAGER = "Publisher Manager", "Publisher Manager"
        ADMINISTRATOR = "Administrator", "Administrator"

    publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name="users",
    )

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.READER,
    )

    def __str__(self):
        return self.username
