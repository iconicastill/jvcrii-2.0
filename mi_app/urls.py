from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/<uuid:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<uuid:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),

    # direcciones
    path('clientes/<uuid:cliente_id>/direcciones/', views.listar_direcciones, name='listar_direcciones'),
    path('clientes/<uuid:cliente_id>/direcciones/agregar/', views.agregar_direccion, name='agregar_direccion'),
    path('direcciones/<uuid:direccion_id>/editar/', views.editar_direccion, name='editar_direccion'),
    path('direcciones/<uuid:direccion_id>/eliminar/', views.eliminar_direccion, name='eliminar_direccion'),

    # productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    # facturas
    # path('facturas/', views.listar_facturas, name='listar_facturas'),
    # path('facturas/agregar/', views.agregar_factura, name='agregar_factura'),
    # path('facturas/<int:factura_id>/', views.ver_factura, name='ver_factura'),
    # path('facturas/<int:factura_id>/editar/', views.editar_factura, name='editar_factura'),
    # path('facturas/<int:factura_id>/eliminar/', views.eliminar_factura, name='eliminar_factura'),

    path('facturas/crear/', views.crear_factura, name='crear_factura'),
    path('facturas/<int:factura_id>/', views.detalle_factura, name='detalle_factura'),
    path('facturas/<int:factura_id>/emitir/', views.emitir_factura, name='emitir_factura'),
    path('facturas/borradores/', views.listar_borradores, name='listar_borradores'),
    path('facturas/', views.listar_facturas, name='listar_facturas'),
    path('facturas/<int:factura_id>/anular/', views.anular_factura, name='anular_factura'),

]