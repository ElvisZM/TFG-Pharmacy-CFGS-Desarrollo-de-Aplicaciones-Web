from rest_framework import serializers
from .models import *
from .forms import *
from App_AuthUsers.serializers import *
from App_ProductProvider.serializers import *

class CarritoCompraSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    usuario = UsuarioSerializer()
    
    #Para relaciones ManyToMany
    producto_carrito = ProductoSerializer(read_only=True, many=True)
    
    class Meta:
        fields = '__all__'
        model = CarritoCompra
        