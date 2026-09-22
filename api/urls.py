from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (ApprovedArticleListAPIView, approved_article_log,
                    CategoryListAPIView, PublisherListAPIView,
                    ProtectedAPIView)

urlpatterns = [
    path("approved/", approved_article_log, name="approved_article_log"),
    path("token/", obtain_auth_token, name="api_token"),
    path("articles/", ApprovedArticleListAPIView.as_view(), name="api_articles"),
    path("categories/", CategoryListAPIView.as_view(), name="api_categories"),
    path("publishers/", PublisherListAPIView.as_view(), name="api_publishers"),
    path("protected/", ProtectedAPIView.as_view(), name="api_protected"),
]
