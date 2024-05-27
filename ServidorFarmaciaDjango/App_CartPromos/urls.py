from django.urls import path
from .import views

urlpatterns = [
    path('carrito/usuario', views.carrito_usuario),
    path('carrito/usuario/agregar/producto/<int:producto_id>', views.agregar_al_carrito),
    path('carrito/eliminar/producto/<int:producto_id>', views.quitar_del_carrito),
    path('carrito/actualizar/cantidad/producto/<int:producto_id>', views.actualizar_cantidad_producto)
]