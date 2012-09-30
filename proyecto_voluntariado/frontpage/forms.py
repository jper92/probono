from django import forms
from models import Interesados

# Formulario para el modelo Interesados
class InteresadosForm (forms.ModelForm):
    class Meta:
        model = Interesados
        widgets = { 'nombre': forms.TextInput(attrs={'class':'span3', 'placeholder':'Nombre'}), 'correo':forms.TextInput(attrs={'class':'span3', 'placeholder':'Correo-e'}), }
