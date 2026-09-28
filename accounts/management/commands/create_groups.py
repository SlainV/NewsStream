from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from articles.models import Category


class Command(BaseCommand):
    """Create default groups and categories."""

    def handle(self, *args, **kwargs):
        # Groups
        groups = [
            "Administrator",
            "Publisher Manager",
            "Journalist",
            "Editor",
            "Reader",
        ]

        for group_name in groups:
            Group.objects.get_or_create(name=group_name)

        # Categories
        categories = [
            "Politics",
            "Business",
            "Technology",
            "Sports",
            "Entertainment",
            "Education",
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)

        self.stdout.write(
            self.style.SUCCESS(
                "Groups and categories created."
            )
        )
