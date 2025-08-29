from django.urls import path
from . import views

urlpatterns = [
    path("base_doc/", views.base_doc, name="base_doc"),
    path("seguimiento/", views.seguimiento, name="seguimiento"),
    path("proyectos/", views.proyectos, name="proyectos"),
    path("equipo/", views.equipo, name="equipo"),
    path("creditos/", views.creditos, name="creditos"),
]