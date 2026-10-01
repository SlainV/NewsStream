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
    """
    Register a new user and add the user to the group
    matching the selected role.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            selected_role = form.cleaned_data["role"]

            role_group, created = Group.objects.get_or_create(
                name=selected_role
            )

            user.groups.add(role_group)

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


@login_required
def dashboard(request):
    user = request.user

    if user.groups.filter(
        name="Administrator"
    ).exists():
        return redirect(
            "admin_dashboard"
        )

    if user.groups.filter(
        name="Publisher Manager"
    ).exists():
        return redirect(
            "publisher_manager_area"
        )

    if user.groups.filter(
        name="Editor"
    ).exists():
        return redirect(
            "editor_area"
        )

    if user.groups.filter(
        name="Journalist"
    ).exists():
        return redirect(
            "journalist_area"
        )

    return redirect(
        "reader_dashboard"
    )


@login_required
@group_required("Reader")
def reader_dashboard(request):
    return render(
        request,
        "accounts/reader_dashboard.html",
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
    publishers = request.user.publishers.all()
    return render(
        request,
        "accounts/publisher_manager_area.html",
        {
            "publishers": publishers,
        },
    )


@login_required
@group_required("Journalist")
def journalist_area(request):
    articles = request.user.articles.order_by(
        "-created_at"
    )

    return render(
        request,
        "accounts/journalist_area.html",
        {
            "articles": articles,
        },
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
            selected_role = form.cleaned_data["role"]

            user_obj.role = selected_role
            user_obj.save()

            managed_groups = [
                "Reader",
                "Journalist",
                "Editor",
                "Publisher Manager",
                "Administrator",
            ]

            user_obj.groups.remove(
                *user_obj.groups.filter(
                    name__in=managed_groups
                )
            )

            group, created = Group.objects.get_or_create(
                name=selected_role
            )

            user_obj.groups.add(group)

            messages.success(
                request,
                "Role updated successfully."
            )

#            selected_roles = form.cleaned_data["roles"]

#            user_obj.groups.remove(
#                *user_obj.groups.filter(
#                    name__in=[
#                        "Reader",
#                        "Journalist",
#                        "Editor",
#                        "Publisher Manager",
#                    ]
#                )
#            )

#            user_obj.groups.add(*selected_roles)

#            messages.success(request,
#                             "Roles updated successfully.")

    else:
        form = RoleAssignmentForm(
           initial={
                "role": user_obj.role
               }
        )
#        form = RoleAssignmentForm(
#            initial={
#                "roles": user_obj.groups.filter(
#                    name__in=[
#                        "Reader",
#                        "Journalist",
#                        "Editor",
#                        "Publisher Manager",
#                    ]
#                )
#            }
#        )

    return render(
       request,
       "accounts/admin_user_detail.html",
       {
            "user_obj": user_obj,
            "form": form,
       },
       )
