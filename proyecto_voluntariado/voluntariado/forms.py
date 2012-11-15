#!/usr/bin/python
# -*- encoding: UTF-8 -*-

from models import *
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

Voluntario_choices = (
	('p','Primaria'),
	('b','Basicos'),
	('d','Diversificado'),
	('u','Universitario'),
	('m',u'Maestría/Doctorado'),
	('n','Ninguna')
)


class FormularioONG(forms.ModelForm):


	
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget = forms.PasswordInput)
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), help_text='Elige al menos una especialidad para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>'  )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), help_text='Elige al menos un favorito para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>')
	class Meta:
		model = Organizacion
		exclude = ('es_empresa', 'expira', 'user')
		widgets = { 'descripcion': forms.Textarea(attrs={'rows':4}), 'objetivos': forms.Textarea(attrs={'rows':4}) }


class FormularioVoluntario (forms.ModelForm):
	"""
	"""

	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget = forms.PasswordInput(attrs={'placeholder': 'Contraseña' }))
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), help_text='Elige al menos una especialidad para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>' )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}) , help_text='Elige al menos un favorito para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>')
	sexo = forms.TypedChoiceField(coerce=lambda x: True if x=='True' else False,
									choices =((False,'Femenino'), (True,'Masculino')), widget = forms.RadioSelect(attrs={'class':'radio'}))
	escolaridad = forms.ChoiceField(choices = Voluntario_choices)
	class Meta:
		model = Voluntario
		exclude = ('user','puntos', 'evaluacion')
		widgets = { 'nacimiento': SelectDateWidget(years=range(datetime.datetime.now().year-50, datetime.datetime.now().year-9)), 
					'foto': forms.FileInput(attrs={'class': 'input-file'}), }
		
class FormularioProyecto (forms.ModelForm):
	class Meta:
		model = Proyecto
		#exclude = ('organizacion')
		
class FormularioPuesto (forms.ModelForm):
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}))
	escolaridad = forms.ChoiceField(choices = Voluntario_choices)
	class Meta:
		model = Puesto
		
class FormInteres (forms.Form):
	
	nombre_i = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Nombre'}))
	es_favorito = forms.TypedChoiceField(coerce=lambda x: True if x=='True' else False,
									choices =((False,'Especialidad/Profesional'), (True,'Afición/favorito')), widget = forms.RadioSelect)
	descripcion_i = forms.CharField(widget = forms.Textarea(attrs = {'rows': 5, 'placeholder':u'Descripci\u00f3n'}))

class FormularioEditarVoluntario (forms.ModelForm):
	"""
	"""


	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), help_text='Elige al menos una especialidad para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>' )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}) , help_text='Elige al menos un favorito para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>')
	sexo = forms.TypedChoiceField(coerce=lambda x: True if x=='True' else False,
									choices =((False,'Femenino'), (True,'Masculino')), widget = forms.RadioSelect(attrs={'class':'radio'}))
	escolaridad = forms.ChoiceField(choices = Voluntario_choices)
	class Meta:
		model = Voluntario
		exclude = ('user','puntos', 'evaluacion')
		widgets = { 'nacimiento': SelectDateWidget(years=range(datetime.datetime.now().year-50, datetime.datetime.now().year-9)), 
					'foto': forms.FileInput(attrs={'class': 'input-file'}), }

class FormularioEditarONG(forms.ModelForm):
	
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), help_text='Elige al menos una especialidad para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>'  )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), help_text='Elige al menos un favorito para seguir <p><strong>¿No encuentras tus intereses? </strong><a role="button" class="btn" data-toggle="modal" href="#nuevoInteres"> Añádelos!</a></p>')
	class Meta:
		model = Organizacion
		exclude = ('es_empresa', 'expira', 'user')
		widgets = { 'descripcion': forms.Textarea(attrs={'rows':4}), 'objetivos': forms.Textarea(attrs={'rows':4}) }

class FormularioVoluntarioAplicando(forms.ModelForm):
	class Meta:
		model = VoluntariosAplicando

class FormularioEmpresaAplicando(forms.ModelForm):
	class Meta:
		model = EmpresasAplicando
