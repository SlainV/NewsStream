from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, ArticleReviewForm
from .models import Article
from django.shortcuts import get_object_or_404
from django.contrib import messages
from accounts.decorators import group_required
from .services import approve_article, reject_article
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

# Create your views here.

def user_can_manage_articles(user):
    """Return True when the user is a Journalist or Editor."""
    return user.groups.filter(
        name__in=["Journalist", "Editor"]
    ).exists()


def get_manageable_article(user, article_id):
    """
    Return an article the current user is allowed to manage.

    Editors can manage any article.
    Journalists can manage only their own articles.
    """
    if user.is_editor:
        return get_object_or_404(
            Article,
            id=article_id,
        )

    if user.is_journalist:
        return get_object_or_404(
            Article,
            id=article_id,
            author=user,
        )

    raise PermissionDenied

@login_required
@group_required("Journalist")
def article_create(request):
    """Create an article based on the given data."""

    if not request.user.publishers.exists():
        messages.error(
            request,
            "You must be affiliated with a publisher before creating articles."
        )

        return redirect(
            "journalist_area"
        )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            return redirect("article_list")

    else:
        form = ArticleForm(user=request.user)

    return render(
        request,
        "articles/article_form.html",
        {"form": form},
    )


@login_required
def article_list(request):
    """List articles the current user is allowed to manage."""
    if request.user.is_editor:
        articles = Article.objects.select_related(
            "author",
            "publisher",
            "category",
        ).all()
    elif request.user.is_journalist:
        articles = Article.objects.filter(
            author=request.user
        ).select_related(
            "author",
            "publisher",
            "category",
        )
    else:
        raise PermissionDenied

    articles = articles.order_by("-created_at")

    return render(
        request,
        "articles/article_list.html",
        {
            "articles": articles,
        },
    )


@login_required
def article_detail(request, article_id):
    """Show an article the current user is allowed to manage."""
    if not user_can_manage_articles(request.user):
        raise PermissionDenied

    article = get_manageable_article(
        request.user,
        article_id,
    )

    return render(
        request,
        "articles/article_detail.html",
        {
            "article": article,
        },
    )


@login_required
def article_edit(request, article_id):
    """Edit an article the current user is allowed to manage."""
    if not user_can_manage_articles(request.user):
        raise PermissionDenied

    article = get_manageable_article(
        request.user,
        article_id,
    )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            instance=article,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Article updated successfully.",
            )

            return redirect(
                "article_detail",
                article_id=article.id,
            )
    else:
        form = ArticleForm(
            instance=article,
            user=request.user,
        )

    return render(
        request,
        "articles/article_form.html",
        {
            "form": form,
            "article": article,
            "title": "Edit Article",
        },
    )


@login_required
@group_required("Editor")
def review_queue(request):

    articles = Article.objects.filter(
        status="draft"
    ).select_related(
        "author",
        "publisher",
    )

    return render(
        request,
        "articles/review_queue.html",
        {
            "articles": articles,
        },
    )


@login_required
@group_required("Editor")
def review_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        status="draft",
    )

    if request.method == "POST":

        form = ArticleReviewForm(request.POST)

        if form.is_valid():

            action = form.cleaned_data["action"]
            notes = form.cleaned_data["notes"]

            if action == "approved":
                approve_article(
                    article=article,
                    editor=request.user,
                    notes=notes,
                )

            elif action == "rejected":
                reject_article(
                    article=article,
                    editor=request.user,
                    notes=notes,
                )

            messages.success(
                request,
                "Review completed.",
            )

            return redirect(
                "review_queue"
            )

    else:

        form = ArticleReviewForm()

    return render(
        request,
        "articles/review_article.html",
        {
            "article": article,
            "form": form,
        },
    )


def public_article_list(request):
    """Public list of approved articles for homepage."""
    articles = (
        Article.objects.filter(status="approved")
        .order_by("-created_at")
    )

    return render(
        request,
        "articles/public_article_list.html",
        {"articles": articles},
    )


def public_article_detail(request, pk):
    """Public detail view for an approved article."""
    article = get_object_or_404(
        Article.objects.select_related(
            "author",
            "publisher",
            "category",
        ),
        pk=pk,
        status="approved",
    )

    return render(
        request,
        "articles/public_article_detail.html",
        {"article": article},
    )


@login_required
def article_delete(request, article_id):
    """Delete an article the current user is allowed to manage."""
    if not user_can_manage_articles(request.user):
        raise PermissionDenied

    article = get_manageable_article(
        request.user,
        article_id,
    )

    if request.method == "POST":
        article_title = article.title
        article.delete()

        messages.success(
            request,
            f'Article "{article_title}" deleted successfully.',
        )

        return redirect("article_list")

    return render(
        request,
        "articles/article_confirm_delete.html",
        {
            "article": article,
        },
    )
