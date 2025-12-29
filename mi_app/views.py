from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Direccion, Producto
from django import forms
from .forms import ClienteForm, DireccionForm, ProductoForm, InventarioForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
    query = request.GET.get('q', '')

    clientes = Cliente.objects.prefetch_related('direcciones')

    if query:
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) |
            Q(email__icontains=query)
        )

    total_clientes = Cliente.objects.count()

    return render(request, 'mi_app/clientes/listar.html', {
        'clientes': clientes,
        'query': query,
        'total_clientes': total_clientes
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

    return render(request, 'mi_app/clientes/agregar.html', {'form': form})

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

    return render(request, 'mi_app/clientes/editar.html', {
        'form': form,
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

    return render(request, 'mi_app/direcciones/agregar.html', {
        'form': form,
        'cliente': cliente
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

    return render(request, 'mi_app/direcciones/editar.html', {
        'form': form,
        'direccion': direccion,
        'cliente': cliente
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
    productos = Producto.objects.all()
    return render(request, 'mi_app/productos/listar.html', {
        'productos': productos
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

    return render(request, 'productos/form.html', {
        'producto_form': producto_form,
        'inventario_form': inventario_form,
        'mostrar_inventario': mostrar_inventario,
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

