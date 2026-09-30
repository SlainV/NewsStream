from django.conf import settings
from django.db import models

from publishers.models import Publisher
from articles.models import Article

# Create your models here.


class PublisherSubscription(models.Model):
    """Model for a subscription between a user and a publisher."""
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="publisher_subscriptions",
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "publisher"],
                name="unique_publisher_subscription",
            )
        ]

    def __str__(self):
        return f"{self.subscriber.username} follows {self.publisher.name}"


class JournalistSubscription(models.Model):
    """Model for a subscription between a user and a journalist."""
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journalist_subscriptions",
    )

    journalist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journalist_followers",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "journalist"],
                name="unique_journalist_subscription",
            )
        ]

    def __str__(self):
        return (
            f"{self.subscriber.username} follows "
            f"{self.journalist.username}"
        )


class Newsletter(models.Model):
    """A curated newsletter containing approved articles."""

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="newsletters",
    )

    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title