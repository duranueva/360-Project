from django.db import models, connection


class Candidato(models.Model):
    fecha_creacion = models.DateField(blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)
    ap_paterno = models.CharField(blank=True, null=True)
    ap_materno = models.CharField(blank=True, null=True)
    correo = models.CharField(unique=True, blank=True, null=True)
    curp = models.BinaryField(blank=True, null=True)
    ine = models.BinaryField(blank=True, null=True)
    foto = models.BinaryField(blank=True, null=True)

    def __str__(self):
        fields = [
            f"fecha_creacion: {self.fecha_creacion or 'null'}",
            f"nombre: {self.nombre or 'null'}",
            f"ap_paterno: {self.ap_paterno or 'null'}",
            f"ap_materno: {self.ap_materno or 'null'}",
            f"correo: {self.correo or 'null'}",
            f"curp: {self.curp.hex() if self.curp else 'null'}",
            f"ine: {self.ine.hex() if self.ine else 'null'}",
            f"foto: {self.foto.hex() if self.foto else 'null'}",
        ]
        return " | ".join(fields)
    
    class Meta:
        managed = False
        db_table = 'candidato'

def query_all_table__candidato():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * 
            FROM candidato""")
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]  # List of dicts