from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from admn_panel.models import Usuario, EC, CeEc  # importa el modelo desde la app correspondiente
from django.contrib import messages  # para mostrar mensajes opcionales
from django.db import IntegrityError

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
            messages.error(request, f"❌ Archivo no válido para campo binario: INE")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.ine = ine_file.read()
        candidato.save()
        messages.success(request, f"INE agregado correctamente")

def seg_aux_foto(request):
    foto_file = request.FILES.get("foto")
    candidato_id = request.POST.get("candidato_id")
    print(">> FOTO FILE:", foto_file)
    print(">> CANDIDATO ID:", candidato_id)
    if foto_file and candidato_id:
        if foto_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: FOTO")
            messages.error(request, f"❌ Archivo no válido para campo binario: FOTO")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.foto = foto_file.read()
        candidato.save()
        messages.success(request, f"Foto agregada correctamente")

def seg_aux_curp(request):
    curp_file = request.FILES.get("curp")
    candidato_id = request.POST.get("candidato_id")
    print(">> CURP FILE:", curp_file)
    print(">> CANDIDATO ID:", candidato_id)
    if curp_file and candidato_id:
        if curp_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: CURP")
            messages.error(request, f"❌ Archivo no válido para campo binario: CURP")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.curp = curp_file.read()
        candidato.save()
        messages.success(request, f"CURP agregado correctamente")

def seg_aux_portada(request):
    portada_file = request.FILES.get("portada")
    candidato_id = request.POST.get("candidato_id")
    print(">> PORTADA FILE:", portada_file)
    print(">> CANDIDATO ID:", candidato_id)
    if portada_file and candidato_id:
        if portada_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: PORTADA")
            messages.error(request, f"❌ Archivo no válido para campo binario: PORTADA")
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No existe InfoProcesoCandidato para el candidato")
            messages.error(request, f"❌ No existe InfoProcesoCandidato para el candidato")
        proceso.portada = portada_file.read()
        proceso.save()
        messages.success(request, f"Portada agregado correctamente")

def seg_aux_correo(request):
    correo = request.POST.get("correo")
    candidato_id = request.POST.get("candidato_id")
    print(">> CORREO:_", correo)
    print(">> CANDIDATO ID:", candidato_id)
    
    if correo and candidato_id:
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.correo = correo
        candidato.save()
        messages.success(request, f"Correo agregado exitosamente.")

def seg_aux_indice(request):
    indice_file = request.FILES.get("indice")
    candidato_id = request.POST.get("candidato_id")
    print(">> INDICE FILE:", indice_file)
    print(">> CANDIDATO ID:", candidato_id)
    if indice_file and candidato_id:
        if indice_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: INDICE")
            messages.error(request, f"❌ Archivo no válido para campo binario: INDICE")
        proceso, _ = models.InfoProcesoCandidato.objects.get_or_create(id_candidato_id=candidato_id)
        proceso.indice = indice_file.read()
        proceso.save()
        messages.success(request, f"Indice agregado correctamenete")

def seg_aux_carta_recepcion(request):
    file = request.FILES.get("carta_recepcion_docs")
    candidato_id = request.POST.get("candidato_id")
    if file and candidato_id:
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ Proceso no encontrado")
            messages.error(request, f"❌ Proceso no encontrado")

        if file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: carta_recepcion_docs")
            messages.error(request, f"❌ Archivo no válido para campo binario: carta_recepcion_docs")

        proceso.carta_recepcion_docs = file.read()
        proceso.save()
        messages.success(request, f"Carta Recepcion de Documentos agregada correctamente")

def seg_aux_reporte_autenticidad(request):
    file = request.FILES.get("reporte_autenticidad")
    candidato_id = request.POST.get("candidato_id")
    print(">> REPORTE AUTENTICIDAD FILE:", file)
    print(">> CANDIDATO ID:", candidato_id)

    if file and candidato_id:
        if file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: REPORTE AUTENTICIDAD")
            messages.error(request, f"❌ Archivo no válido para campo binario: REPORTE AUTENTICIDAD")

        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ Proceso no encontrado.")
            messages.error(request, f"❌ Proceso no encontrado.")
            

        proceso.reporte_autenticidad = file.read()
        proceso.save()
        messages.success(request, f"Reporte de Autenticidad agregado correctamente")

def seg_aux_triptico_derechos(request):
    triptico_file = request.FILES.get("triptico_derechos_img")
    candidato_id = request.POST.get("candidato_id")
    print(">> TRIPTICO FILE:", triptico_file)
    print(">> CANDIDATO ID:", candidato_id)

    if triptico_file and candidato_id:
        if triptico_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: TRIPTICO DERECHOS")
            messages.error(request, f"❌ Archivo no válido para campo binario: TRIPTICO DERECHOS")
        
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No existe InfoProcesoCandidato")
            messages.error(request, f"❌ No existe InfoProcesoCandidato")
        
        proceso.triptico_derechos_img = triptico_file.read()
        proceso.save()
        messages.success(request, f"Triptico de Derechos agregado correctamente")

