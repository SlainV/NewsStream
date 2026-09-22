from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    """Form for articles."""

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["publisher"].queryset = (
                user.publishers.all()
            )

    class Meta:
        model = Article

        fields = [
            "publisher",
            "category",
            "title",
            "content",
        ]


class ArticleReviewForm(forms.Form):
    """Form for article reviews."""

    action = forms.ChoiceField(
        choices=[
            ("approved", "Approve"),
            ("rejected", "Reject"),
        ]
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
