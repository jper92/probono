
from models import *
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

class FormularioONG(forms.ModelForm):
	
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget = forms.PasswordInput)
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox inline'}), )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple)	
	class Meta:
		model = Organizacion
		exclude = ('es_empresa', 'expira', 'user')
		widgets = { 'descripcion': forms.Textarea(attrs={'rows':4}), 'objetivos': forms.Textarea(attrs={'rows':4}) }

class FormularioEmpresa(forms.ModelForm):
	
	class Meta:
		model = Organizacion
		exclude = ('es_empresa',)

class FormularioVoluntario (forms.ModelForm):
	"""
	"""
	
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget = forms.PasswordInput)
	especialidades = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=False), widget = forms.CheckboxSelectMultiple(attrs={'class':'checkbox inline'}), )
	favoritos = forms.ModelMultipleChoiceField(queryset = Intereses.objects.filter(es_favorito=True), widget = forms.CheckboxSelectMultiple)
	sexo = forms.TypedChoiceField(coerce=lambda x: True if x=='True' else False,
									choices =((False,'Femenino'), (True,'Masculino')), widget = forms.RadioSelect)
	class Meta:
		model = Voluntario
		exclude = ('user')
		widgets = { 'nacimiento': SelectDateWidget(years=range(datetime.datetime.now().year-50, datetime.datetime.now().year-9)),  }
		
class FormularioProyecto (forms.ModelForm):
	
	class Meta:
		model = Proyecto
		


