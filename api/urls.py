from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (ApprovedArticleListAPIView, approved_article_log,
                    CategoryListAPIView, PublisherListAPIView,
                    ProtectedAPIView, ArticleDetailAPIView,
                    SubscribedArticlesAPIView, ArticleCreateAPIView,
                    ArticleUpdateAPIView, ArticleDeleteAPIView)

urlpatterns = [
    path("approved/", approved_article_log, name="approved_article_log"),
    path("token/", obtain_auth_token, name="api_token"),
    path("articles/", ApprovedArticleListAPIView.as_view(), name="api_articles"),
    path("categories/", CategoryListAPIView.as_view(), name="api_categories"),
    path("publishers/", PublisherListAPIView.as_view(), name="api_publishers"),
    path("protected/", ProtectedAPIView.as_view(), name="api_protected"),
    path("articles/<int:pk>/", ArticleDetailAPIView.as_view(),
         name="article-detail"),
    path("articles/subscribed/", SubscribedArticlesAPIView.as_view(),
         name="subscribed-articles"),
    path("articles/create/", ArticleCreateAPIView.as_view(),
         name="article-create"),
    path("articles/<int:pk>/update/", ArticleUpdateAPIView.as_view(),
         name="article-update"),
    path("articles/<int:pk>/delete/", ArticleDeleteAPIView.as_view(),
         name="article-delete"),
]
