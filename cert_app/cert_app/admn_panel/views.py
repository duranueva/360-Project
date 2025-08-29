from django.shortcuts import render, redirect
from . import models
from django.db import connection, DatabaseError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import base64



@login_required
def test_1(request):
    return render(request,"test_ad_1.html")

@login_required
def base_ad(request):
    return render(request,"base_ad.html")

@login_required
def control(request):
    return render(request,"control.html")

from accounts.models import query_users
@login_required
def usuarios(request):
    users = query_users()
    return render(request,"usuarios.html",{'users': users})

'''
# Este solo muestra los ECs del Cent Eval al que perteneces
@login_required
def estandares(request):
    """
        Función que solo muestra los Estandares de Competencia 
        de el Centro Evaluador al que pertenece el usuario en sesión.

        Se tiene un botón 'Agregar EC' que muestra un formulario para
        agregar dicho fila a la tabla 'estandar_de_competencia'. 
        
        Además, se hace una incersión a 'ce_ec', que modela la conexión 
        de un Estandar de Competencia con su Centro Evaluador.
    """
    #Variables que utilizaremos en distintas fases de la función
    id_usuario_creador = request.session.get('usuario_id')
    id_ce = models.Usuario.obtener_id_centro_evaluador(id_usuario_creador)

    # Manejo del formulario (POST) para incersión en BD
    if request.method == 'POST' and 'save' in request.POST:
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        id_examen_diagnostico = request.POST.get('id_examen_diagnostico')
        
        #Guardando Estandar de Competencia
        success, message = models.EstandarCompetencia.crear(
            nombre, codigo, id_examen_diagnostico, id_usuario_creador
        )

        if success:
            ec = models.EC.buscar_estandar(
                nombre=nombre,
                codigo=codigo,
                id_examen_diagnostico=id_examen_diagnostico,
                usuario_creador=id_usuario_creador
            ).first()

            if ec:
                if id_ce:
                    id_ec = ec.id
                    ce_ec_success, ce_ec_message = models.CeEc.crear(id_ce, id_ec)
                    if ce_ec_success:
                        messages.success(request, "EC and CE-EC relationship created successfully")
                    else:
                        messages.error(request, f"EC created but CE-EC relationship failed: {ce_ec_message}")
                else:
                    messages.error(request, "EC created but no Centro Evaluador found for this user")
            else:
                messages.error(request, "EC created but could not be found afterwards")
            
            return redirect('estandares')
        else:
            messages.error(request, message)
            return redirect(f"{request.path}?show_form=1")

    # Manejo del GET para mostrar formulario
    show_form = request.GET.get('show_form') == '1'

    # Tomando los Estandar de Competencia
    try:
        success, result = models.get_ecs_by_id_ce(id_ce)
        if not success:
            messages.error(request, result)
            ecs = []
        else:
            ecs = result  # Lista de diccionarios
    except Exception as e:
        messages.error(request, f"Error retrieving standards: {str(e)}")
        ecs = []

    return render(request, "estandares.html", {
        'ecs': ecs,
        'show_form': show_form
    })
'''

@login_required
def estandares(request):
    """
        Función que muestra todos los estandares de competencia.

        Además, permite agregarlos. Con el usuario en cuestión.
    """
    #Variables que utilizaremos en distintas fases de la función
    id_usuario_creador = request.session.get('usuario_id')
    id_ce = models.Usuario.obtener_id_centro_evaluador(id_usuario_creador)

    # Manejo del formulario (POST) para incersión en BD
    if request.method == 'POST' and 'save' in request.POST:
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        id_examen_diagnostico = request.POST.get('id_examen_diagnostico')
        
        #Guardando Estandar de Competencia
        success, message = models.EstandarCompetencia.crear(
            nombre, codigo, id_examen_diagnostico, id_usuario_creador
        )

        if success:
            ec = models.EC.buscar_estandar(
                nombre=nombre,
                codigo=codigo,
                id_examen_diagnostico=id_examen_diagnostico,
                usuario_creador=id_usuario_creador
            ).first()

            if ec:
                if id_ce:
                    id_ec = ec.id
                    ce_ec_success, ce_ec_message = models.CeEc.crear(id_ce, id_ec)
                    if ce_ec_success:
                        messages.success(request, "EC and CE-EC relationship created successfully")
                    else:
                        messages.error(request, f"EC created but CE-EC relationship failed: {ce_ec_message}")
                else:
                    messages.error(request, "EC created but no Centro Evaluador found for this user")
            else:
                messages.error(request, "EC created but could not be found afterwards")
            
            return redirect('estandares')
        else:
            messages.error(request, message)
            return redirect(f"{request.path}?show_form=1")

    # Manejo del GET para mostrar formulario
    show_form = request.GET.get('show_form') == '1'

    # Tomando los Estandar de Competencia
    try:
        success, result = models.get_all_ecs()
        if not success:
            messages.error(request, result)
            ecs = []
        else:
            ecs = result  # Lista de diccionarios
    except Exception as e:
        messages.error(request, f"Error retrieving standards: {str(e)}")
        ecs = []

    return render(request, "estandares.html", {
        'ecs': ecs,
        'show_form': show_form
    })







