from django.db import connection, IntegrityError
from django.db.utils import DatabaseError
from django.db import models
from django.utils import timezone
from django.db import connection, DatabaseError
from django.contrib import messages

def get_all_ecs():
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM estandar_de_competencia   
            """)
            # ORDER BY fecha_creacion DESC
            
            # Get column names from cursor description
            columns = [col[0] for col in cursor.description]
            
            # Convert rows to list of dictionaries
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return True, result
            
    except Exception as e:
        return False, f"Database error: {str(e)}"

class LogoEmisorCertificados(models.Model):
    class Meta:
        db_table = 'logo_emisor_certificados'
        managed = False

    id = models.AutoField(primary_key=True)
    logo = models.BinaryField()

class CentroEvaluador(models.Model):
    class Meta:
        db_table = 'centro_evaluador'
        managed = False

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    logo_centro_evaluador = models.BinaryField(null=True)
    triptico_derechos_img = models.BinaryField(null=True)
    
    # Foreign key to LogoEmisorCertificados
    id_logo_emisor_cert = models.ForeignKey(
        'LogoEmisorCertificados',
        on_delete=models.DO_NOTHING,
        db_column='id_logo_emisor_cert',
        null=True
    )


def get_ecs_by_id_ce(id_ce):
    """
    Returns all ECs (Estandares de Competencia) by the CE's id (Centro Evaluador)
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EC.*
                FROM estandar_de_competencia AS EC
                JOIN ce_ec ON EC.id = ce_ec.id_ec
                WHERE ce_ec.id_ce = %s
            """, [id_ce])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return True, [dict(zip(columns, row)) for row in rows]
    except DatabaseError as e:
        return False, f"Error en la búsqueda de ECs con el id_ce dado: {str(e)}"


class EstandarCompetencia:
    @staticmethod
    def crear(nombre, codigo, id_examen_diagnostico, id_usuario_creador):
        """
        Creates a new competency standard in the database
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO estandar_de_competencia 
                    (nombre, codigo, id_examen_diagnostico, id_usuario_creador, fecha_creacion)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                """, [nombre, codigo, id_examen_diagnostico, id_usuario_creador])
            
            return True, "El estándar de competencia se ha agregado correctamente."
            
        except DatabaseError as e:
            return False, f"Error al agregar el estándar: {str(e)}"
        
    @staticmethod
    def obtener_todos():
        """
        Gets all competency standards from database
        
        Returns:
            list: List of dictionaries representing all standards
            OR
            tuple: (False, error_message) if error occurs
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nombre, codigo, id_examen_diagnostico, 
                        fecha_creacion, id_usuario_creador 
                    FROM estandar_de_competencia
                """)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
            
            return [dict(zip(columns, row)) for row in rows]
        
        except DatabaseError as e:
            # Return tuple (success=False, error_message) for consistency with crear()
            return False, f"Error al obtener los estándares: {str(e)}"



class Candidato(models.Model):
    fecha_creacion = models.DateField(auto_now_add=False, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    ap_paterno = models.CharField(max_length=255, blank=True, null=True)
    ap_materno = models.CharField(max_length=255, blank=True, null=True)
    correo = models.EmailField(unique=True)
    curp = models.CharField(max_length=255, blank=True, null=True)
    foto = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidato'

class InfoProcesoCandidato(models.Model):
    #id_candidato = models.ForeignKey('Candidato', on_delete=models.CASCADE, db_column='id_candidato')
    id_candidato = models.IntegerField(blank=True, null=True)
    id_grupo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    portada = models.BinaryField(blank=True, null=True)
    indice = models.BinaryField(blank=True, null=True)
    carta_recepcion_docs = models.BinaryField(blank=True, null=True)
    fecha_registro_generado = models.DateField(blank=True, null=True)
    reporte_autenticidad = models.BinaryField(blank=True, null=True)
    triptico_derechos_img = models.BinaryField(blank=True, null=True)
    plan_evaluacion = models.BinaryField(blank=True, null=True)
    encuesta_satisfaccion = models.BinaryField(blank=True, null=True)
    instrumento_evaluacion = models.BinaryField(blank=True, null=True)
    cedula_evaluacion = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'info_proceso_candidato'

class CeEc(models.Model):
    id_ce = models.IntegerField(blank=True, null=True)
    id_ec = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Since you're managing the table outside Django
        db_table = 'ce_ec'
        unique_together = (('id_ce', 'id_ec'),)  # This represents the composite primary key

    def __str__(self):
        return f"CE-EC Relation: {self.id_ce} - {self.id_ec}"


    @staticmethod
    def crear(id_ce, id_ec):
        """
        Creates a new CE-EC relationship in the database if it doesn't already exist.
        
        Args:
            id_ce: ID of the evaluation center
            id_ec: ID of the competency standard
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ce_ec (id_ce, id_ec)
                    VALUES (%s, %s)
                """, [id_ce, id_ec])
            
            return True, "The CE-EC relationship was added successfully."

        except IntegrityError:
            return False, "The CE-EC relationship already exists."

        except DatabaseError as e:
            return False, f"Error adding the relationship: {str(e)}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EC(models.Model):
    """Model representing the existing Estandar_de_competencia table"""
    nombre = models.TextField(verbose_name="Nombre del estándar")
    codigo = models.TextField(verbose_name="Código del estándar")
    id_examen_diagnostico = models.IntegerField(verbose_name="ID Examen Diagnóstico")
    fecha_creacion = models.DateField(
        verbose_name="Fecha de creación",
        auto_now_add=True
    )
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Usuario creador",
        related_name="estandares_creados",
        db_column='id_usuario_creador'  # Explicitly map to your column name
    )
    
    class Meta:
        db_table = 'estandar_de_competencia'
        verbose_name = "Estándar de Competencia"
        verbose_name_plural = "Estándares de Competencia"
        managed = False  # This tells Django not to manage the table's lifecycle
        
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
    @classmethod
    def buscar_estandar(cls, nombre=None, codigo=None, id_examen_diagnostico=None, usuario_creador=None):
        """
        Finds an Estandar de Competencia by one or more of the following criteria:
        - nombre (case-insensitive partial match)
        - codigo (case-insensitive exact match)
        - id_examen_diagnostico (exact match)
        - usuario_creador (exact match)
        
        Returns a queryset of matching records
        """
        filters = {}
        
        if nombre:
            filters['nombre__icontains'] = nombre
        if codigo:
            filters['codigo__iexact'] = codigo
        if id_examen_diagnostico:
            filters['id_examen_diagnostico'] = id_examen_diagnostico
        if usuario_creador:
            filters['usuario_creador'] = usuario_creador
            
        return cls.objects.filter(**filters)

class Usuario(models.Model):
    """Model representing the existing usuario table"""
    usuario = models.CharField(max_length=255, unique=True, verbose_name="Nombre de usuario")
    contrasena = models.CharField(max_length=255, verbose_name="Contraseña")
    fecha_creacion = models.DateField(
        verbose_name="Fecha de creación",
        auto_now_add=True
    )
    id_centro_evaluador = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="ID Centro Evaluador"
    )
    
    class Meta:
        db_table = 'usuario'
        managed = False  # Since it's an existing table
        
    def __str__(self):
        return self.usuario
    
    @classmethod
    def obtener_por_id(cls, usuario_id):
        """Retrieves a user by ID"""
        try:
            return cls.objects.get(id=usuario_id)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def obtener_id_centro_evaluador(cls, usuario_id):
        """Gets the id_centro_evaluador for a given user"""
        try:
            usuario = cls.objects.get(id=usuario_id)
            return usuario.id_centro_evaluador
        except cls.DoesNotExist:
            return None
    
    @staticmethod
    def get_id_ce__from_actual_user(id_usuario):
        usuario = Usuario.objects.get(id=id_usuario)
        return usuario.id_centro_evaluador
