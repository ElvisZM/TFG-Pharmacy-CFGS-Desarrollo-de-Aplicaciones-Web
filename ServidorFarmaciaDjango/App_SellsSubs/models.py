from django.db import models
from django.conf import settings
from django.utils import timezone
from App_ProductProvider.models import *
from App_CartPromos.models import *

 
class Subscripcion(models.Model):
    plan_sub = models.CharField(max_length=200)
    descripcion_sub = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    cliente_id = models.OneToOneField('App_AuthUsers.Cliente', on_delete=models.CASCADE, db_column='cliente_id')
    
class Votacion(models.Model):
    puntuacion = models.IntegerField()
    fecha_votacion = models.DateField(default=timezone.now)
    comenta_votacion = models.TextField()
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='producto_id')
    cliente_id = models.ForeignKey('App_AuthUsers.Cliente', on_delete=models.CASCADE, db_column='cliente_id')
    

class Compra(models.Model):
    fecha_compra = models.DateField(null=False, blank=False)
    direccion_envio = models.CharField(max_length=200)
    codigo_postal = models.IntegerField()
    municipio = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    total_pago = models.FloatField() 
    cliente_id = models.ForeignKey('App_AuthUsers.Cliente', on_delete=models.CASCADE, db_column='cliente_id')
    carrito_id = models.OneToOneField(CarritoCompra, on_delete=models.CASCADE, db_column='carrito_id')


class Pago(models.Model):
    tipo_pago = models.CharField(max_length=30)
    titular_tarjeta = models.CharField(max_length=100, null=True, blank=True)
    numero_tarjeta = models.CharField(max_length=100, null=True, blank=True)
    tipo_tarjeta = models.CharField(max_length=100, null=True, blank=True)
    id_transaccion = models.CharField(max_length=100, null=True, blank=True)
    paypal_email_transaccion = models.CharField(max_length=100, null=True, blank=True)
    fecha_pago = models.DateField(null=False, blank=False)
    cliente_id = models.ForeignKey('App_AuthUsers.Cliente', on_delete=models.CASCADE, db_column='cliente_id')
    subscripcion_id = models.ForeignKey(Subscripcion, on_delete=models.CASCADE, db_column='subscripcion_id', null=True, blank=True)
    compra_id = models.ForeignKey(Compra, on_delete=models.CASCADE, db_column='compra_id')
    

class HistorialCliente(models.Model):
    cliente_id = models.OneToOneField('App_AuthUsers.Cliente', on_delete=models.CASCADE, db_column='cliente_id')
    pago_id = models.ForeignKey(Pago, on_delete=models.CASCADE, db_column='pago_id')
    compra_id = models.ManyToManyField(Compra)
       
class Tratamiento(models.Model):
    veces_al_dia = models.IntegerField()
    fecha_inicio = models.DateField() 
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    cliente_id = models.ForeignKey('App_AuthUsers.Cliente', on_delete=models.CASCADE, db_column='cliente_id')
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='producto_id')