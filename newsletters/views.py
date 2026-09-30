from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from publishers.models import Publisher

from .models import JournalistSubscription, PublisherSubscription, Newsletter
from .forms import NewsletterForm

# Create your views here.

User = get_user_model()


@login_required
def subscription_manage(request):
    """ Manage the subscriptions"""
    publishers = Publisher.objects.filter(
        is_active=True
    ).order_by("name")

    journalists = User.objects.filter(
        groups__name="Journalist",
        is_active=True,
    ).distinct().order_by("username")

    subscribed_publisher_ids = list(
        PublisherSubscription.objects.filter(
            subscriber=request.user
        ).values_list("publisher_id", flat=True)
    )

    subscribed_journalist_ids = list(
        JournalistSubscription.objects.filter(
            subscriber=request.user
        ).values_list("journalist_id", flat=True)
    )

    context = {
        "publishers": publishers,
        "journalists": journalists,
        "subscribed_publisher_ids": subscribed_publisher_ids,
        "subscribed_journalist_ids": subscribed_journalist_ids,
    }

    return render(
        request,
        "newsletters/subscription_manage.html",
        context,
    )


@login_required
@require_POST
def publisher_subscription_toggle(request, publisher_id):
    """ Toggle the publisher subscription. """
    publisher = get_object_or_404(
        Publisher,
        id=publisher_id,
        is_active=True,
    )

    subscription, created = (
        PublisherSubscription.objects.get_or_create(
            subscriber=request.user,
            publisher=publisher,
        )
    )

    if created:
        messages.success(
            request,
            f"You subscribed to {publisher.name}.",
        )
    else:
        subscription.delete()

        messages.success(
            request,
            f"You unsubscribed from {publisher.name}.",
        )

    return redirect("newsletters:subscription_manage")


@login_required
@require_POST
def journalist_subscription_toggle(request, journalist_id):
    """ Toggle the journalist subscription. """
    journalist = get_object_or_404(
        User,
        id=journalist_id,
        groups__name="Journalist",
        is_active=True,
    )

    subscription, created = (
        JournalistSubscription.objects.get_or_create(
            subscriber=request.user,
            journalist=journalist,
        )
    )

    if created:
        messages.success(
            request,
            f"You subscribed to {journalist.username}.",
        )
    else:
        subscription.delete()

        messages.success(
            request,
            f"You unsubscribed from {journalist.username}.",
        )

    return redirect("newsletters:subscription_manage")


@login_required
def newsletter_create(request):
    """Create a newsletter."""

    if not request.user.groups.filter(
        name__in=["Journalist", "Editor"]
    ).exists():
        return redirect("dashboard")

    if request.method == "POST":
        form = NewsletterForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            newsletter = form.save(
                commit=False
            )

            newsletter.author = request.user
            newsletter.save()

            form.save_m2m()

            messages.success(
                request,
                "Newsletter created successfully."
            )

            return redirect(
                "newsletters:newsletter_detail",
                newsletter.id,
            )

    else:
        form = NewsletterForm(
            user=request.user
        )

    return render(
        request,
        "newsletters/newsletter_form.html",
        {
            "form": form,
            "title": "Create Newsletter",
        },
    )


def newsletter_detail(
    request,
    newsletter_id,
):
    """Display a newsletter."""

    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    return render(
        request,
        "newsletters/newsletter_detail.html",
        {
            "newsletter": newsletter,
        },
    )


def newsletter_list(request):
    """Display all newsletters."""

    newsletters = Newsletter.objects.all()

    return render(
        request,
        "newsletters/newsletter_list.html",
        {
            "newsletters": newsletters,
        },
    )


@login_required
def newsletter_edit(
    request,
    newsletter_id,
):
    """Edit a newsletter."""

    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    is_editor = request.user.groups.filter(
        name="Editor"
    ).exists()

    if (
        newsletter.author != request.user
        and not is_editor
    ):
        return redirect(
            "newsletters:newsletter_detail",
            newsletter.id,
        )

    if request.method == "POST":
        form = NewsletterForm(
            request.POST,
            instance=newsletter,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Newsletter updated successfully."
            )

            return redirect(
                "newsletters:newsletter_detail",
                newsletter.id,
            )

    else:
        form = NewsletterForm(
            instance=newsletter,
            user=request.user,
        )

    return render(
        request,
        "newsletters/newsletter_form.html",
        {
            "form": form,
            "title": "Edit Newsletter",
        },
    )