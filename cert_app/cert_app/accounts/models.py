from django.db import models
# Create your models here.

from django.db import connection

def query_users():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, usuario, contrasena, 
                    fecha_creacion, id_centro_evaluador 
            FROM usuario""")
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]  # List of dicts