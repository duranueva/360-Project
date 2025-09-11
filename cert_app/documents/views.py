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

def seg_aux_portada(request):
    portada_file = request.FILES.get("portada")
    candidato_id = request.POST.get("candidato_id")
    print(">> PORTADA FILE:", portada_file)
    print(">> CANDIDATO ID:", candidato_id)
    if portada_file and candidato_id:
        if portada_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: PORTADA")
            return redirect("seguimiento")
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No existe InfoProcesoCandidato para el candidato")
            return redirect("seguimiento")
        proceso.portada = portada_file.read()
        proceso.save()
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

def seg_aux_indice(request):
    indice_file = request.FILES.get("indice")
    candidato_id = request.POST.get("candidato_id")
    print(">> INDICE FILE:", indice_file)
    print(">> CANDIDATO ID:", candidato_id)
    if indice_file and candidato_id:
        if indice_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: INDICE")
            return redirect("seguimiento")
        proceso, _ = models.InfoProcesoCandidato.objects.get_or_create(id_candidato_id=candidato_id)
        proceso.indice = indice_file.read()
        proceso.save()
        return redirect("seguimiento")

def seg_aux_carta_recepcion(request):
    file = request.FILES.get("carta_recepcion_docs")
    candidato_id = request.POST.get("candidato_id")
    if file and candidato_id:
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ Proceso no encontrado")
            return redirect("seguimiento")

        if file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: carta_recepcion_docs")
            return redirect("seguimiento")

        proceso.carta_recepcion_docs = file.read()
        proceso.save()
    return redirect("seguimiento")

def seg_aux_reporte_autenticidad(request):
    file = request.FILES.get("reporte_autenticidad")
    candidato_id = request.POST.get("candidato_id")
    print(">> REPORTE AUTENTICIDAD FILE:", file)
    print(">> CANDIDATO ID:", candidato_id)

    if file and candidato_id:
        if file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: REPORTE AUTENTICIDAD")
            return redirect("seguimiento")

        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ Proceso no encontrado.")
            return redirect("seguimiento")

        proceso.reporte_autenticidad = file.read()
        proceso.save()
        return redirect("seguimiento")

def seg_aux_triptico_derechos(request):
    triptico_file = request.FILES.get("triptico_derechos_img")
    candidato_id = request.POST.get("candidato_id")
    print(">> TRIPTICO FILE:", triptico_file)
    print(">> CANDIDATO ID:", candidato_id)

    if triptico_file and candidato_id:
        if triptico_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: TRIPTICO DERECHOS")
            return redirect("seguimiento")
        
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No existe InfoProcesoCandidato")
            return redirect("seguimiento")
        
        proceso.triptico_derechos_img = triptico_file.read()
        proceso.save()
        return redirect("seguimiento")

def seg_aux_encuesta_satisfaccion(request):
    archivo = request.FILES.get("encuesta_satisfaccion")
    candidato_id = request.POST.get("candidato_id")
    print(">> ENCUESTA:", archivo)
    print(">> CANDIDATO ID:", candidato_id)

    if archivo and candidato_id:
        if archivo.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: ENCUESTA SATISFACCION")
            return redirect("seguimiento")
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No existe InfoProcesoCandidato para el candidato")
            return redirect("seguimiento")
        proceso.encuesta_satisfaccion = archivo.read()
        proceso.save()
        return redirect("seguimiento")

def seg_aux_cedula_evaluacion(request):
    archivo = request.FILES.get("cedula_evaluacion")
    candidato_id = request.POST.get("candidato_id")
    print(">> CEDULA FILE:", archivo)
    print(">> CANDIDATO ID:", candidato_id)

    if archivo and candidato_id:
        if archivo.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: CEDULA")
            return redirect("seguimiento")

        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
            proceso.cedula_evaluacion = archivo.read()
            proceso.save()
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No se encontró el proceso para el candidato.")
        return redirect("seguimiento")

