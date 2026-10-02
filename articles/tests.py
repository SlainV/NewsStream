from django.test import TestCase
from django.contrib.auth import get_user_model
from publishers.models import Publisher
from articles.models import Category, Article
from articles.models import ApprovalLog
from django.contrib.auth.models import Group
from articles.services import approve_article
from unittest.mock import patch
from django.urls import reverse
from newsletters.models import Newsletter

# Create your tests here.

User = get_user_model()


class ArticleModelTests(TestCase):
    """Tests for the models."""
    def setUp(self):
        self.user = User.objects.create_user(
            username="journalist",
            password="testpass123",
            email="test@email.com"
        )

        self.publisher = Publisher.objects.create(
            name="Test Publisher"
        )

        self.category = Category.objects.create(
            name="Technology"
        )

    def test_article_creation(self):
        article = Article.objects.create(
            title="Test Article",
            content="Article content",
            author=self.user,
            publisher=self.publisher,
            category=self.category
        )

        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.author, self.user)

    def test_default_status_is_draft(self):
        article = Article.objects.create(
            title="Draft Article",
            content="Content",
            author=self.user,
            publisher=self.publisher,
            category=self.category
        )

        self.assertEqual(article.status, "draft")


class ApprovalLogTests(TestCase):
    """Test the ApprovalLog model."""
    def setUp(self):
        """Set up the test environment."""
        self.user = User.objects.create_user(
            username="editor",
            password="password",
            email="editor@example.com"
        )

        self.publisher = Publisher.objects.create(
            name="Publisher"
        )

        self.category = Category.objects.create(
            name="News"
        )

        self.article = Article.objects.create(
            title="Article",
            content="Body",
            author=self.user,
            publisher=self.publisher,
            category=self.category
        )

    def test_log_creation(self):
        """Test that an approval log is created when the article status changes."""
        log = ApprovalLog.objects.create(
            article=self.article,
            editor=self.user,
            action="approved",
            notes="Looks good"
        )

        self.assertEqual(log.action, "approved")
        self.assertEqual(log.notes, "Looks good")


class ApprovalServiceTests(TestCase):
    """Tests for the ApprovalService class."""
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="user",
            password="password",
            email="user@example.com",
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="password",
            email="editor@example.com"
        )

        self.author = User.objects.create_user(
            username="author",
            password="password",
            email="author@example.com"
        )

        self.publisher = Publisher.objects.create(
            name="Test Publisher"
        )

        self.category = Category.objects.create(
            name="Technology"
        )

        self.article = Article.objects.create(
            title="Pending Article",
            content="Content",
            author=self.author,
            publisher=self.publisher,
            category=self.category,
            status="submitted"
        )

    @patch("articles.services.requests.post")  # Mock the requests.post
    def test_article_can_be_approved(self, mock_post):
        """ Test that an article can be approved by the editor """
        mock_post.return_value.status_code = 200

        approve_article(
            article=self.article,
            editor=self.editor,
            notes="Approved for publication"
        )

        self.article.refresh_from_db()

        self.assertEqual(
            self.article.status,
            "approved"
        )
        self.assertEqual(
            self.article.reviewed_by,
            self.editor
        )
        self.assertTrue(
            ApprovalLog.objects.filter(
                article=self.article,
                editor=self.editor,
                action="approved",
                notes="Approved for publication"
            ).exists()
        )

        mock_post.assert_called_once()


