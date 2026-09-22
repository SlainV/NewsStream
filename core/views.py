from django.shortcuts import render

from articles.models import Article


def home(request):
    """Home page view.
    Shows list of approved articles in chronological order"""
    articles = (
        Article.objects.filter(status="approved")
        .select_related("author", "publisher", "category")
        .order_by("-created_at")
    )

    return render(
        request,
        "core/home.html",
        {"articles": articles},
    )
