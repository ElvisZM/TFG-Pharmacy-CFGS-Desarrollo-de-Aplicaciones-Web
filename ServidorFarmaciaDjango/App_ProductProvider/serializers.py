from rest_framework import serializers
from .models import *
from .forms import *
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile


class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    
    farmacia_id = FarmaciaSerializer()
    
    proveedor_id = ProveedorSerializer(read_only=True, many=True)
    
    class Meta:
        model = Producto
        fields = ('id','imagen_prod','nombre_prod','descripcion','precio','stock','farmacia_id','proveedor_id')


class ProductoSerializerCreate(serializers.Serializer):
    
    class Meta:
        model = Producto
        fields = ['nombre_prod', 'descripcion', 'precio', 'stock', 'farmacia_id', 'proveedor_id']
        
        
    def validate_nombre_prod(self,nombre):
        productoNombre = Producto.objects.filter(nombre_prod=nombre, farmacia_prod= self.initial_data['farmacia_id']).first()
        if(not productoNombre is None):
            if(not self.instance is None and productoNombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('El producto ya existe en esta farmacia')
        return nombre
    
    def validate_descripcion(self,descripcion):
        if len(descripcion) < 10:
            raise serializers.ValidationError('La descripcion debe contener minimo 10 caracteres')
        return descripcion
    
    def validate_precio(self,precio):
        if type(precio) != float:
            raise serializers.ValidationError('El precio introducido no es válido')
        return precio
    
    def validate_stock(self, stock):
        if type(stock) != int or stock < 0:
            raise serializers.ValidationError('El stock introducido no es válido')
        return stock
    
    def create(self, validated_data):
        if('proveedor_id' not in self.initial_data):
            raise serializers.ValidationError(
                {'proveedor_id': ['No ha seleccionado proveedores']}
                )

        proveedores = self.initial_data['proveedor_id']
        imagen_prod = base64.b64encode(self.initial_data['imagen_prod'])
        contenido_archivo = ContentFile(imagen_prod)
        
        archivo = InMemoryUploadedFile(
            contenido_archivo,
            None,
            validated_data['nombre_prod'],
            self.initial_data['formato_imagen'],
            contenido_archivo.size,
            None
        )
        
        producto = Producto.objects.create(
            nombre_prod = validated_data['nombre_prod'],
            descripcion = validated_data['descripcion'],
            precio = validated_data['precio'],
            stock = validated_data['stock'],
            farmacia_id = validated_data['farmacia_id'],
            imagen_prod = validated_data['imagen_prod'],
            )
        fecha_actual = date.today()
        
        for proveedor in proveedores:
            modeloProveedor = Proveedor.objects.get(id=proveedor)
            SuministroProducto.objects.create(fecha=fecha_actual, cantidad=validated_data['stock'], costo_ud=(round(validated_data['precio']/1.30)), proveedor_id = modeloProveedor, producto_id=producto)
        
        return producto
    
    def update(self, instance, validated_data):
        
        fecha_actual = date.today()
        
        proveedores = self.initial_data['proveedor_id']
        if len(proveedores) < 1:
            raise serializers.ValidationError(
                {'proveedor_id': 'Debe seleccionar al menos un proveedor'}
            )
            
        instance.nombre_prod = validated_data['nombre_prod']
        instance.descripcion = validated_data['descripcion']
        instance.precio = validated_data['precio']
        instance.stock = validated_data['stock']
        instance.farmacia_id = validated_data['farmacia_id']
        instance.save()
        
        instance.proveedor_id.clear()
        for proveedor in proveedores:
            modeloProveedor = Proveedor.objects.get(id=proveedor)
            SuministroProducto.objects.create(fecha=fecha_actual, cantidad = validated_data['stock'], costo_ud=(round(validated_data['precio']/1.30)), proveedor_id = modeloProveedor, producto_id = instance)
            
        return instance
    
            