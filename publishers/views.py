from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import group_required

from .forms import PublisherForm, PublisherStaffForm
from .models import Publisher


@group_required("Publisher Manager")
def publisher_manager_dashboard(request):
    """  Dashboard view for the Publisher Manager."""
    publishers = Publisher.objects.prefetch_related("users").order_by("name")

    context = {
        "publishers": publishers,
    }

    return render(
        request,
        "publishers/dashboard.html",
        context,
    )


@group_required("Publisher Manager")
def publisher_create(request):
    """  Create a new publisher."""
    if request.method == "POST":
        form = PublisherForm(request.POST)

        if form.is_valid():
            publisher = form.save()

            messages.success(
                request,
                f"{publisher.name} was created successfully.",
            )

            return redirect("publishers:publisher_staff", publisher.id)
    else:
        form = PublisherForm()

    context = {
        "form": form,
        "page_title": "Create Publisher",
        "button_text": "Create Publisher",
    }

    return render(
        request,
        "publishers/publisher_form.html",
        context,
    )


@group_required("Publisher Manager")
def publisher_edit(request, publisher_id):
    """  Edit an existing publisher."""
    publisher = get_object_or_404(
        Publisher,
        id=publisher_id,
    )

    if request.method == "POST":
        form = PublisherForm(
            request.POST,
            instance=publisher,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                f"{publisher.name} was updated successfully.",
            )

            return redirect("publishers:dashboard")
    else:
        form = PublisherForm(instance=publisher)

    context = {
        "form": form,
        "publisher": publisher,
        "page_title": "Edit Publisher",
        "button_text": "Save Changes",
    }

    return render(
        request,
        "publishers/publisher_form.html",
        context,
    )


@group_required("Publisher Manager")
def publisher_staff(request, publisher_id):
    """View to manage staff for a specific publisher."""
    publisher = get_object_or_404(
        Publisher,
        id=publisher_id,
    )

    if request.method == "POST":
        form = PublisherStaffForm(
            request.POST,
            publisher=publisher,
        )

        if form.is_valid():
            selected_staff = form.cleaned_data["staff"]

            eligible_staff = publisher.users.filter(
                groups__name__in=["Journalist", "Editor"]
            ).distinct()

            publisher.users.remove(*eligible_staff)
            publisher.users.add(*selected_staff)

            messages.success(
                request,
                f"Staff affiliations for {publisher.name} were updated.",
            )

            return redirect("publishers:dashboard")
    else:
        form = PublisherStaffForm(
            publisher=publisher,
        )

    context = {
        "form": form,
        "publisher": publisher,
    }

    return render(
        request,
        "publishers/publisher_staff.html",
        context,
    )


def public_publisher_list(request):
    """List all active publishers."""
    publishers = Publisher.objects.filter(
        is_active=True
    ).order_by("name")

    return render(
        request,
        "publishers/public_publisher_list.html",
        {"publishers": publishers},
    )
