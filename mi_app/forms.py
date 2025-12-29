from django import forms
from .models import Direccion, Cliente, Producto, Inventario

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre', 
            'email', 
            'telefono'
        ]

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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'codigo',
            'descripcion',
            'precio',
            'tipo',
            'activo',
        ]

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['cantidad']

