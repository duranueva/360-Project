from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # para mostrar mensajes opcionales
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from . import models
from admn_panel.models import Usuario, EC, CeEc  # importa el modelo desde la app correspondiente

# Create your views here.
@login_required
def base_doc(request):
    return render(request,"base_doc.html")


"""
    Sección Seguimiento
"""
def seg_aux_ine_frente(request):
    ine_file = request.FILES.get("ine_frente")
    candidato_id = request.POST.get("candidato_id")
    print(">> INE FILE:", ine_file)
    print(">> CANDIDATO ID:", candidato_id)
    if ine_file and candidato_id:
        if ine_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: INE")
            messages.error(request, f"❌ Archivo no válido para campo binario: INE")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.ine_frente = ine_file.read()
        candidato.save()
        messages.success(request, f"INE (Frente) agregado correctamente")

def seg_aux_ine_reverso(request):
    ine_file = request.FILES.get("ine_reverso")
    candidato_id = request.POST.get("candidato_id")
    print(">> INE FILE:___  ", ine_file)
    print(">> CANDIDATO ID:____  ", type(candidato_id), "|",candidato_id,"|")
    if ine_file and candidato_id:
        if ine_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: INE")
            messages.error(request, f"❌ Archivo no válido para campo binario: INE")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.ine_reverso = ine_file.read()
        candidato.save()
        messages.success(request, f"INE (Reverso) agregado correctamente")

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
        try:
            candidato = models.Candidato.objects.get(id=candidato_id)
            candidato.correo = correo
            candidato.save()
            messages.success(request, "Correo agregado exitosamente.")
        
        except IntegrityError:
            messages.error(request, "El correo que ingresas ya está registrado. Intenta con otro.")

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

def seg_aux_firma(request):
    firma_file = request.FILES.get("firma")
    candidato_id = request.POST.get("candidato_id")
    print(">> FIRMA FILE:", firma_file)
    print(">> CANDIDATO ID:", candidato_id)
    if firma_file and candidato_id:
        if firma_file.content_type.startswith("text"):
            print("❌ Archivo no válido para campo binario: FIRMA")
            messages.error(request, "❌ Archivo no válido para campo binario: FIRMA")
        candidato = models.Candidato.objects.get(id=candidato_id)
        candidato.firma = firma_file.read()
        candidato.save()
        messages.success(request, "Firma agregada correctamente")

"""
@login_required
def seguimiento(request,debug=True):
    
    # ---- Acciones de carga de archivos / correo (POST) ----
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

    # Obtenemos el Centro Evaluador actual
    id_usuario = request.user.id
    id_ce = Usuario.get_id_ce__from_actual_user(id_usuario)

    # Obtener proyectos del Centro Evaluador
    proyectos = models.Proyecto.objects.filter(id_ce=id_ce)

    # Obtener grupos relacionados a los proyectos
    grupos = models.Grupo.objects.filter(id_proyecto__in=proyectos)

    # Obtener procesos que pertenezcan a esos grupos
    procesos = models.InfoProcesoCandidato.objects.filter(id_grupo__in=grupos)

    # Obtener candidatos cuyos procesos están en los grupos anteriores
    data = []
    for proceso in procesos:
        data.append({
            "candidato": proceso.id_candidato,
            "proceso": proceso
        })

    return render(request, "seguimiento.html", {"candidatos_info": data})

"""


@login_required
def seguimiento(request, debug=True):
    # ---- Acciones de carga de archivos / correo (POST) ----
    if request.method == "POST":
        if request.FILES.get("ine_frente"):
            seg_aux_ine_frente(request)
        elif request.FILES.get("ine_reverso"):
            seg_aux_ine_reverso(request)
        elif request.FILES.get("foto"):
            seg_aux_foto(request)
        elif request.FILES.get("firma"):
            seg_aux_firma(request)
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

    # ---- Parámetros de filtro (GET) ----
    ec_id = request.GET.get("ec")            # id de EC
    proyecto_id = request.GET.get("proyecto")
    grupo_id = request.GET.get("grupo")
    candidato_id = request.GET.get("candidato")

    # ---- Ámbito del usuario (CE actual) ----
    id_usuario = request.user.id
    id_ce = Usuario.get_id_ce__from_actual_user(id_usuario)

    # ---- Base: Proyectos del CE ----
    proyectos_qs = models.Proyecto.objects.filter(id_ce=id_ce)

    # EC disponibles (derivados de los proyectos del CE)
    ecs_qs = EC.objects.filter(
        pk__in=proyectos_qs.values_list("id_ec_id", flat=True)
    ).order_by("nombre").distinct()

    # Filtrar por EC si viene seleccionado
    if ec_id:
        proyectos_qs = proyectos_qs.filter(id_ec_id=ec_id)

    # Grupos disponibles (derivados de los proyectos filtrados)
    grupos_qs = models.Grupo.objects.filter(
        id_proyecto__in=proyectos_qs.values_list("id", flat=True)
    ).order_by("nombre")

    # Filtrar por Proyecto si viene seleccionado
    if proyecto_id:
        grupos_qs = grupos_qs.filter(id_proyecto_id=proyecto_id)

    # Procesos base (derivados de los grupos filtrados)
    procesos_qs = models.InfoProcesoCandidato.objects.filter(
        id_grupo__in=grupos_qs.values_list("id", flat=True)
    ).select_related("id_candidato", "id_grupo")

    # Filtros de Grupo y Candidato
    if grupo_id:
        procesos_qs = procesos_qs.filter(id_grupo_id=grupo_id)
    if candidato_id:
        procesos_qs = procesos_qs.filter(id_candidato_id=candidato_id)

    # Candidatos disponibles (derivados de los procesos filtrados)
    candidatos_qs = models.Candidato.objects.filter(
        id__in=procesos_qs.values_list("id_candidato_id", flat=True)
    ).order_by("ap_paterno", "ap_materno", "nombre").distinct()

    # Data final para render
    data = [
        {"candidato": p.id_candidato, "proceso": p}
        for p in procesos_qs
    ]

    context = {
        "candidatos_info": data,

        # para llenar selects
        "ecs": ecs_qs,
        "proyectos": proyectos_qs.order_by("nombre"),
        "grupos": grupos_qs,
        "candidatos": candidatos_qs,

        # seleccionados (para marcar 'selected' en template)
        "selected": {
            "ec": str(ec_id) if ec_id else "",
            "proyecto": str(proyecto_id) if proyecto_id else "",
            "grupo": str(grupo_id) if grupo_id else "",
            "candidato": str(candidato_id) if candidato_id else "",
        },
    }
    return render(request, "seguimiento.html", context)



