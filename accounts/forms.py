from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

from .models import User


class UserRegistrationForm(UserCreationForm):
    """ User registration form. """
    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]


class RoleAssignmentForm(forms.Form):
    """ Form for assigning roles to users by the admin user. """
    roles = forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(
            name__in=[
                "Reader",
                "Journalist",
                "Editor",
                "Publisher Manager",
            ]
        ).order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
