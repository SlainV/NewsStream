from django.db import models

# Create your models here.


class Publisher(models.Model):
    """A model for publishers."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
