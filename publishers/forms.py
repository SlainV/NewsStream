from django import forms
from django.contrib.auth import get_user_model

from .models import Publisher


User = get_user_model()


class PublisherForm(forms.ModelForm):
    """ Publisher form for creating and updating publishers."""
    class Meta:
        model = Publisher
        fields = [
            "name",
            "description",
            "website",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter a short publisher description",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
        }


class PublisherStaffForm(forms.Form):
    """Form for creating and updating publishers."""
    staff = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Journalists and Editors",
        help_text=(
            "Select the journalists and editors who should be "
            "affiliated with this publisher."
        ),
    )

    def __init__(self, *args, publisher=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.publisher = publisher

        self.fields["staff"].queryset = (
            User.objects.filter(
                groups__name__in=["Journalist", "Editor"]
            )
            .distinct()
            .order_by("username")
        )

        if publisher is not None:
            self.fields["staff"].initial = publisher.users.filter(
                groups__name__in=["Journalist", "Editor"]
            )
