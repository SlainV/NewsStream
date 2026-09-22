from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("create/", views.article_create, name="article_create"),
    path("<int:article_id>/", views.article_detail, name="article_detail"),
    path("<int:article_id>/edit/", views.article_edit, name="article_edit"),
    path("review/", views.review_queue, name="review_queue"),
    path("review/<int:article_id>/", views.review_article,
         name="review_article"),
    path("news/", views.public_article_list, name="public_article_list"),
    path("news/<int:pk>/", views.public_article_detail,
         name="public_article_detail"),
]