class ArticleViewTests(TestCase):
    def setUp(self):
        self.journalist = User.objects.create_user(
            username="journalist",
            password="password",
            email="journalist@example.com"
        )

        self.other_user = User.objects.create_user(
            username="other",
            password="password",
            email="other@example.com"
        )

        self.publisher = Publisher.objects.create(
            name="Test Publisher"
        )

        self.journalist.publishers.add(self.publisher)

        self.category = Category.objects.create(
            name="Technology"
        )

        self.article = Article.objects.create(
            title="My Article",
            content="Content",
            author=self.journalist,
            publisher=self.publisher,
            category=self.category
        )

        self.journalist_group, _ = Group.objects.get_or_create(
            name="Journalist"
        )
        self.editor_group, _ = Group.objects.get_or_create(
            name="Editor"
        )

        self.journalist.groups.add(self.journalist_group)

        self.other_user.groups.add(self.journalist_group)

        self.editor = User.objects.create_user(
            username="editor",
            password="password",
            email="editor@example.com",
        )

        self.editor.groups.add(
            self.editor_group
        )

    def test_article_list_view(self):
        self.client.login(
            username="journalist",
            password="password"
        )

        response = self.client.get(
            reverse("article_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Article")

    def test_journalist_can_edit_own_article(self):
        self.client.login(
            username="journalist",
            password="password"
        )

        response = self.client.get(
            reverse(
                "article_edit",
                args=[self.article.pk]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_edit_other_users_article(self):
        self.client.login(
            username="other",
            password="password"
        )

        response = self.client.get(
            reverse(
                "article_edit",
                args=[self.article.pk]
            )
        )

        self.assertEqual(response.status_code, 404)

def test_journalist_can_view_delete_confirmation_for_own_article(self):
    self.client.login(
        username="journalist",
        password="password",
    )

    response = self.client.get(
        reverse(
            "article_delete",
            args=[self.article.pk],
        )
    )

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.article.title)


def test_journalist_can_delete_own_article(self):
    self.client.login(
        username="journalist",
        password="password",
    )

    response = self.client.post(
        reverse(
            "article_delete",
            args=[self.article.pk],
        )
    )

    self.assertRedirects(
        response,
        reverse("article_list"),
    )

    self.assertFalse(
        Article.objects.filter(
            pk=self.article.pk
        ).exists()
    )


def test_journalist_cannot_delete_another_users_article(self):
    self.client.login(
        username="other",
        password="password",
    )

    response = self.client.post(
        reverse(
            "article_delete",
            args=[self.article.pk],
        )
    )

    self.assertEqual(response.status_code, 404)

    self.assertTrue(
        Article.objects.filter(
            pk=self.article.pk
        ).exists()
    )


def test_editor_can_edit_article(self):
    self.client.login(
        username="editor",
        password="password",
    )

    response = self.client.get(
        reverse(
            "article_edit",
            args=[self.article.pk],
        )
    )

    self.assertEqual(response.status_code, 200)


def test_editor_can_delete_article(self):
    self.client.login(
        username="editor",
        password="password",
    )

    response = self.client.post(
        reverse(
            "article_delete",
            args=[self.article.pk],
        )
    )

    self.assertRedirects(
        response,
        reverse("article_list"),
    )

    self.assertFalse(
        Article.objects.filter(
            pk=self.article.pk
        ).exists()
    )


class NewsletterManagementTests(TestCase):
    """Tests for newsletter editing and deletion."""

    def setUp(self):
        journalist_group, _ = Group.objects.get_or_create(
            name="Journalist"
        )
        editor_group, _ = Group.objects.get_or_create(
            name="Editor"
        )

        self.journalist = User.objects.create_user(
            username="journalist_manager",
            password="password123",
            email="journalist_manager@test.com",
        )
        self.journalist.groups.add(journalist_group)

        self.other_journalist = User.objects.create_user(
            username="other_journalist",
            password="password123",
            email="other_journalist@test.com",
        )
        self.other_journalist.groups.add(journalist_group)

        self.editor = User.objects.create_user(
            username="newsletter_editor",
            password="password123",
            email="newsletter_editor@test.com",
        )
        self.editor.groups.add(editor_group)

        self.newsletter = Newsletter.objects.create(
            title="Weekly News",
            description="A weekly collection of articles.",
            author=self.journalist,
        )

    def test_journalist_can_edit_own_newsletter(self):
        self.client.login(
            username="journalist_manager",
            password="password123",
        )

        response = self.client.get(
            reverse(
                "newsletters:newsletter_edit",
                args=[self.newsletter.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_journalist_can_delete_own_newsletter(self):
        self.client.login(
            username="journalist_manager",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "newsletters:newsletter_delete",
                args=[self.newsletter.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("newsletters:newsletter_list"),
        )

        self.assertFalse(
            Newsletter.objects.filter(
                pk=self.newsletter.pk
            ).exists()
        )

    def test_journalist_cannot_delete_another_newsletter(self):
        self.client.login(
            username="other_journalist",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "newsletters:newsletter_delete",
                args=[self.newsletter.pk],
            )
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            Newsletter.objects.filter(
                pk=self.newsletter.pk
            ).exists()
        )

    def test_editor_can_edit_newsletter(self):
        self.client.login(
            username="newsletter_editor",
            password="password123",
        )

        response = self.client.get(
            reverse(
                "newsletters:newsletter_edit",
                args=[self.newsletter.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_editor_can_delete_newsletter(self):
        self.client.login(
            username="newsletter_editor",
            password="password123",
        )

        response = self.client.post(
            reverse(
                "newsletters:newsletter_delete",
                args=[self.newsletter.pk],
            )
        )

        self.assertRedirects(
            response,
            reverse("newsletters:newsletter_list"),
        )

        self.assertFalse(
            Newsletter.objects.filter(
                pk=self.newsletter.pk
            ).exists()
        )
