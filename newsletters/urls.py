from django.urls import path
from . import views

app_name = "newsletters"

urlpatterns = [
    path("", views.subscription_manage, name="subscription_manage"),
    path("publishers/<int:publisher_id>/toggle/",
         views.publisher_subscription_toggle,
         name="publisher_subscription_toggle"),
    path(
        "journalists/<int:journalist_id>/toggle/",
        views.journalist_subscription_toggle,
        name="journalist_subscription_toggle"),
    path("list/", views.newsletter_list,
         name="newsletter_list"),
    path("create/", views.newsletter_create,
         name="newsletter_create"),
    path("<int:newsletter_id>/", views.newsletter_detail,
         name="newsletter_detail"),
    path("<int:newsletter_id>/edit/", views.newsletter_edit,
         name="newsletter_edit"),
    path("<int:newsletter_id>/delete/", views.newsletter_delete,
         name="newsletter_delete"),
]
