from django import forms
from models import Interesados

# Formulario para el modelo Interesados
class InteresadosForm (forms.ModelForm):
    class Meta:
        model = Interesados
