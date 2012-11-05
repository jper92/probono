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
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False).order_by('nombre'), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}))
	class Meta:
		model = Organizacion
		exclude = ('es_empresa', 'expira', 'user')
		widgets = { 'descripcion': forms.Textarea(attrs={'rows':4}), 'objetivos': forms.Textarea(attrs={'rows':4}) }


class FormularioVoluntario (forms.ModelForm):
	"""
	"""
	
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget = forms.PasswordInput)
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}), )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}))
	sexo = forms.TypedChoiceField(coerce=lambda x: True if x=='True' else False,
									choices =((False,'Femenino'), (True,'Masculino')), widget = forms.RadioSelect)
	escolaridad = forms.ChoiceField(choices = Voluntario_choices)
	class Meta:
		model = Voluntario
		exclude = ('user')
		widgets = { 'nacimiento': SelectDateWidget(years=range(datetime.datetime.now().year-50, datetime.datetime.now().year-9)), }
		
class FormularioProyecto (forms.ModelForm):
	class Meta:
		model = Proyecto
		#exclude = ('organizacion')
		
class FormularioPuesto (forms.ModelForm):
	class Meta:
		model = Puesto
		
class FormInteres (forms.ModelForm):
	
	es_favorito = forms.TypedChoiceField(coerce=lambda x: True if x=='True' else False,
									choices =((False,'Especialidad/Profesional'), (True,'Afición/favorito')), widget = forms.RadioSelect)
	class Meta:
		model = Intereses
		widgets = { 'descripcion': forms.Textarea(attrs = {'rows': 5, 'placeholder':u'Descripci\u00f3n'}),
					'nombre': forms.TextInput(attrs={'placeholder':'Nombre'})}

