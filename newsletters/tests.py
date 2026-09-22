from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from publishers.models import Publisher

from .models import (
    JournalistSubscription,
    PublisherSubscription,
)


User = get_user_model()


class NewsletterSubscriptionTests(TestCase):
    """Tests for the newsletter subscription views."""


    def setUp(self):
        self.reader = User.objects.create_user(
            username="reader",
            password="password123",
            email="reader@test.com"
        )

        self.journalist = User.objects.create_user(
            username="journalist",
            password="password123",
            email="journalist@test.com"
        )

        journalist_group, created = Group.objects.get_or_create(
            name="Journalist"
        )

        self.journalist.groups.add(journalist_group)

        self.publisher = Publisher.objects.create(
            name="Campus News",
            description="University and campus news.",
            website="https://example.com",
            is_active=True,
        )

    def test_subscription_page_requires_login(self):
        """Test that the subscription page requires login."""
        response = self.client.get(
            reverse("newsletters:subscription_manage")
        )

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_view_subscription_page(self):
        """Test that a logged in user can view the subscription page."""
        self.client.login(
            username="reader",
            password="password123",
        )

        response = self.client.get(
            reverse("newsletters:subscription_manage")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.publisher.name)
        self.assertContains(response, self.journalist.username)

    def test_user_can_subscribe_to_publisher(self):
        """Test that a user can subscribe to a publisher."""
        self.client.login(
            username="reader",
            password="password123",
        )

        self.client.post(
            reverse(
                "newsletters:publisher_subscription_toggle",
                args=[self.publisher.id],
            )
        )

        subscription_exists = (
            PublisherSubscription.objects.filter(
                subscriber=self.reader,
                publisher=self.publisher,
            ).exists()
        )

        self.assertTrue(subscription_exists)

    def test_user_can_unsubscribe_from_publisher(self):
        """Test that a user can unsubscribe from a publisher."""
        PublisherSubscription.objects.create(
            subscriber=self.reader,
            publisher=self.publisher,
        )

        self.client.login(
            username="reader",
            password="password123",
        )

        self.client.post(
            reverse(
                "newsletters:publisher_subscription_toggle",
                args=[self.publisher.id],
            )
        )

        subscription_exists = (
            PublisherSubscription.objects.filter(
                subscriber=self.reader,
                publisher=self.publisher,
            ).exists()
        )

        self.assertFalse(subscription_exists)

    def test_user_can_subscribe_to_journalist(self):
        """Test that a user can subscribe to a journalist."""
        self.client.login(
            username="reader",
            password="password123",
        )

        self.client.post(
            reverse(
                "newsletters:journalist_subscription_toggle",
                args=[self.journalist.id],
            )
        )

        subscription_exists = (
            JournalistSubscription.objects.filter(
                subscriber=self.reader,
                journalist=self.journalist,
            ).exists()
        )

        self.assertTrue(subscription_exists)

    def test_user_can_unsubscribe_from_journalist(self):
        """Test that a user can unsubscribe from a journalist."""
        JournalistSubscription.objects.create(
            subscriber=self.reader,
            journalist=self.journalist,
        )

        self.client.login(
            username="reader",
            password="password123",
        )

        self.client.post(
            reverse(
                "newsletters:journalist_subscription_toggle",
                args=[self.journalist.id],
            )
        )

        subscription_exists = (
            JournalistSubscription.objects.filter(
                subscriber=self.reader,
                journalist=self.journalist,
            ).exists()
        )

        self.assertFalse(subscription_exists)

    def test_subscription_actions_require_post(self):
        """Test that subscription actions require POST requests."""
        self.client.login(
            username="reader",
            password="password123",
        )

        response = self.client.get(
            reverse(
                "newsletters:publisher_subscription_toggle",
                args=[self.publisher.id],
            )
        )

        self.assertEqual(response.status_code, 405)
