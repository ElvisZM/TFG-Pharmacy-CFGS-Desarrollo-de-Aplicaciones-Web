from django.db import models
from django.conf import settings
from django.utils import timezone

 
class Subscripcion(models.Model):
    plan_sub = models.CharField(max_length=200)
    descripcion_sub = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    cliente_id = models.OneToOneField(settings.CLIENT_MODEL, on_delete=models.CASCADE)
    
class Votacion(models.Model):
    numeros = [
        (1,"1"), 
        (2,"2"), 
        (3,"3"),
        (4,"4"),
        (5,"5"),
        ]
    puntuacion = models.IntegerField(choices=numeros)
    fecha_votacion = models.DateField(default=timezone.now)
    comenta_votacion = models.TextField()
    producto_id = models.ForeignKey(settings.PRODUCT_MODEL, on_delete=models.CASCADE)
    cliente_id = models.ForeignKey(settings.CLIENT_MODEL, on_delete=models.CASCADE)
    

class Compra(models.Model):
    fecha_compra = models.DateField(null=False, blank=False)
    cliente_id = models.ForeignKey(settings.CLIENT_MODEL, on_delete=models.CASCADE)
    empleado_id = models.ForeignKey(settings.EMPLOYEE_MODEL, on_delete=models.CASCADE)
    carrito_id = models.OneToOneField(settings.CART_MODEL, on_delete=models.CASCADE)


class Pago(models.Model):
    entidades = [
        ("CA","Caixa"),
        ("BB","BBVA"),
        ("UN","UNICAJA"),
        ("IN","ING Direct"),
    ]
    banco = models.CharField(
        max_length=2,
        choices=entidades,
    )
    numero_tarjeta = models.CharField(max_length=20)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    cliente_id = models.ForeignKey(settings.CLIENT_MODEL, on_delete=models.CASCADE)
    subscripcion_id = models.ForeignKey(Subscripcion, on_delete=models.CASCADE)
    compra_id = models.ForeignKey(Compra, on_delete=models.CASCADE)
    

class HistorialCliente(models.Model):
    cliente_id = models.OneToOneField(settings.CLIENT_MODEL, on_delete=models.CASCADE)
    compra_id = models.ManyToManyField(Compra)
       
class Tratamiento(models.Model):
    veces_al_dia = models.IntegerField()
    fecha_inicio = models.DateField() 
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    cliente_id = models.ForeignKey(settings.CLIENT_MODEL, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(settings.PRODUCT_MODEL, on_delete=models.CASCADE)