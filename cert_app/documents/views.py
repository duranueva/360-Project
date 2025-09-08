from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.
@login_required
def base_doc(request):
    return render(request,"base_doc.html")


"""
    Sección Seguimiento
"""
def seg_aux_ine(request):
    ine_file = request.FILES.get("ine")
    candidato_id = request.POST.get("candidato_id")
    print(">> INE FILE:", ine_file)
    print(">> CANDIDATO ID:", candidato_id)
    if ine_file and candidato_id:
        if ine_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: INE")
            return redirect("seguimiento")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.ine = ine_file.read()
        candidato.save()
        return redirect("seguimiento")

def seg_aux_foto(request):
    foto_file = request.FILES.get("foto")
    candidato_id = request.POST.get("candidato_id")
    print(">> FOTO FILE:", foto_file)
    print(">> CANDIDATO ID:", candidato_id)
    if foto_file and candidato_id:
        if foto_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: FOTO")
            return redirect("seguimiento")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.foto = foto_file.read()
        candidato.save()
        return redirect("seguimiento")


def seg_aux_curp(request):
    curp_file = request.FILES.get("curp")
    candidato_id = request.POST.get("candidato_id")
    print(">> CURP FILE:", curp_file)
    print(">> CANDIDATO ID:", candidato_id)
    if curp_file and candidato_id:
        if curp_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: CURP")
            return redirect("seguimiento")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.curp = curp_file.read()
        candidato.save()
        return redirect("seguimiento")


def seg_aux_correo(request):
    correo = request.POST.get("correo")
    candidato_id = request.POST.get("candidato_id")
    print(">> CORREO:", correo)
    print(">> CANDIDATO ID:", candidato_id)
    if correo and candidato_id:
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.correo = correo
        candidato.save()
        return redirect("seguimiento")




@login_required
def seguimiento(request):
    path = r"C:\Users\costo\Downloads\test.jpg"
    """
    id = 1
    models.insert_file_to_bytea__candidato(id, path)
    """

    if request.method == "POST":
        if request.FILES.get("ine"):
            seg_aux_ine(request)
        elif request.FILES.get("foto"):
            seg_aux_foto(request)
        elif request.FILES.get("curp"):
            seg_aux_curp(request)
        elif request.POST.get("correo"):
            seg_aux_correo(request)
        # if portada ...
        


    candidatos = models.Candidato.objects.all()
    data = []

    for candidato in candidatos:
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato.id)
        except models.InfoProcesoCandidato.DoesNotExist:
            proceso = None

        data.append({
            "candidato": candidato,
            "proceso": proceso
        })

    return render(request, "seguimiento.html", {"candidatos_info": data})


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

