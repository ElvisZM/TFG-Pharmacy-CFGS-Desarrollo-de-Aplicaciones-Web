from django.db import models
from django.conf import settings

   
class Promocion(models.Model):
    nombre_promo = models.CharField(max_length=100)
    descripcion_promo = models.TextField()
    descuento_promo = models.IntegerField(default=0)
    fecha_fin_promo = models.DateField(null=True, blank=True)
    producto_id = models.ManyToManyField(settings.PRODUCT_MODEL)
    cliente_id = models.ManyToManyField(settings.CLIENT_MODEL, blank=True)
        
    def __str__(self):
        return self.nombre_promo
    

class CarritoCompra(models.Model):
    finalizado = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.CLIENT_MODEL, on_delete=models.CASCADE)
    producto_carrito = models.ManyToManyField(settings.PRODUCT_MODEL, through='ContenidoCarrito')

class ContenidoCarrito(models.Model):    
    producto_id = models.ForeignKey(settings.PRODUCT_MODEL, on_delete=models.CASCADE)
    carrito_id = models.ForeignKey(CarritoCompra, on_delete=models.CASCADE)