def seg_aux_encuesta_satisfaccion(request):
    archivo = request.FILES.get("encuesta_satisfaccion")
    candidato_id = request.POST.get("candidato_id")
    print(">> ENCUESTA:", archivo)
    print(">> CANDIDATO ID:", candidato_id)

    if archivo and candidato_id:
        if archivo.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: ENCUESTA SATISFACCION")
            messages.error(request, f"❌ Archivo no válido para campo binario: ENCUESTA SATISFACCION")
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No existe InfoProcesoCandidato para el candidato")
            messages.error(request, f"❌ No existe InfoProcesoCandidato para el candidato")
        proceso.encuesta_satisfaccion = archivo.read()
        proceso.save()
        messages.success(request, f"Encuesta de Satisfacción agregada correctamente")

def seg_aux_cedula_evaluacion(request):
    archivo = request.FILES.get("cedula_evaluacion")
    candidato_id = request.POST.get("candidato_id")
    print(">> CEDULA FILE:", archivo)
    print(">> CANDIDATO ID:", candidato_id)

    if archivo and candidato_id:
        if archivo.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: CEDULA")
            messages.error(request, f"❌ Archivo no válido para campo binario: CEDULA")
        try:
            proceso = models.InfoProcesoCandidato.objects.get(id_candidato_id=candidato_id)
            proceso.cedula_evaluacion = archivo.read()
            proceso.save()
        except models.InfoProcesoCandidato.DoesNotExist:
            print("❌ No se encontró el proceso para el candidato.")
            messages.error(request, f"❌ No se encontró el proceso para el candidato.")
        messages.success(request, f"Cedula de Evaluación agregado correctamente")

@login_required
def seguimiento(request,debug=True):
    """
        https://chatgpt.com/share/68929281-4d54-800f-a451-01921c879339
    """
    
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
        
        
        return redirect("seguimiento")


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
    id_usuario = request.user.id # Obtenemos id del usuario en sesión
    id_ce = Usuario.get_id_ce__from_actual_user(id_usuario) # Obtenemos id del Centro Evaluador al que pertenece el usuario en sesión

    # Creamos record Proyecto, ligado a un Estandar de Competencia
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        id_ec = int(request.POST.get('id_ec')) # EC elegido

        if nombre and id_ec:
            # Intentar crear CeEc
            success, ceec_msg = CeEc.crear(id_ce, id_ec)

            # Crear Proyecto relacionado al CE y EC
            nuevo_proyecto = models.Proyecto(nombre=nombre, id_ce_id=id_ce, id_ec_id=id_ec)
            nuevo_proyecto.save()
            messages.success(request, 'Proyecto agregado exitosamente.')
            return redirect('proyectos')
        else:
            messages.error(request, 'Debes dar un nombre y asignar un Estandar de Competencia.')
            return redirect('proyectos')

    proyectos = models.Proyecto.objects.filter(id_ce=id_ce)
    ecs = EC.objects.all()

    return render(request, 'proyectos.html', {
        'proyectos': proyectos,
        'ecs': ecs,
        'active_section': 'proyectos'
    })

@login_required
def grupos(request, proyecto_id):
    proyecto = get_object_or_404(models.Proyecto, id=proyecto_id)

    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        if nombre:
            # avoid duplicates if user double-submits
            models.Grupo.objects.get_or_create(
                id_proyecto=proyecto,
                nombre=nombre
            )
        # PRG: redirect so refresh doesn't resubmit the POST
        return redirect('grupos', proyecto_id=proyecto.id)

    # GET
    grupos = models.Grupo.objects.filter(id_proyecto=proyecto_id)
    return render(request, "grupos.html", {
        'grupos': grupos,
        'proyecto': proyecto,
        'active_section': 'proyectos',
    })

@login_required
def candidatos(request, grupo_id):
    grupo = models.Grupo.objects.get(id=grupo_id)

    # Obtener procesos que pertenecen al grupo
    procesos = models.InfoProcesoCandidato.objects.filter(id_grupo=grupo)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ap_p = request.POST.get('apellido_paterno')
        ap_m = request.POST.get('apellido_materno')

        if nombre and ap_p and ap_m:
            nuevo_candidato = models.Candidato.objects.create(
                nombre=nombre,
                ap_paterno=ap_p,
                ap_materno=ap_m
            )

            models.InfoProcesoCandidato.objects.create(
                id_grupo=grupo,
                id_candidato=nuevo_candidato
            )

            messages.success(request, f"Candidato {nombre} agregado exitosamente.")
            return redirect('candidatos', grupo_id=grupo.id)  # Evita re-envíos en F5
        else:
            messages.error(request, "Por favor llena todos los campos.")




    # Construir la data de candidatos con su proceso
    data = []
    for proceso in procesos:
        data.append({
            "candidato": proceso.id_candidato,
            "proceso": proceso
        })

    return render(request, "candidatos.html", {
        "candidatos_info": data,
        "grupo": grupo,
        "active_section": "proyectos"
    })

@login_required
def candidato_n(request, candidato_id, debug=False):
    candidato = models.Candidato.objects.get(id=candidato_id)

    if request.method == "POST":
        if request.FILES.get("curp"):
            seg_aux_curp(request)
        elif request.FILES.get("ine"):
            seg_aux_ine(request)
        elif request.FILES.get("foto"):
            seg_aux_foto(request)
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
        


        return redirect('candidato_n', candidato_id=candidato_id)

    try:
        proceso = models.InfoProcesoCandidato.objects.get(id_candidato=candidato)
    except models.InfoProcesoCandidato.DoesNotExist:
        proceso = None

    return render(request, "candidato_n.html", {
        "candidato": candidato,
        "proceso": proceso,
        "active_section": "proyectos"
    })


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

