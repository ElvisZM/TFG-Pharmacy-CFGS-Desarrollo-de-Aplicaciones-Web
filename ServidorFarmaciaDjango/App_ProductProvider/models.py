from django.db import models
from django.conf import settings



class Farmacia(models.Model):
    cif_farm = models.CharField(max_length=8)
    nombre_farm = models.CharField(max_length=200)
    direccion_farm = models.CharField(max_length=200)
    telefono_farm = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_farm

class Categoria(models.Model):
    nombre_cat = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre_cat
    
class Proveedor(models.Model):
    cif_prov = models.CharField(max_length=8)
    nombre_prov = models.CharField(max_length=200)
    direccion_prov = models.CharField(max_length=200)
    telefono_prov = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_prov

class Producto(models.Model):
    cn_prod = models.IntegerField()
    imagen_prod = models.ImageField(upload_to='productos/', null=True, blank=True)
    nombre_prod = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    ventas = models.IntegerField(default=0)
    cif_farm = models.CharField(max_length=8)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='categoria_id')
    farmacia_id = models.ForeignKey(Farmacia, on_delete=models.CASCADE, db_column='farmacia_id')
    proveedor_id = models.ManyToManyField(Proveedor, through='SuministroProducto')
    
    def __str__(self):
        return self.nombre_prod
    
class Prospecto(models.Model):
    detalles = models.TextField()
    composicion = models.TextField()
    modo_de_uso = models.TextField()
    fecha_vencimiento = models.DateField()
    cn_prod = models.CharField(max_length=10)
    producto_id = models.OneToOneField(Producto, on_delete=models.CASCADE, db_column='producto_id')

    def __str__(self):
        return self.producto.nombre_prod

class SuministroProducto(models.Model):
    fecha_pedido = models.DateField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    costo_ud = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cn_prod = models.IntegerField()
    cif_prov = models.CharField(max_length=8)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='producto_id')
    proveedor_id = models.ForeignKey(Proveedor, on_delete=models.CASCADE, db_column='proveedor_id')
