from django.urls import path
from .api_views import *


urlpatterns = [
    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),
    
    path('upload-file/', FileUploadAPIView.as_view()),
    path('upload-file/<int:pk>/', FileUploadAPIView.as_view(), name='file-detail'),
    
    path('productos', producto_list),
    path('producto/<int:producto_id>', producto_obtener),
    path('productos/mejorado', producto_list_mejorado),
    path('producto/busqueda_simple', producto_buscar),
    path('producto/busqueda_avanzada', producto_busqueda_avanzada),
    path('producto/crear', producto_create),
    path('producto/editar/<int:producto_id>', producto_editar),
    path('producto/actualizar/nombre/<int:producto_id>', producto_actualizar_nombre),
    path('producto/eliminar/<int:producto_id>', producto_eliminar),
    
    path('empleados', empleado_list),
    path('empleados/mejorado', empleado_list_mejorado),
    path('empleado/busqueda_avanzada', empleado_busqueda_avanzada),
    
    path('farmacia/<int:farmacia_id>', farmacia_obtener),
    path('farmacias', farmacia_list),
    path('farmacia/busqueda_simple', farmacia_buscar),
    path('farmacia/crear', farmacia_create),
    path('farmacia/editar/<int:farmacia_id>', farmacia_editar),
    path('farmacia/actualizar/nombre/<int:farmacia_id>', farmacia_actualizar_nombre),
    path('farmacia/eliminar/<int:farmacia_id>', farmacia_eliminar),
    
    path('votacion/<int:votacion_id>', votacion_obtener),
    path('votaciones/mejorado', votacion_list_mejorado),
    path('votacion/busqueda_simple', votacion_buscar),
    path('votacion/busqueda_avanzada', votacion_busqueda_avanzada),
    path('votacion/crear', votacion_create),
    path('votacion/editar/<int:votacion_id>', votacion_editar),
    path('votacion/actualizar/puntuacion/<int:votacion_id>', votacion_actualizar_puntuacion),
    path('votacion/eliminar/<int:votacion_id>', votacion_eliminar),
    
    path('proveedores', proveedor_list),
    
    path('clientes', clientes_list),
    
    path('promociones', promociones_list),
    
    path('productos/stock/asc', productos_stock_asc),
    path('productos/stock/desc', productos_stock_desc),

    path('producto/agregar/carrito/<int:producto_id>', agregar_al_carrito),
    path('producto/quitar/carrito/<int:producto_id>', quitar_del_carrito),
    path('producto/quitar/unidad/carrito/<int:producto_id>', bajar_unidad_carrito),
    path('carrito/usuario', carrito_usuario),
    
    path('producto/prospecto/<int:producto_id>', producto_prospecto),
    
    
    path('tratamiento/lista/mejorada', tratamiento_lista_mejorada),
    path('tratamiento/eliminar/<int:tratamiento_id>', tratamiento_eliminar),

    path('tratamiento/crear', tratamiento_create),

    path('registro/google', registrar_usuario_google.as_view()),

]
