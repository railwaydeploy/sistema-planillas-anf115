import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator

class Empresa(models.Model):
    SK_empresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=256, null=True, blank=False, verbose_name="Nombre")
    nombre_comercial = models.CharField(max_length=256, null=True, blank=False, verbose_name="Nombre comercial")
    nit = models.CharField(max_length=256, null=True, blank=False, verbose_name="NIT de la empresa")
    act_eco = models.CharField(max_length=256, null=True, blank=False, verbose_name="Actividad economica")
    direccion = models.CharField(max_length=100, null=True, blank=False, verbose_name="Direccion")
    telefono = models.CharField(max_length=15, null=True, blank=False, verbose_name="Telefono")

    def __str__(self):
        return self.informacion
    
    class Meta:
        db_table = "empresa"

class Usuario(AbstractUser):
    SK_usuario = models.AutoField(primary_key=True)
    fecha_contratacion = models.DateField(default=timezone.now)

    def __str__(self):
        return self.SK_usuario
    
    class Meta:
        db_table = "usuario"


class Departamento(models.Model):
    SK_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=256, null=True, blank=False, verbose_name="nombre del Departamento")
    codigo = models.CharField(max_length=2, null=True, blank=False, verbose_name="codigo Departamento")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = "departamento"

# Modelo de la tabla "Municipio"
class Municipio(models.Model):
    SK_municipio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=False, verbose_name="Nombre del municipio")
    codigo = models.CharField(max_length=2, null=True, blank=False, verbose_name="codigo municipio")
    FK_departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = "municipio"


class Empleado(models.Model):
    nombre = models.CharField(max_length=256, null=True, blank=False, verbose_name="Nombres")
    apellidos = models.CharField(max_length=256, null=True, blank=False, verbose_name="Apellido")
    documento = models.CharField(max_length=256, null=True, blank=False, verbose_name="Documento")
    fk_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    direccion = models.CharField(max_length=100, null=True, blank=False, verbose_name="Direccion")
    telefono = models.CharField(max_length=15, null=True, blank=False, verbose_name="Telefono")
    cargo = models.CharField(max_length=100,null=True, blank=False, verbose_name="Ingrese cargo del empleado")
    salario_base= models.DecimalField(max_digits=10, decimal_places=4)
    FK_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    class Meta:
        db_table = "empleado"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Planilla(models.Model):
    
    SK_Planilla = models
    fecha_planilla = models.DateField((""), auto_now=False, auto_now_add=False)
    
    

    class Meta:
        db_table = "planilla"

class DetallePlanilla(models.Model):     
    SK_detallePlanilla = models.AutoField(primary_key=True)
    FK_empleado = models.ForeignKey(Empleado, on_delete=models.DO_NOTHING, null=True)
    dias_trabajados = models.CharField(max_length=10,null=True,blank=False,verbose_name="cantidad de dias trabajados")
    fecha_emision = models.DateField()
    horas_extras = models.CharField(max_length=10,null=True,blank=False,verbose_name="cantidad de horas extras")
    ISSS = models.CharField(max_length=10,null=True,blank=False,verbose_name="ISSS")
    AFP = models.CharField(max_length=10,null=True,blank=False,verbose_name="AFP")
    RENTA = models.CharField(max_length=10,null=True,blank=False,verbose_name="Renta")
    Otras_deducciones = models.CharField(max_length=10,null=True,blank=False,verbose_name="otras deducciones")
    Liquido_pagar = models.CharField(max_length=50,null=True, blank=False,verbose_name="Salario Final")
    Fk_planilla = models.ForeignKey(Planilla, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="planilla")


    class Meta:
        db_table = "detallePlanilla"


