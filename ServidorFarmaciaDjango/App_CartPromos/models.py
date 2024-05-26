from django.db import models
from django.conf import settings
from App_ProductProvider.models import *

   
class Promocion(models.Model):
    nombre_promo = models.CharField(max_length=100)
    descripcion_promo = models.TextField()
    descuento_promo = models.IntegerField(default=0)
    fecha_fin_promo = models.DateField(null=True, blank=True)
    producto_id = models.ManyToManyField(Producto)
    cliente_id = models.ManyToManyField('App_AuthUsers.Cliente', blank=True)
        
    def __str__(self):
        return self.nombre_promo
    

class CarritoCompra(models.Model):
    codigo_compra = models.CharField(max_length=12)
    finalizado = models.BooleanField(default=False)
    usuario = models.ForeignKey('App_AuthUsers.Usuario', on_delete=models.CASCADE)
    producto_carrito = models.ManyToManyField(Producto, through='ContenidoCarrito')


class ContenidoCarrito(models.Model):    
    cantidad_producto = models.IntegerField(default=1)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito_id = models.ForeignKey(CarritoCompra, on_delete=models.CASCADE)