'''
# Funcion que agrega  triptico, logotipo_ce, logo_emis_certf
@login_required
def formularios(request):
    id_usuario_creador = request.session.get('usuario_id')
    centro_id = models.Usuario.obtener_id_centro_evaluador(id_usuario_creador)

    show_form = request.GET.get("show_form") == "1"

    triptico_img = None
    logotipo_ce_img = None
    logo_emis_certf_img = None

    try:
        centro = models.CentroEvaluador.objects.get(id=centro_id)

        # Load existing images from the database and encode to base64
        if centro.triptico_derechos_img:
            triptico_img = base64.b64encode(centro.triptico_derechos_img).decode('utf-8')

        if centro.logo_centro_evaluador:
            logotipo_ce_img = base64.b64encode(centro.logo_centro_evaluador).decode('utf-8')

        if centro.id_logo_emisor_cert and centro.id_logo_emisor_cert.logo:
            logo_emis_certf_img = base64.b64encode(centro.id_logo_emisor_cert.logo).decode('utf-8')

        if request.method == "POST":
            try:
                triptico_file = request.FILES.get('triptico')
                logotipo_ce_file = request.FILES.get('logotipo_ce')
                logo_emis_certf_file = request.FILES.get('logo_emis_certf')

                if not triptico_file and not logotipo_ce_file and not logo_emis_certf_file:
                    messages.error(request, "Debes subir al menos un archivo.")
                    return redirect("formularios")

                if triptico_file:
                    centro.triptico_derechos_img = triptico_file.read()

                if logotipo_ce_file:
                    centro.logo_centro_evaluador = logotipo_ce_file.read()

                if logo_emis_certf_file:
                    logo_bytes = logo_emis_certf_file.read()
                    new_logo = models.LogoEmisorCertificados.objects.create(logo=logo_bytes)
                    centro.id_logo_emisor_cert = new_logo

                centro.save()
                messages.success(request, "Documento(s) actualizado(s) correctamente.")
                return redirect("formularios")

            except Exception as e:
                messages.error(request, f"Error al guardar documentos: {str(e)}")

    except models.CentroEvaluador.DoesNotExist:
        messages.error(request, "Centro Evaluador no encontrado.")
    except Exception as e:
        messages.error(request, f"Error al cargar los documentos: {str(e)}")

    return render(request, "formularios.html", {
        "show_form": show_form,
        "triptico_img": triptico_img,
        "logotipo_ce_img": logotipo_ce_img,
        "logo_emis_certf_img": logo_emis_certf_img,
    })
'''

# Función que agrega triptico, logo_emis_certf
@login_required
def formularios(request):
    id_usuario_creador = request.session.get('usuario_id')
    centro_id = models.Usuario.obtener_id_centro_evaluador(id_usuario_creador)

    show_form = request.GET.get("show_form") == "1"

    triptico_img = None
    #logotipo_ce_img = None
    logo_emis_certf_img = None

    try:
        centro = models.CentroEvaluador.objects.get(id=centro_id)

        # Load existing images from the database and encode to base64
        if centro.triptico_derechos_img:
            triptico_img = base64.b64encode(centro.triptico_derechos_img).decode('utf-8')

        """if centro.logo_centro_evaluador:
            logotipo_ce_img = base64.b64encode(centro.logo_centro_evaluador).decode('utf-8')"""

        if centro.id_logo_emisor_cert and centro.id_logo_emisor_cert.logo:
            logo_emis_certf_img = base64.b64encode(centro.id_logo_emisor_cert.logo).decode('utf-8')

        if request.method == "POST":
            try:
                triptico_file = request.FILES.get('triptico')
                #logotipo_ce_file = request.FILES.get('logotipo_ce')
                logo_emis_certf_file = request.FILES.get('logo_emis_certf')

                if not triptico_file and not logo_emis_certf_file:
                    messages.error(request, "Debes subir al menos un archivo.")
                    return redirect("formularios")

                if triptico_file:
                    centro.triptico_derechos_img = triptico_file.read()

                """if logotipo_ce_file:
                    centro.logo_centro_evaluador = logotipo_ce_file.read()"""

                if logo_emis_certf_file:
                    logo_bytes = logo_emis_certf_file.read()
                    new_logo = models.LogoEmisorCertificados.objects.create(logo=logo_bytes)
                    centro.id_logo_emisor_cert = new_logo

                centro.save()
                messages.success(request, "Documento(s) actualizado(s) correctamente.")
                return redirect("formularios")

            except Exception as e:
                messages.error(request, f"Error al guardar documentos: {str(e)}")

    except models.CentroEvaluador.DoesNotExist:
        messages.error(request, "Centro Evaluador no encontrado.")
    except Exception as e:
        messages.error(request, f"Error al cargar los documentos: {str(e)}")

    return render(request, "formularios.html", {
        "show_form": show_form,
        "triptico_img": triptico_img,
        #"logotipo_ce_img": logotipo_ce_img,
        "logo_emis_certf_img": logo_emis_certf_img,
    })

