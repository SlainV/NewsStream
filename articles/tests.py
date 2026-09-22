from django.test import TestCase
from django.contrib.auth import get_user_model
from publishers.models import Publisher
from articles.models import Category, Article
from articles.models import ApprovalLog
# from django.contrib.auth.models import Group
from articles.services import approve_article
from unittest.mock import patch
from django.urls import reverse


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


    @patch("articles.services.requests.post") # Mock the requests.post function
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


from django.urls import reverse


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
