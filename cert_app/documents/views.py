from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def base_doc(request):
    return render(request,"base_doc.html")

from . import models
@login_required
def seguimiento(request):
    candidatos = models.Candidato.objects.all()
    return render(request, "seguimiento.html", {"candidatos": candidatos})


"""@login_required
def seguimiento(request):
    return render(request,"seguimiento.html")"""

@login_required
def proyectos(request):
    return render(request,"proyectos.html")

@login_required
def equipo(request):
    return render(request,"equipo.html")

@login_required
def creditos(request):
    return render(request,"creditos.html")