from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Direccion, Producto, Factura, FacturaDetalle
# from django import forms
from .forms import ClienteForm, DireccionForm, ProductoForm, InventarioForm, FacturaForm, FacturaDetalleForm
from django.db.models import Q, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.db.models import Max
from django.views.decorators.http import require_POST





# Create your views here.
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()

    return render(request, 'mi_app/dashboard.html', {
        'total_productos': total_productos,
    })

def listar_clientes(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.prefetch_related('direcciones')

    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(email__icontains=query)
        )

    total_clientes = Cliente.objects.count()

    return render(request, 'mi_app/clientes/listar.html', {
        'clientes': clientes,
        'query': query,
    })

def listar_direcciones(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    direcciones = cliente.direcciones.all()

    return render(request, 'mi_app/direcciones/listar.html', {
        'cliente': cliente,
        'direcciones': direcciones
    })

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente agregado correctamente")
            return redirect('dashboard')
        else:
            messages.error(request, "Ocurrió un error al guardar el cliente")
    else:
        form = ClienteForm()

    return render(request, 'mi_app/clientes/form.html', {
        'form': form,
        'titulo': 'Agregar cliente'
    })

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente")
            return redirect('dashboard')
        else:
            messages.error(request, "Ocurrió un error al actualizar el cliente")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'mi_app/clientes/form.html', {
        'form': form,
        'titulo': 'Editar cliente',
        'cliente': cliente
    })

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, "Cliente eliminado correctamente")
            return redirect('dashboard')
        except Exception:
            messages.error(request, "Ocurrió un error al eliminar el cliente")
            return redirect('dashboard')

    return render(request, 'mi_app/clientes/eliminar.html', {
        'cliente': cliente
    })

