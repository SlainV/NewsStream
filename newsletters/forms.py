from django import forms
from articles.models import Article
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            "title",
            "description",
            "articles",
        ]

        widgets = {
            "articles": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        approved_articles = Article.objects.filter(
            status="approved"
        )
        if (
            user
            and user.groups.filter(
                name="Journalist"
            ).exists()
        ):
            approved_articles = approved_articles.filter(
              author=user
            )
        self.fields["articles"].queryset = approved_articles
