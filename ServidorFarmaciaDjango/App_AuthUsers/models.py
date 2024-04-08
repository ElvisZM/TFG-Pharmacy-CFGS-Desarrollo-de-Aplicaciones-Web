from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


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


class Gerente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    direccion_ger = models.CharField(max_length=200)
    telefono_ger = models.IntegerField(null=True, blank=True)
    salario_ger = models.FloatField(default=2100.0)
    birthday_date = models.DateField(null=True, blank=True)
    gerente_farm = models.OneToOneField(settings.PHARMACY_MODEL , on_delete=models.CASCADE, null=True)


class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    direccion_emp = models.CharField(max_length=200)
    telefono_emp = models.IntegerField(null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    salario = models.FloatField(default=1024.0)
    farm_emp = models.ForeignKey(settings.PHARMACY_MODEL, on_delete=models.CASCADE, null=True, blank=True) 



class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion_cli = models.CharField(max_length=200, null=True, blank=True)
    telefono_cli = models.IntegerField(null=True, blank=True)
    birthday_date = models.DateField(null=True, blank=True)
    productos_favoritos = models.ManyToManyField(settings.PRODUCT_MODEL , related_name='productos_favoritos')
    votacion_prod = models.ManyToManyField(settings.PRODUCT_MODEL, through=settings.REVIEW_MODEL , related_name='votacion_prod')
    