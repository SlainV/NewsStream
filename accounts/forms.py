from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import User


class UserRegistrationForm(UserCreationForm):
    """User registration form."""

    role = forms.ChoiceField(
        choices=[
            (User.Role.READER, "Reader"),
            (User.Role.JOURNALIST, "Journalist"),
            (User.Role.EDITOR, "Editor"),
        ],
        initial=User.Role.READER,
        help_text="Choose the type of account you want to register.",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
        ]

"""
class RoleAssignmentForm(forms.Form):
    
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
"""


class RoleAssignmentForm(forms.Form):
    role = forms.ChoiceField(
        choices=User.Role.choices
    )
