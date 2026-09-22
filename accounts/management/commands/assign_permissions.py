from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """Command to assign permissions to the Default roles"""

    def handle(self, *args, **kwargs):

        configs = {
            "Administrator": [
                "add_user",
                "change_user",
                "delete_user",
                "view_user",
            ],
            "Journalist": [],
            "Editor": [],
            "Publisher Manager": [],
            "Reader": [],
        }

        for group_name in configs:
            Group.objects.get_or_create(
                name=group_name
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Initial role configuration complete."
            )
        )
