from django.urls import path
from . import views

urlpatterns = [
    # Base para el diseño de Centro Evaluador
    path("base_doc/", views.base_doc, name="base_doc"),

    # Sección "Seguimiento" 
    path("seguimiento/", views.seguimiento, name="seguimiento"),
    
    # Sección "Equipo"
    path("equipo/", views.equipo, name="equipo"),
    
    # Sección "Créditos"
    path("creditos/", views.creditos, name="creditos"),

    # Sección "Proyectos"
    path("proyectos/", views.proyectos, name="proyectos"),
    path("grupos/", views.grupos, name="grupos"),
    path("candidatos/", views.candidatos, name="candidatos"),
    path("candidato_n/", views.candidato_n, name="candidato_n"),
]