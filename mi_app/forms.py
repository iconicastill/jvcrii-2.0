from django import forms
from .models import Direccion

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = [
            'provincia',
            'municipio',
            'sector',
            'calle',
            'numero_casa',
            'nombre_residencial',
            'manzana',
            'nombre_edificio',
            'piso',
            'apartamento',
            'referencia',
            'notas',
        ]
