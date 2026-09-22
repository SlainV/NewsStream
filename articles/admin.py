from django.contrib import admin
from .models import Article, Category, ApprovalLog

# Register your models here.

admin.site.register(ApprovalLog)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""
    list_display = ["name"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Article admin."""
    list_display = [
        "title",
        "publisher",
        "author",
        "status",
        "created_at",
    ]

    list_filter = [
        "status",
        "publisher",
    ]
