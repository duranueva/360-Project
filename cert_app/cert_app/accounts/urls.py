from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("home/", views.home, name="home"),
    path("home2/", views.home2, name="home2"),
    path("start/", views.start, name="start"),
    path("logout/", views.custom_logout, name="logout"),
]