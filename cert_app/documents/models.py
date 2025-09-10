from django.db import models, connection
from django.utils import timezone



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
        def safe_hex(val):
            return val.hex() if isinstance(val, (bytes, bytearray)) else 'invalid'

        fields = [
            f"id: {self.id or 'null'}",
            f"fecha_creacion: {self.fecha_creacion or 'null'}",
            f"nombre: {self.nombre or 'null'}",
            f"ap_paterno: {self.ap_paterno or 'null'}",
            f"ap_materno: {self.ap_materno or 'null'}",
            f"correo: {self.correo or 'null'}",
            f"curp: {safe_hex(self.curp) if self.curp else 'null'}",
            f"ine: {safe_hex(self.ine) if self.ine else 'null'}",
            f"foto: {safe_hex(self.foto) if self.foto else 'null'}",
        ]
        return " | ".join(fields)
    
    class Meta:
        managed = False
        db_table = 'candidato'

class InfoProcesoCandidato(models.Model):
    id_candidato = models.ForeignKey(
        'Candidato',
        on_delete=models.CASCADE,
        db_column='id_candidato'
    )
    id_grupo = models.ForeignKey(
        'Grupo',
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_grupo'
    )
    fecha_creacion = models.DateField(blank=True, null=True, default=timezone.now)
    portada = models.BinaryField(blank=True, null=True)
    indice = models.BinaryField(blank=True, null=True)
    carta_recepcion_docs = models.BinaryField(blank=True, null=True)
    #ficha_registro_generado = models.BinaryField(blank=True, null=True)
    reporte_autenticidad = models.BinaryField(blank=True, null=True)
    triptico_derechos_img = models.BinaryField(blank=True, null=True)
    encuesta_satisfaccion = models.BinaryField(blank=True, null=True)
    cedula_evaluacion = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return f"Proceso de {self.id_candidato_id} en grupo {self.id_grupo_id or 'null'}"

    class Meta:
        managed = False
        db_table = 'info_proceso_candidato'

class Grupo(models.Model):
    # define aquí los campos de tu tabla Grupo
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'grupo'

def query_all_table__candidato():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * 
            FROM candidato""")
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]  # List of dicts

def insert_file_to_bytea__candidato(candidato_id, file_path):
    #path = r"C:\Users\costo\Downloads\test.jpg"
    """
        Para insertar un dato:
            
            id = 1
            models.insert_file_to_bytea__candidato(id, path)
    """
    with open(file_path, 'rb') as f:
        binary_data = f.read()

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE candidato
            SET ine = %s, foto = %s
            WHERE id = %s
        """, [binary_data, binary_data, candidato_id])

def insert_file_to_bytea__proceso(proceso_id, file_path):
    with open(file_path, 'rb') as f:
        binary_data = f.read()

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE info_proceso_candidato
            SET portada = %s, indice = %s
            WHERE id = %s
        """, [binary_data, binary_data, candidato_id])