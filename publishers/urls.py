from django.urls import path

from . import views


app_name = "publishers"


urlpatterns = [
    path("", views.publisher_manager_dashboard, name="dashboard"),
    path("create/", views.publisher_create,
         name="publisher_create"),
    path("<int:publisher_id>/edit/", views.publisher_edit,
         name="publisher_edit"),
    path("<int:publisher_id>/staff/", views.publisher_staff,
         name="publisher_staff"),
    path("directory/", views.public_publisher_list,
         name="public_publisher_list"),
]
