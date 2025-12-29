import uuid
from django.db import models

# Create your models here.
class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='direcciones'
    )

    provincia = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)

    calle = models.CharField(max_length=100, blank=True, null=True)
    numero_casa = models.CharField(max_length=20, blank=True, null=True)

    nombre_residencial = models.CharField(max_length=100, blank=True, null=True)
    manzana = models.CharField(max_length=10, blank=True, null=True)

    nombre_edificio = models.CharField(max_length=50, blank=True, null=True)
    piso = models.CharField(max_length=10, blank=True, null=True)
    apartamento = models.CharField(max_length=10, blank=True, null=True)

    referencia = models.TextField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sector} - {self.nombre_residencial or 'Sin residencial'}"

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
