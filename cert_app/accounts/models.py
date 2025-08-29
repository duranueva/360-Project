'''from django.db import models
from django.db import connection
import bcrypt
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_centro_evaluador = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

def query_users():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, usuario, contrasena, 
                    fecha_creacion, id_centro_evaluador 
            FROM usuario""")
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]  # List of dicts

class Usuario:
    @staticmethod
    def log_in_validation(usuario, contrasena):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, contrasena FROM Usuario WHERE usuario = %s
                """, [usuario])
                user = cursor.fetchone()

            if user:
                user_id, hashed_password = user
                if bcrypt.checkpw(contrasena.encode(), hashed_password.encode()):
                    return user_id  # simpler return (not as a tuple)
            return None

        except Exception as e:
            print(f"[ERROR] log_in_validation failed: {e}")
            return None

    @staticmethod
    def signup(usuario, contrasena, id_centro_evaluador=None):
        try:
            hashed = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Usuario (usuario, contrasena, id_centro_evaluador)
                    VALUES (%s, %s, %s)
                """, [usuario, hashed, id_centro_evaluador])
            return True
        except Exception as e:
            print("Signup error:", e)
            return False
    
    @staticmethod
    def crea(usuario, contrasena, id_centro_evaluador=None):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Usuario (usuario, contrasena, id_centro_evaluador)
                    VALUES (%s, %s, %s)
                """, [usuario, contrasena, id_centro_evaluador])
            return True
        except Exception as e:
            print("Signup error:", e)
            return False
'''

from django.db import models, connection
import bcrypt
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_centro_evaluador = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

def query_users():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, usuario, contrasena, 
                    fecha_creacion, id_centro_evaluador 
            FROM usuario""")
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]  # List of dicts

class Usuario:
    @staticmethod
    def log_in_validation(usuario, contrasena):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, contrasena FROM Usuario WHERE usuario = %s
                """, [usuario])
                user = cursor.fetchone()

            if user:
                user_id, hashed_password = user
                if bcrypt.checkpw(contrasena.encode(), hashed_password.encode()):
                    return user_id
            return None

        except Exception as e:
            print(f"[ERROR] log_in_validation failed: {e}")
            return None

    @staticmethod
    def signup(usuario, contrasena, id_centro_evaluador=None):
        try:
            hashed = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Usuario (usuario, contrasena, id_centro_evaluador)
                    VALUES (%s, %s, %s)
                """, [usuario, hashed, id_centro_evaluador])
            return True
        except Exception as e:
            print("Signup error:", e)
            return False

    @staticmethod
    def get_usuario_by_username(username):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, usuario, id_centro_evaluador, fecha_creacion
                FROM Usuario WHERE usuario = %s
            """, [username])
            return cursor.fetchone()
