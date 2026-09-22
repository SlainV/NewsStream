from django.utils import timezone

from .models import ApprovalLog

from django.conf import settings
from django.core.mail import send_mail
from newsletters.models import PublisherSubscription
from newsletters.models import JournalistSubscription
import requests

import logging
logger = logging.getLogger(__name__)


def approve_article(article, editor, notes=""):
    article.status = "approved"
    article.reviewed_by = editor
    article.reviewed_at = timezone.now()

    article.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
        ]
    )

    ApprovalLog.objects.create(
        article=article,
        editor=editor,
        action="approved",
        notes=notes,
    )

    notify_publisher_subscribers(article)
    notify_journalist_subscribers(article)
    notify_internal_api(article)


def reject_article(article, editor, notes=""):
    article.status = "rejected"
    article.reviewed_by = editor
    article.reviewed_at = timezone.now()

    article.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
        ]
    )

    ApprovalLog.objects.create(
        article=article,
        editor=editor,
        action="rejected",
        notes=notes,
    )


def send_article_notification(email, article):
    """ Send an email notification to the author of an approved article. """
    send_mail(
        subject=f"New article: {article.title}",
        message=(
            f"A new article has been approved.\n\n"
            f"Title: {article.title}\n"
            f"Author: {article.author.username}\n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


def notify_publisher_subscribers(article):
    """ Notify all subscribers of a new approved article. """
    subscriptions = PublisherSubscription.objects.filter(
        publisher=article.publisher,
    ).select_related("subscriber")

    for subscription in subscriptions:
        if subscription.subscriber.email:
            send_article_notification(
                subscription.subscriber.email,
                article,
            )


def notify_journalist_subscribers(article):
    """ Notify all subscribers of a new approved article. """
    subscriptions = JournalistSubscription.objects.filter(
        journalist=article.author,
    ).select_related("subscriber")

    for subscription in subscriptions:
        if subscription.subscriber.email:
            send_article_notification(
                subscription.subscriber.email,
                article,
            )


def notify_internal_api(article):
    """ Notify the internal API of a new article. """
    try:
        requests.post(
            "http://localhost:8000/api/approved/",
            json={
                "id": article.id,
                "title": article.title,
                "author": article.author.username,
            },
            timeout=5,
        )
    except Exception:
        logger.exception(
            "Failed to notify internal API"
        )
