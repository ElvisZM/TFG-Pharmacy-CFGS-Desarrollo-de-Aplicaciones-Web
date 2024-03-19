from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    EMPLEADO = 3
    GERENTE = 4
    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (EMPLEADO, 'Empleado'),
        (GERENTE, 'Gerente'),
    )
    
    rol = models.PositiveSmallIntegerField(choices=ROLES, default=CLIENTE)

class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    direccion_admin = models.CharField(max_length=200)
    telefono_admin = models.IntegerField(null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)

class Farmacia(models.Model):
    nombre_farm = models.CharField(max_length=200)
    direccion_farm = models.CharField(max_length=200)
    telefono_farm = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_farm

class Gerente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    direccion_ger = models.CharField(max_length=200)
    telefono_ger = models.IntegerField(null=True, blank=True)
    salario_ger = models.FloatField(default=2100.0)
    birthday_date = models.DateField(null=True, blank=True)
    gerente_farm = models.OneToOneField(Farmacia, on_delete=models.CASCADE, null=True)


class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    direccion_emp = models.CharField(max_length=200)
    telefono_emp = models.IntegerField(null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    salario = models.FloatField(default=1024.0)
    farm_emp = models.ForeignKey(Farmacia, on_delete=models.CASCADE, null=True, blank=True) 

    
class Proveedor(models.Model):
    nombre_prov = models.CharField(max_length=200)
    direccion_prov = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre_prov

class Producto(models.Model):
    imagen_prod = models.ImageField(upload_to='productos/')
    nombre_prod = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField(default=0)
    farmacia_prod = models.ForeignKey(Farmacia, on_delete=models.CASCADE)
    prov_sum_prod = models.ManyToManyField(Proveedor, through='SuministroProducto')
    
    def __str__(self):
        return self.nombre_prod
    
class Prospecto(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    detalles = models.TextField()
    composicion = models.TextField()
    modo_de_uso = models.TextField()

    def __str__(self):
        return self.producto.nombre_prod
    

class SuministroProducto(models.Model):
    fecha_sum = models.DateField(null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    costo_ud = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion_cli = models.CharField(max_length=200, null=True, blank=True)
    telefono_cli = models.IntegerField(null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    productos_favoritos = models.ManyToManyField(Producto, related_name='productos_favoritos')
    votacion_prod = models.ManyToManyField(Producto, through='Votacion', related_name='votacion_prod')
    
class Subscripcion(models.Model):
    cliente_sub = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    plan_sub = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    
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
    voto_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    voto_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

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
    cuenta_bancaria = models.CharField(max_length=20)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    cliente_pago = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    subscripcion_pago = models.ForeignKey(Subscripcion, on_delete=models.CASCADE)
    

class Compra(models.Model):
    fecha_compra = models.DateField(null=False, blank=False)
    cliente_compra = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado_compra = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class DetalleCompra(models.Model):
    cantidad_prod_comprado = models.IntegerField(null=True, blank=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto_detalle = models.ForeignKey(Producto, on_delete=models.CASCADE)

class HistorialCliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    total_compras = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class DatosFarmacia(models.Model):
    farmacia_datos = models.OneToOneField(Farmacia, on_delete=models.CASCADE)
    descripcion = models.TextField()
    horario = models.CharField(max_length=100)
    fecha_creacion = models.DateField()

class DetalleProducto(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_stock = models.IntegerField(default=0)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    
class Promocion(models.Model):
    nombre_promo = models.CharField(max_length=100)
    descripcion_promo = models.TextField()
    valor_promo = models.IntegerField(default=0)
    fecha_fin_promo = models.DateField(null=True, blank=True)
    cliente_promo = models.ManyToManyField(Cliente, blank=True)
        
    def __str__(self):
        return self.nombre_promo
    
class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.uploaded_on.date()

class CarritoCompra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto_carrito = models.ManyToManyField(Producto, through='UsuarioCarrito')
    realizado = models.BooleanField(default=False)
    

class UsuarioCarrito(models.Model):
    carrito = models.ForeignKey(CarritoCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField(default=1)
        
        
class Tratamiento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    veces_al_dia = models.IntegerField()
    fecha_inicio = models.DateField() 
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)