@login_required
def agregar_direccion(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.cliente = cliente
            direccion.save()
            messages.success(request, 'Dirección agregada correctamente')
            return redirect('listar_direcciones', cliente_id=cliente.id)
    else:
        form = DireccionForm()

    return render(request, 'mi_app/direcciones/form.html', {
        'form': form,
        'cliente': cliente,
        'titulo': 'Agregar dirección'
    })

@login_required
def editar_direccion(request, direccion_id):
    direccion = get_object_or_404(Direccion, id=direccion_id)
    cliente = direccion.cliente

    if request.method == 'POST':
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dirección actualizada correctamente')
            return redirect('listar_direcciones', cliente_id=cliente.id)
        else:
            messages.error(request, "Error al actualizar la dirección")    
    else:
        form = DireccionForm(instance=direccion)

    return render(request, 'mi_app/direcciones/form.html', {
        'form': form,
        'direccion': direccion,
        'cliente': cliente,
        'titulo': 'Editar dirección'
    })

@login_required
def eliminar_direccion(request, direccion_id):
    direccion = get_object_or_404(Direccion, id=direccion_id)
    cliente_id = direccion.cliente.id

    if request.method == 'POST':
        direccion.delete()
        messages.success(request, 'Dirección eliminada correctamente')
        return redirect('listar_direcciones', cliente_id=cliente_id)

    return render(request, 'mi_app/direcciones/eliminar.html', {
        'direccion': direccion
    })

def listar_productos(request):
    query = request.GET.get('q', '')

    productos = Producto.objects.all()

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    return render(request, 'mi_app/productos/listar.html', {
        'productos': productos,
        'query': query
    })

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        inventario_form = InventarioForm(request.POST)

        if producto_form.is_valid():
            producto = producto_form.save()

            if producto.tipo == 'fisico' and inventario_form.is_valid():
                inventario = inventario_form.save(commit=False)
                inventario.producto = producto
                inventario.save()

            return redirect('listar_productos')

    else:
        producto_form = ProductoForm()
        inventario_form = InventarioForm()

    mostrar_inventario = request.POST.get('tipo') == 'fisico'

    return render(request, 'mi_app/productos/form.html', {
        'producto_form': producto_form,
        'inventario_form': inventario_form,
        'mostrar_inventario': mostrar_inventario,
        'titulo': 'Agregar producto'
    })

    
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    inventario = getattr(producto, 'inventario', None)

    if request.method == 'POST':

        print(request.POST)  # 👈 AQUÍ

        producto_form = ProductoForm(request.POST, instance=producto)
        inventario_form = InventarioForm(
            request.POST,
            instance=inventario
        )

        if producto_form.is_valid() and (
            producto.tipo != 'fisico' or inventario_form.is_valid()
        ):
            
            producto = producto_form.save()

            if producto.tipo == 'fisico':
                    inv = inventario_form.save(commit=False)
                    inv.producto = producto
                    inv.save()
            else:
                # Si pasó de físico a servicio → eliminar inventario
                if inventario:
                    inventario.delete()

            return redirect('listar_productos')

    else:
        producto_form = ProductoForm(instance=producto)
        inventario_form = InventarioForm(instance=inventario)

    mostrar_inventario = (
        producto_form.instance.tipo == 'fisico'
        or request.POST.get('tipo') == 'fisico'
    )

    return render(request, 'mi_app/productos/form.html', {
        'producto_form': producto_form,
        'inventario_form': inventario_form,
        'producto': producto,
        'mostrar_inventario': mostrar_inventario,
        'titulo': 'Editar producto'
    })

    


@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')

    return render(request, 'mi_app/productos/eliminar.html', {
        'producto': producto
    })

# Nuevo view para listar facturas

@login_required
def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.estado = 'borrador'
            factura.numero = None  # importante
            factura.save()
            return redirect('detalle_factura', factura_id=factura.id)
    else:
        form = FacturaForm()

    return render(request, 'mi_app/facturas/crear.html', {
        'form': form
    })


@login_required
def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    detalles = factura.detalles.all()

    if factura.estado != 'borrador':
        form = None
    else:
        if request.method == 'POST':
            form = FacturaDetalleForm(request.POST)
            if form.is_valid():
                detalle = form.save(commit=False)
                detalle.factura = factura
                detalle.save()
                recalcular_factura(factura)
                return redirect('detalle_factura', factura_id=factura.id)
        else:
            form = FacturaDetalleForm()

    return render(request, 'mi_app/facturas/detalle_factura.html', {
        'factura': factura,
        'detalles': detalles,
        'form': form
    })

def recalcular_factura(factura):
    subtotal = factura.detalles.aggregate(
        total=Sum('subtotal')
    )['total'] or Decimal('0.00')

    impuesto = subtotal * Decimal('0.18')
    total = subtotal + impuesto

    factura.subtotal = subtotal
    factura.impuesto = impuesto
    factura.total = total
    factura.save()

@transaction.atomic
@login_required
def emitir_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if factura.estado != 'borrador':
        return redirect('detalle_factura', factura_id=factura.id)

    # Validar stock
    for detalle in factura.detalles.select_related('producto'):
        producto = detalle.producto
        if producto.tipo == 'fisico':
            inventario = producto.inventario
            if inventario.stock < detalle.cantidad:
                messages.error(
                    request,
                    f"Stock insuficiente para {producto.nombre}"
                )
                return redirect('detalle_factura', factura_id=factura.id)

    # Descontar stock
    for detalle in factura.detalles.select_related('producto'):
        producto = detalle.producto
        if producto.tipo == 'fisico':
            inventario = producto.inventario
            inventario.stock -= detalle.cantidad
            inventario.save()

    # Numerar y emitir
    factura.numero = generar_numero_factura()
    factura.estado = 'emitida'
    factura.save()

    messages.success(request, "Factura emitida correctamente")
    return redirect('detalle_factura', factura_id=factura.id)

def generar_numero_factura():
    ultimo = Factura.objects.aggregate(
        Max('numero')
    )['numero__max']

    return (ultimo or 0) + 1



@login_required
@transaction.atomic
def anular_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if factura.estado != 'emitida':
        return redirect('detalle_factura', factura_id=factura.id)

    # Revertir stock
    for detalle in factura.detalles.select_related('producto'):
        if detalle.producto.tipo == 'fisico':
            inventario = detalle.producto.inventario
            inventario.stock += detalle.cantidad
            inventario.save()

    factura.estado = 'anulada'
    factura.save()

    messages.warning(request, 'Factura anulada')
    return redirect('detalle_factura', factura_id=factura.id)


@require_POST
def borrar_borrador(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if factura.estado != 'BORRADOR':
        messages.error(request, "Solo los borradores pueden eliminarse.")
        return redirect('listar_facturas')

    factura.delete()
    messages.success(request, "Borrador eliminado correctamente.")

    return redirect('listar_facturas')


@login_required
def listar_facturas(request):
    facturas = (
        Factura.objects
        .select_related('cliente')
        .order_by('-creada')
    )

    return render(request, 'mi_app/facturas/listar.html', {
        'facturas': facturas
    })
