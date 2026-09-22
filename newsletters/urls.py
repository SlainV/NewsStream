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
]
