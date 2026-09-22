from django.conf import settings
from django.db import models
from publishers.models import Publisher

# Create your models here.


class Category(models.Model):
    """Category model."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Article model."""
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_articles",
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    class Meta:
        ordering = ["-created_at"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ApprovalLog(models.Model):
    """Approval log model."""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="approval_logs",
    )

    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    action = models.CharField(max_length=20)

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.article.title} - {self.action}"
