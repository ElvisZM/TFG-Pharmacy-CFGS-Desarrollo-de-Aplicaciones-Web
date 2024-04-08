from django.db import models
from django.conf import settings



class Farmacia(models.Model):
    nombre_farm = models.CharField(max_length=200)
    direccion_farm = models.CharField(max_length=200)
    telefono_farm = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_farm
    
class Proveedor(models.Model):
    nombre_prov = models.CharField(max_length=200)
    direccion_prov = models.CharField(max_length=200)
    telefono_prov = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_prov

class Producto(models.Model):
    imagen_prod = models.ImageField(upload_to='productos/')
    nombre_prod = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField(default=0)
    farmacia_id = models.ForeignKey(Farmacia, on_delete=models.CASCADE)
    proveedor_id = models.ManyToManyField(Proveedor, through='SuministroProducto')
    
    def __str__(self):
        return self.nombre_prod
    
class Prospecto(models.Model):
    detalles = models.TextField()
    composicion = models.TextField()
    modo_de_uso = models.TextField()
    fecha_vencimiento = models.DateField()
    producto_id = models.OneToOneField(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.producto.nombre_prod
    

class SuministroProducto(models.Model):
    fecha = models.DateField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    costo_ud = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor_id = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

