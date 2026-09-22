from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import User

# Create your tests here.


class AuthenticationTests(TestCase):
    """ Authentication Tests """

    def test_dashboard_requires_login(self):
        """ Test that the dashboard requires login """
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302
        )


class JournalistAccessTests(TestCase):
    """ Journalist Access Tests """

    def test_journalist_can_access_view(self):
        """ Test that a journalist can access the journalist area """

        journalist_group = Group.objects.create(
            name="Journalist"
        )

        user = User.objects.create_user(
            username="journalist",
            password="testpass123"
        )

        user.groups.add(
            journalist_group
        )

        self.client.login(
            username="journalist",
            password="testpass123"
        )

        response = self.client.get(
            reverse("journalist_area")
        )

        self.assertEqual(
            response.status_code,
            200
        )


class EditorAccessTests(TestCase):
    """ Editor Access Tests """

    def test_non_editor_denied(self):
        """ Test that a non-editor is denied access to the editor area """

        user = User.objects.create_user(
            username="reader",
            password="testpass123"
        )

        self.client.login(
            username="reader",
            password="testpass123"
        )

        response = self.client.get(
            reverse("editor_area")
        )

        self.assertNotEqual(
            response.status_code,
            200
        )


class AdminDashboardTests(TestCase):
    def setUp(self):
        """ Set up the test environment """
        self.admin_group, _ = Group.objects.get_or_create(
            name="Administrator"
        )

        self.reader_group, _ = Group.objects.get_or_create(
            name="Reader"
        )

        self.journalist_group, _ = Group.objects.get_or_create(
            name="Journalist"
        )

        self.editor_group, _ = Group.objects.get_or_create(
            name="Editor"
        )

        self.publisher_manager_group, _ = Group.objects.get_or_create(
            name="Publisher Manager"
        )

    """ Admin Dashboard Tests """
    def test_admin_can_access_dashboard(self):
        admin_group = Group.objects.get(
            name="Administrator"
        )

        user = User.objects.create_user(
            username="adminuser",
            password="testpass123",
            email="adminuser@home.com"
        )

        user.groups.add(admin_group)

        self.client.login(
            username="adminuser",
            password="testpass123"
        )

        response = self.client.get(
            reverse("admin_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200
        )


def test_reader_cannot_access_dashboard(self):
    """ Test that Reader role cannot access admin dashboard """
    reader_group = Group.objects.get(
        name="Reader"
    )

    user = User.objects.create_user(
        username="reader",
        password="testpass123"
    )

    user.groups.add(reader_group)

    self.client.login(
        username="reader",
        password="testpass123"
    )

    response = self.client.get(
        reverse("admin_dashboard")
    )

    self.assertNotEqual(
        response.status_code,
        200
    )


def test_admin_can_view_user_detail(self):
    """Test that an admin can view a user's detail page."""
    admin_group = Group.objects.get(
        name="Administrator"
    )

    admin = User.objects.create_user(
        username="admin",
        password="testpass123"
    )

    admin.groups.add(admin_group)

    target_user = User.objects.create_user(
        username="journalist",
        password="testpass123"
    )

    self.client.login(
        username="admin",
        password="testpass123"
    )

    response = self.client.get(
        reverse(
            "admin_user_detail",
            args=[target_user.id]
        )
    )

    self.assertEqual(
        response.status_code,
        200
    )

    self.assertContains(
        response,
        "journalist"
    )


def test_admin_can_assign_role(self):
    """ Test that an administrator can assign a role to another user. """
    admin_group = Group.objects.get(
        name="Administrator"
    )

    editor_group = Group.objects.get(
        name="Editor"
    )

    admin = User.objects.create_user(
        username="admin",
        password="testpass123"
    )

    admin.groups.add(admin_group)

    target_user = User.objects.create_user(
        username="user1",
        password="testpass123"
    )

    self.client.login(
        username="admin",
        password="testpass123"
    )

    response = self.client.post(
        reverse(
            "admin_user_detail",
            args=[target_user.id]
        ),
        {
            "roles": [editor_group.id]
        }
    )

    target_user.refresh_from_db()

    self.assertTrue(
        target_user.groups.filter(
            name="Editor"
        ).exists()
    )
