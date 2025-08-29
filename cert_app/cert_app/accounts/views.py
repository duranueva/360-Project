"""from . import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile  # if you're storing id_centro_evaluador
from django.contrib.auth.decorators import login_required"""



from . import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db import transaction, IntegrityError




def start(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "register":
            usuario = request.POST.get("usuario")
            contrasena = request.POST.get("contrasena")
            id_centro_evaluador = request.POST.get("id_centro_evaluador")  # Remove the 'or None' part

            # First validate that id_centro_evaluador is provided
            if not id_centro_evaluador:
                messages.error(request, "Debe proporcionar un ID de centro evaluador válido.")
                return render(request, "base_start.html")

            try:
                # Usamos una transacción atómica
                with transaction.atomic():
                    # 1. Create Django user for login/session
                    user = User.objects.create_user(username=usuario, password=contrasena)

                    # 2. Save to custom Usuario table (with bcrypt)
                    models.Usuario.signup(usuario, contrasena, id_centro_evaluador)

                    # 3. Optional: link id_centro_evaluador to Django user
                    UserProfile.objects.create(user=user, id_centro_evaluador=id_centro_evaluador)

                messages.success(request, "Usuario registrado correctamente.")
            except IntegrityError:
                messages.error(request, "El usuario ya existe.")
            except Exception as e:
                print("Signup error:", e)
                messages.error(request, "Error al registrar el usuario.")

        elif action == "login":
            usuario = request.POST.get("usuario")
            contrasena = request.POST.get("contrasena")
            user = authenticate(request, username=usuario, password=contrasena)

            if user is not None:
                login(request, user)

                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM usuario WHERE usuario = %s", [usuario])
                    result = cursor.fetchone()
                    if result:
                        request.session['usuario_id'] = result[0]
                        print("USUARIO ID saved in session:", request.session['usuario_id'])
                        print(request.session.get('usuario_id'))

                messages.success(request, "Inicio de sesión exitoso.")
                return redirect('estandares')
            else:
                messages.error(request, "Credenciales inválidas.")

    return render(request, "base_start.html")

def custom_logout(request):
    logout(request)
    return redirect('start')






def home(request):
    users = models.query_users()
    return render(request,"home.html",{'users': users})

def home2(request):
    users = models.query_users()
    return render(request,"home2.html",{'users': users})
