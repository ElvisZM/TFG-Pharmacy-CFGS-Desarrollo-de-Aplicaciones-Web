from django.urls import path
from .import views

urlpatterns = [
    #path('registrar/productos', views.registrar_productos),
    path('registrar/producto/csv', views.registrar_producto_csv),
    path('productos/list', views.productos_list),
    path('proveedores/list', views.proveedores_list),
    path('suministros/productos/list', views.suministro_productos_list)
]