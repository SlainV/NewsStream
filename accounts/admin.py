from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """ Custom user admin """
    fieldsets = UserAdmin.fieldsets + (
        (
            "Publishers",
            {
                "fields": ("publishers",)
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions", "publishers")
