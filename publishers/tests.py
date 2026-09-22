from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from publishers.models import Publisher

User = get_user_model()


class PublisherTests(TestCase):
    """ Tests for the publisher model. """
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager",
            password="password",
            email="test@example.com",
        )

        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            description="Test Description"
        )

    def test_publisher_creation(self):
        self.assertEqual(
            self.publisher.name,
            "Test Publisher"
        )

    def test_user_can_be_affiliated_with_publisher(self):
        self.manager.publishers.add(self.publisher)

        self.assertIn(
            self.publisher,
            self.manager.publishers.all()
        )
