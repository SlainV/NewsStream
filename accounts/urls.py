from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("journalist/", views.journalist_area, name="journalist_area"),
    path("editor/", views.editor_area, name="editor_area"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/users/<int:user_id>/", views.admin_user_detail,
         name="admin_user_detail"),
]
