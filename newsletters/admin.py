from django.contrib import admin

from .models import JournalistSubscription, PublisherSubscription

# Register your models here.


@admin.register(PublisherSubscription)
class PublisherSubscriptionAdmin(admin.ModelAdmin):
    """ Manage the publisher subscription through the Admin portal. """
    
    list_display = (
        "subscriber",
        "publisher",
        "created_at",
    )

    list_filter = (
        "publisher",
        "created_at",
    )

    search_fields = (
        "subscriber__username",
        "publisher__name",
    )


@admin.register(JournalistSubscription)
class JournalistSubscriptionAdmin(admin.ModelAdmin):
    """ Manage the journalist subscription through the Admin portal. """
    list_display = (
        "subscriber",
        "journalist",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "subscriber__username",
        "journalist__username",
    )
