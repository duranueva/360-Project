from django.db import models

class Candidato(models.Model):
    fecha_creacion = models.DateField(blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)
    ap_paterno = models.CharField(blank=True, null=True)
    ap_materno = models.CharField(blank=True, null=True)
    correo = models.CharField(unique=True, blank=True, null=True)
    curp = models.BinaryField(blank=True, null=True)
    ine = models.BinaryField(blank=True, null=True)
    foto = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidato'