from django.urls import path
from . import views

urlpatterns = [
    path("test_1/", views.test_1, name="test_1"),
    path("base_ad/", views.base_ad, name="base_ad"),
    path("estandares/", views.estandares, name="estandares"),
    path("control/", views.control, name="control"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("formularios/", views.formularios, name="formularios"),
]