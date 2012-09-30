
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
	"""
	"""
	
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget = forms.PasswordInput)
	intereses = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple)
	sexo = forms.TypedChoiceField(coerce=lambda x: True if x=='Masculino' else False,
									choices =((False,'Femenino'), (True,'Masculino')), widget = forms.RadioSelect)
	class Meta:
		model = Voluntario
		exclude = ('user')
#		widgets = { 'intereses': forms.CheckboxSelectMultiple(),  }
		
class FormularioProyecto (forms.ModelForm):
	
	class Meta:
		model = Proyecto
		


