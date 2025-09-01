from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.
@login_required
def base_doc(request):
    return render(request,"base_doc.html")


"""
    Sección Seguimiento
"""
from django.forms.models import model_to_dict
@login_required
def seguimiento(request):
    """
    candidatos = models.Candidato.objects.all()
    candidatos_dicts = [model_to_dict(c) for c in candidatos]
    for c in candidatos:
        print(c) 
    return render(request, "seguimiento.html", {"candidatos": candidatos, "candidatos_dicts": candidatos_dicts})"""
    candidatos = models.Candidato.objects.all()
    candidatos_con_dict = [(c, model_to_dict(c)) for c in candidatos]
    return render(request, "seguimiento.html", {"candidatos_con_dict": candidatos_con_dict})


"""@login_required
def seguimiento(request):
    return render(request,"seguimiento.html")"""

"""
    Sección Proyectos
"""
@login_required
def proyectos(request):
    proyectos = ['Naucalpan', 'Xalapa', 'Morelos']
    return render(request, 'proyectos.html', {'proyectos': proyectos, 'active_section': 'proyectos'})
    #return render(request,"proyectos.html")

@login_required
def grupos(request):
    grupos = ['Grupo 1', 'Grupo 2', 'Grupo 3']
    return render(request,"grupos.html", {'grupos': grupos, 'active_section': 'proyectos'})

@login_required
def candidatos(request):
    candidatos = ['Israel Razo', 'Jean Duran', 'Regina G']
    return render(request,"candidatos.html", {'candidatos': candidatos, 'active_section': 'proyectos'})

@login_required
def candidato_n(request):
    return render(request,"candidato_n.html", {'active_section': 'proyectos'})


"""
    Sección Equipo
"""
@login_required
def equipo(request):
    return render(request,"equipo.html")

"""
    Sección Créditos
"""
@login_required
def creditos(request):
    return render(request,"creditos.html")

