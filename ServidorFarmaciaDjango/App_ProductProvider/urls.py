from django.urls import path
from .import views

urlpatterns = [
    #path('registrar/productos', views.registrar_productos),
    path('registrar/producto/csv', views.registrar_producto_csv),
    path('registrar/producto/formulario', views.producto_create),
    path('productos/list', views.productos_list),
    path('farmacias/list', views.farmacias_list),
    path('proveedores/list', views.proveedores_list),
    path('categorias/list', views.categorias_list),
    path('suministros/productos/list', views.suministro_productos_list),
    path('modificar/producto/<str:cn_prod>', views.producto_editar),
    path('producto/<int:cn_prod>', views.producto_obtener),
    path('proveedor/<str:nombre_prov>', views.helper_cif_prov),
    path('categoria/<str:nombre_cat>', views.helper_id_cat),
]