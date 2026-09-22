from django.contrib import admin
from .models import Publisher

# Register your models here.


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """A class for the admin interface of Publisher model."""
    list_display = (
        "name",
        "website",
        "is_active"
    )

    search_fields = (
        "name",
    )