"""
    Sección Proyectos
"""
@login_required
def proyectos(request):
    id_usuario = request.user.id  # Usuario en sesión
    id_ce = Usuario.get_id_ce__from_actual_user(id_usuario)  # Centro Evaluador

    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        id_ec = request.POST.get('id_ec')

        if nombre and id_ec:
            try:
                id_ec = int(id_ec)
            except ValueError:
                messages.error(request, 'ID de Estandar de Competencia inválido.')
                return redirect('proyectos')

            created, message = CeEc.crear(id_ce=id_ce,id_ec=id_ec)
            print(message)

            # Verificar si ya existe el proyecto
            proyecto, creado = models.Proyecto.objects.get_or_create(
                nombre=nombre,
                id_ce_id=id_ce,
                id_ec_id=id_ec
            )

            if creado:
                messages.success(request, 'Proyecto agregado exitosamente.')
            else:
                messages.error(request, '❌ El nombre asignado para el Proyecto ya existe con ese Estandar de Competencia. Escoge uno diferente.')

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
            grupo, created = models.Grupo.objects.get_or_create(
                id_proyecto=proyecto,
                nombre=nombre
            )
            if created:
                messages.success(request, "Grupo agregado correctamente")
            else:
                messages.error(request, "❌ El grupo ya existe en este proyecto")
        else:
            messages.error(request, "❌ El nombre no puede estar vacío")
        
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

            messages.success(request, f"Candidato '{nombre} {ap_p} {ap_m}' agregado exitosamente.")
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


"""
@login_required
def candidatos(request, grupo_id):
    grupo = models.Grupo.objects.get(id=grupo_id)

    # Obtener procesos que pertenecen al grupo
    procesos = models.InfoProcesoCandidato.objects.filter(id_grupo=grupo)

    if request.method == 'POST':
        nombre  = (request.POST.get('nombre') or '').strip()
        ap_p    = (request.POST.get('apellido_paterno') or '').strip()
        ap_m    = (request.POST.get('apellido_materno') or '').strip()

        if not (nombre and ap_p and ap_m):
            messages.error(request, "Por favor llena todos los campos.")
            return redirect('candidatos', grupo_id=grupo.id)
        else:
            candidato = models.Candidato.objects.filter(
                nombre__iexact=nombre,
                ap_paterno__iexact=ap_p,
                ap_materno__iexact=ap_m
            ).first()

            if candidato:
                # ¿Ya está ligado este candidato al grupo?
                ya_asignado = models.InfoProcesoCandidato.objects.filter(
                    id_grupo=grupo,
                    id_candidato=candidato
                ).exists()

                
                print("************")
                print("************")
                print("************")
                print("************")
                print(candidato)
                print(ya_asignado)
                print("************")
                print("************")
                print("************")
                print("************")

                if ya_asignado:
                    messages.error(request, f"❌ El candidato {nombre} {ap_p} {ap_m} ya está en este grupo.")
                    return redirect('candidatos', grupo_id=grupo.id)
            
            # Si no existe el candidato ligado al Grupo, lo creamos
            nuevo_candidato = models.Candidato.objects.create(
                nombre=nombre,
                ap_paterno=ap_p,
                ap_materno=ap_m
            )
            models.InfoProcesoCandidato.objects.create(
                id_grupo=grupo,
                id_candidato=nuevo_candidato
            )
            messages.success(request, f"Candidato '{nombre} {ap_p} {ap_m}' agregado exitosamente.")
            return redirect('candidatos', grupo_id=grupo.id)

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

"""


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