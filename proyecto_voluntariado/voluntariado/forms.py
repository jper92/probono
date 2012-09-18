
from models import *
from django import forms

class FormularioONG(forms.ModelForm):
	
	class Meta:
		model = Organizacion
		exclude = ('es_empresa', 'expira',)

class FormularioEmpresa(forms.ModelForm):
	
	class Meta:
		model = Organizacion
		exclude = ('es_empresa',)

class FormularioVoluntario (forms.ModelForm):
	
	class Meta:
		model = Voluntario
		
class FormularioProyecto (forms.ModelForm):
	
	class Meta:
		model = Proyecto
		


