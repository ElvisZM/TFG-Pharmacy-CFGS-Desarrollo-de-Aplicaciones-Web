from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Gerente)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Administrador)