"""
@login_required
def seguimiento(request):
    
    if request.method == "POST":
        if request.FILES.get("ine"):
            seg_aux_ine(request)
        elif request.FILES.get("foto"):
            seg_aux_foto(request)
        elif request.FILES.get("curp"):
            seg_aux_curp(request)
        elif request.FILES.get("portada"):
            seg_aux_portada(request)
        elif request.FILES.get("indice"):
            seg_aux_indice(request)
        elif request.FILES.get("carta_recepcion_docs"):
            seg_aux_carta_recepcion(request)
        elif request.FILES.get("reporte_autenticidad"):
            seg_aux_reporte_autenticidad(request)
        elif request.FILES.get("triptico_derechos_img"):
            seg_aux_triptico_derechos(request)
        elif request.FILES.get("encuesta_satisfaccion"):
            seg_aux_encuesta_satisfaccion(request)
        elif request.FILES.get("cedula_evaluacion"):
            seg_aux_cedula_evaluacion(request)



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

"""
@login_required
def seguimiento(request,debug=True):
    
        https://chatgpt.com/share/68929281-4d54-800f-a451-01921c879339
    

    id_usuario = request.user.id
    id_ce = Usuario.get_id_ce__from_actual_user(id_usuario)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("id_ce ",id_ce)
        print("*************************")
        print("*************************")
        print("*************************")

    # Paso 1: Proyectos del CE
    proyectos = models.Proyecto.objects.filter(id_ce=id_ce).values_list("id", flat=True)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("proyectos ",proyectos)
        print("*************************")
        print("*************************")
        print("*************************")

    # Paso 2: Grupos de esos proyectos
    grupos = models.Grupo.objects.filter(id_proyecto__in=proyectos).values_list("id", flat=True)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("grupos ",grupos)
        print("*************************")
        print("*************************")
        print("*************************")

    # Paso 3: Procesos asociados a esos grupos
    procesos = models.InfoProcesoCandidato.objects.filter(id_grupo__in=grupos)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("procesos ",procesos)
        print("*************************")
        print("*************************")
        print("*************************")

    # Paso 4: Obtener los candidatos relacionados
    candidatos_ids = procesos.values_list("id_candidato_id", flat=True)
    candidatos = models.Candidato.objects.filter(id__in=candidatos_ids)

    # Construir la data a pasar al template
    data = []
    for candidato in candidatos:
        proceso = procesos.filter(id_candidato_id=candidato.id).first()
        data.append({
            "candidato": candidato,
            "proceso": proceso
        })

    return render(request, "seguimiento.html", {"candidatos_info": data})
"""

from admn_panel.models import Usuario  # importa el modelo desde la app correspondiente

@login_required
def seguimiento(request,debug=True):
    """
        https://chatgpt.com/share/68929281-4d54-800f-a451-01921c879339
    """

    id_usuario = request.user.id
    id_ce = Usuario.get_id_ce__from_actual_user(id_usuario)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("id_ce ",id_ce)
        print("*************************")
        print("*************************")
        print("*************************")

    # Obtener proyectos del centro evaluador
    proyectos = models.Proyecto.objects.filter(id_ce=id_ce)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("proyectos ",proyectos)
        print("*************************")
        print("*************************")
        print("*************************")

    # Obtener grupos relacionados a los proyectos
    grupos = models.Grupo.objects.filter(id_proyecto__in=proyectos)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("grupos ",grupos)
        print("*************************")
        print("*************************")
        print("*************************")

    # Obtener procesos que pertenezcan a esos grupos
    procesos = models.InfoProcesoCandidato.objects.filter(id_grupo__in=grupos)
    if debug:
        print("*************************")
        print("*************************")
        print("*************************")
        print("procesos ",procesos)
        print("*************************")
        print("*************************")
        print("*************************")

    # Obtener candidatos cuyos procesos están en los grupos anteriores
    data = []
    for proceso in procesos:
        data.append({
            "candidato": proceso.id_candidato,
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

