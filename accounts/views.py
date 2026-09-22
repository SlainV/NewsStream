from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from django.contrib import messages

from .decorators import group_required

from .forms import UserRegistrationForm
from .forms import RoleAssignmentForm

User = get_user_model()


def register(request):
    """Register a new user.
    If the form is valid, create a new user and log them in.
    If the form is invalid, display the registration form again. """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            reader_group = Group.objects.get(
                name="Reader"
            )
            user.groups.add(reader_group)
            # automatically adds new registrants as readers

            login(request, user)

            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """Show the dashboard for a specific user."""
    context = {
        "is_admin": request.user.groups.filter(
            name="Administrator"
        ).exists(),
        "is_publisher_manager": request.user.groups.filter(
            name="Publisher Manager"
        ).exists(),
        "is_journalist": request.user.groups.filter(
            name="Journalist"
        ).exists(),
        "is_editor": request.user.groups.filter(
            name="Editor"
        ).exists(),
        "is_reader": request.user.groups.filter(
            name="Reader"
        ).exists(),
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )


@login_required
@group_required("Editor")
def editor_area(request):
    return render(
        request,
        "accounts/editor_area.html"
    )


@login_required
@group_required("Publisher Manager")
def publisher_manager_area(request):
    return render(
        request,
        "accounts/publisher_manager_area.html"
    )


@login_required
@group_required("Journalist")
def journalist_area(request):
    return render(
        request,
        "accounts/journalist_area.html",
    )


@login_required
@group_required("Administrator")
def admin_dashboard(request):
    """Admin dashboard for other user admin functions"""
    users = User.objects.all().order_by("username")

    return render(
        request,
        "accounts/admin_dashboard.html",
        {
            "users": users,
        },
    )


@login_required
@group_required("Administrator")
def admin_user_detail(request, user_id):
    """Admin view of other user details"""
    user_obj = get_object_or_404(
        User,
        pk=user_id,
    )

    if request.method == "POST":
        form = RoleAssignmentForm(request.POST)

        if form.is_valid():
            selected_roles = form.cleaned_data["roles"]

            user_obj.groups.remove(
                *user_obj.groups.filter(
                    name__in=[
                        "Reader",
                        "Journalist",
                        "Editor",
                        "Publisher Manager",
                    ]
                )
            )

            user_obj.groups.add(*selected_roles)

            messages.success(request,
                             "Roles updated successfully.")

    else:
        form = RoleAssignmentForm(
            initial={
                "roles": user_obj.groups.filter(
                    name__in=[
                        "Reader",
                        "Journalist",
                        "Editor",
                        "Publisher Manager",
                    ]
                )
            }
        )

    return render(
       request,
       "accounts/admin_user_detail.html",
       {
            "user_obj": user_obj,
            "form": form,
       },
       )
