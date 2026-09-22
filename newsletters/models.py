from django.conf import settings
from django.db import models

from publishers.models import Publisher

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
