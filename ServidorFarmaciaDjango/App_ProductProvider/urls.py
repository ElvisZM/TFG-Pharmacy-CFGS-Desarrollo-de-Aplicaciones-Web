from django.urls import path
from .import views

urlpatterns = [
    path('registrar/producto/csv', views.registrar_producto_csv),
    path('registrar/producto/formulario', views.producto_create),
    path('productos/list', views.productos_list),
    path('farmacias/list', views.farmacias_list),
    path('proveedores/list', views.proveedores_list),
    path('categorias/list', views.categorias_list),
    path('suministros/productos/list', views.suministro_productos_list),
    path('productos/buscador/query/simple/<str:busqueda>', views.productos_buscador_simple),
    path('modificar/producto/<str:cn_prod>', views.producto_editar),
    path('eliminar/producto/<int:cn_prod>/<str:cif_farm>', views.producto_eliminar),
    path('producto/<int:cn_prod>/<str:cif_farm>', views.producto_obtener),
    path('proveedor/<str:nombre_prov>', views.helper_cif_prov),
    path('categoria/<str:nombre_cat>', views.helper_id_cat),
    path('producto/recomendado/<str:nombre_cat>', views.productos_recomendados)
]