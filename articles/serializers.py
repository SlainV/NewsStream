from rest_framework import serializers
from .models import Article
from articles.models import Category
from publishers.models import Publisher


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the Article model."""
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "category",
            "status",
            "created_at",
        ]


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
