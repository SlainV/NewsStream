from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class APITestCase(TestCase):

    def test_articles_endpoint_exists(self):
        """ Test that the articles endpoint exists """
        response = self.client.get(
            reverse("api_articles")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_protected_endpoint_requires_authentication(self):
        """ Test that the protected endpoint requires authentication """
        response = self.client.get(
            reverse("api_protected")
        )

        self.assertEqual(
            response.status_code,
            401
        )

    def test_authenticated_user_can_access_protected_api(self):
        """ Test that an authenticated user can access the protected endpoint """

        User = get_user_model()

        user = User.objects.create_user(
            username="john",
            password="password123"
        )

        token, _ = Token.objects.get_or_create(
            user=user
        )

        response = self.client.get(
            reverse("api_protected"),
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        self.assertEqual(
            response.status_code,
            200
        )
