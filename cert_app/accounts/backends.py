from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth.hashers import check_password

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, contrasena FROM Usuario WHERE usuario = %s", [username])
                result = cursor.fetchone()

            if result:
                user_id, hashed_password = result
                if check_password(password, hashed_password):
                    user, _ = User.objects.get_or_create(username=username)
                    return user
        except Exception as e:
            print(f"[ERROR] custom auth failed: {e}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
