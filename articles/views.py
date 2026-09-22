from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, ArticleReviewForm
from .models import Article
from django.shortcuts import get_object_or_404
from django.contrib import messages
from accounts.decorators import group_required
from .services import approve_article, reject_article

# Create your views here.


@login_required
def article_create(request):
    """Create an article based on the given data."""

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
    """List all the articles created by the current user."""

    articles = Article.objects.filter(
        author=request.user
    ).order_by("-created_at")

    return render(
        request,
        "articles/article_list.html",
        {"articles": articles},
    )


@login_required
def article_detail(request, article_id):
    """Show the details of a specific article."""

    article = get_object_or_404(
        Article,
        id=article_id,
        author=request.user,
    )

    return render(
        request,
        "articles/article_detail.html",
        {"article": article},
    )


@login_required
def article_edit(request, article_id):
    """Edit an existing article."""

    article = get_object_or_404(
        Article,
        id=article_id,
        author=request.user,
    )

    if request.method == "POST":

        form = ArticleForm(
            request.POST,
            instance=article,
            user=request.user,
        )

        if form.is_valid():
            form.save()
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

            # article.status = action
            # article.reviewed_by = request.user
            # article.reviewed_at = timezone.now()
            # article.save()

            # ApprovalLog.objects.create(
            #    article=article,
            #    editor=request.user,
            #    action=action,
            #    notes=notes,
            # )

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

            # approve_article(article, request.user)

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
