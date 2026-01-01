import uuid
from decimal import Decimal
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

class Producto(models.Model):
    TIPO_CHOICES = [
        ('fisico', 'Físico'),
        ('servicio', 'Servicio'),
    ]

    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
class Inventario(models.Model):
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name='inventario'
    )

    stock = models.PositiveIntegerField(default=0)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.stock}"

# Nuevo modelo Factura

class Factura(models.Model):
    ESTADOS = (
        ('borrador', 'Borrador'),
        ('emitida', 'Emitida'),
        ('anulada', 'Anulada'),
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='facturas'
    )

    numero = models.PositiveIntegerField(
        unique=True,
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='borrador'
    )

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura {self.numero or 'BORRADOR'}"


class FacturaDetalle(models.Model):
    
    factura = models.ForeignKey(
        Factura,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
