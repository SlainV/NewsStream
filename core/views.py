from django.shortcuts import render

from articles.models import Article


def home(request):
    """Landing page showing the latest approved articles."""

    articles = (
        Article.objects.filter(status="approved")
        .select_related("author", "publisher", "category")
        .order_by("-created_at")[:3]
    )

    return render(
        request,
        "core/home.html",
        {"articles": articles},
    )
