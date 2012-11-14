#!/usr/bin/python
# -*- encoding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User	

class Intereses(models.Model):
	nombre = models.CharField(max_length=60)
	es_favorito = models.BooleanField()
	descripcion = models.CharField(max_length=60)
	
	def __unicode__(self):
		s = self.nombre + " , " + self.descripcion
		return s

class Voluntario(models.Model):
	
	correo = models.EmailField(primary_key=True)
	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	nacimiento = models.DateField()
	sexo = models.BooleanField()
	telefono = models.CharField(max_length=15, null=True, blank=True, help_text="(opcional)")
	direccion = models.CharField(max_length=70, null=True, blank=True, help_text="(opcional)")
	escolaridad = models.CharField(max_length=1)
	titulo = models.CharField(max_length=60, null = True, blank=True, help_text="(opcional)")
	user = models.OneToOneField(User)
	especialidades = models.ManyToManyField(Intereses, related_name="especialidades")
	favoritos = models.ManyToManyField(Intereses, related_name="favoritos", help_text="Elige al menos un favorito para seguir")
	puntos = models.IntegerField()
	evaluacion = models.IntegerField()
	foto = models.ImageField(upload_to='profile/volunteers/', null=True, blank=True, help_text="(Opcional)")
	pass
	#puestos = models.ManyToManyField(Puesto, through='VoluntariosAplicando')
	#foto, cv
	
class Organizacion(models.Model):
	correo = models.CharField(max_length=50, primary_key=True)
	nombre = models.CharField(max_length=70)
	descripcion = models.CharField(max_length=350)
	objetivos = models.CharField(max_length=350)
	nombre_representante = models.CharField(max_length=50)
	apellido_representante = models.CharField(max_length=50)
	telefono = models.CharField(max_length=15, null=True, blank=True, help_text="(opcional)")
	direccion = models.CharField(max_length=70, null=True, blank=True, help_text="(opcional)")
	pagina_web = models.CharField(max_length=50, null=True, blank=True, help_text="(opcional)")
	info_adicional=models.CharField(max_length=350, null=True, blank=True, help_text="(opcional)")
	linkedin = models.CharField(max_length=30, null=True, blank=True, help_text="(opcional)")
	es_empresa = models.BooleanField()
	expira = models.DateField()
	user = models.OneToOneField(User)
	especialidades = models.ManyToManyField(Intereses, related_name="especialidades_org")
	favoritos = models.ManyToManyField(Intereses, related_name="favoritos_org")
	logo = models.ImageField(upload_to='profile/orgs/', null=True, blank=True, help_text="(opcional)")
	pass
	#puestos = models.ManyToManyField(Puesto, through="EmpresasAplicando")
	#logo
	

"""	
class InteresesVoluntarios(models.Model):
	voluntario = models.ForeignKey(Voluntario)
	interes = models.ForeignKey(Intereses)
	
class InteresesOrganizaciones(models.Model):
	organizacion = models.ForeignKey(Organizacion)
	interes = models.ForeignKey(Intereses)

"""


class Proyecto(models.Model):
	descripcion = models.CharField(max_length=350)
	objetivos = models.CharField(max_length=350)
	organizacion = models.ForeignKey(Organizacion)

class Puesto(models.Model):
	proyecto = models.ForeignKey(Proyecto)
	entregables = models.CharField(max_length=350)
	escolaridad = models.CharField(max_length=1)
	costo = models.DecimalField(max_digits=7, decimal_places =2)
	descripcion = models.CharField(max_length=350)
	forma_trabajo = models.CharField(max_length=350)
	fecha_limite = models.DateField(null=True)
	especialidades = models.ManyToManyField(Intereses, related_name="especialidades_puesto")
	favoritos = models.ManyToManyField(Intereses, related_name="favoritos_puesto")

Voluntario.puestos = models.ManyToManyField(Puesto, through='VoluntariosAplicando')
Organizacion.puestos = models.ManyToManyField(Puesto, through="EmpresasAplicando")

class EmpresasAplicando(models.Model):
	empresa = models.ForeignKey(Organizacion)
	puesto = models.ForeignKey(Puesto)
	status = models.IntegerField()
	mensaje = models.CharField(max_length=300, null=True)
	

class VoluntariosAplicando(models.Model):
	voluntario = models.ForeignKey(Voluntario)
	puesto = models.ForeignKey(Puesto)
	status = models.IntegerField()
	mensaje = models.CharField(max_length=300, null=True)
	
