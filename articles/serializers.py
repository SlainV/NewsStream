from rest_framework import serializers
from articles.models import Article, Category
from publishers.models import Publisher


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer used to read, create, and update articles.
    """

    author = serializers.StringRelatedField(
        read_only=True
    )

    publisher = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.filter(
            is_active=True
        )
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    publisher_name = serializers.CharField(
        source="publisher.name",
        read_only=True,
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Article

        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "publisher_name",
            "category",
            "category_name",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "author",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_publisher(self, publisher):
        """
        Journalists may only use affiliated publishers.
        """
        request = self.context.get("request")

        if request is None:
            return publisher

        user = request.user

        if (
            user.is_authenticated
            and user.role == "Journalist"
        ):
            if not user.publishers.exists():
                raise serializers.ValidationError(
                    "You must be affiliated with a "
                    "publisher before creating or "
                    "updating articles."
                )

            if not user.publishers.filter(
                pk=publisher.pk
            ).exists():
                raise serializers.ValidationError(
                    "You may only use a publisher with "
                    "which you are affiliated."
                )

        return publisher

    def create(self, validated_data):
        """
        Create a draft article owned by the authenticated
        API user.
        """
        request = self.context.get("request")

        return Article.objects.create(
            author=request.user,
            status="draft",
            **validated_data,
        )

    def update(self, instance, validated_data):
        """
        Update article content without allowing the API
        to change the approval status.
        """
        validated_data.pop("status", None)
        validated_data.pop("author", None)

        return super().update(
            instance,
            validated_data,
        )


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    class Meta:
        model = Category
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for the Publisher model."""
    class Meta:
        model = Publisher
        fields = [
            "id",
            "name",
            "description",
            "website",
        ]
