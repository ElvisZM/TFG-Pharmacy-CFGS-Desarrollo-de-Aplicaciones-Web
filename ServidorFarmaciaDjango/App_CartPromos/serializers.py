from rest_framework import serializers
from .models import *
from .forms import *
from App_AuthUsers.serializers import *
from App_ProductProvider.serializers import *

  
class ContenidoCarritoSerializer(serializers.ModelSerializer):
    producto_id = ProductoSerializer(read_only=True)

    class Meta:
        model = ContenidoCarrito
        fields = ['producto_id', 'cantidad_producto']
        
        
class CarritoCompraSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    usuario = UsuarioSerializer()
    
    #Para relaciones ManyToMany
    productos = serializers.SerializerMethodField()
    class Meta:
        model = CarritoCompra
        fields = ['id', 'codigo_compra', 'finalizado', 'usuario', 'productos']

    def get_productos(self, obj):
        contenido_carrito = ContenidoCarrito.objects.filter(carrito_id=obj)
        return ContenidoCarritoSerializer(contenido_carrito, many=True).data