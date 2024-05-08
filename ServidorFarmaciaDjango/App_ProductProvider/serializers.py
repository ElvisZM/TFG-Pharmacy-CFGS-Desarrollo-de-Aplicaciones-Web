from rest_framework import serializers
from .models import *
from .forms import *
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from App_AuthUsers.models import *

class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne o OneToOne
    farmacia_id = FarmaciaSerializer()
    
    #Para relaciones ManyToMany
    proveedor_id = ProveedorSerializer(read_only=True, many=True)
    
    class Meta:
        fields = ('cn_prod', 'imagen_prod', 'nombre_prod', 'descripcion', 'precio', 'stock', 'cif_farm', 'farmacia_id', 'proveedor_id')
        model = Producto
        
   
class SuministroProductoSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    producto = ProductoSerializer()
    proveedor = ProveedorSerializer()
    
    class Meta:
        model = SuministroProducto
        fields = '__all__'


class ProductoSerializerCreate(serializers.Serializer):
    
    farmacia_id = FarmaciaSerializer()
    
    proveedor_id = ProveedorSerializer()
    
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
    
            
            
            
            

class CsvProductoSerializerCreate(serializers.Serializer):
    
    #Campos de Producto
    cn_prod = serializers.IntegerField()
    nombre_prod = serializers.CharField()
    descripcion = serializers.CharField()
    precio = serializers.DecimalField(max_digits=5, decimal_places=2)
    cif_farm = serializers.CharField()
    
    #Campos de Proveedor
    cif_prov = serializers.CharField()
    nombre_prov = serializers.CharField()
    direccion_prov = serializers.CharField()
    telefono_prov = serializers.IntegerField()
    
    #Campos de SuministroProducto
    fecha_pedido = serializers.DateField()
    cantidad = serializers.IntegerField()
    costo_ud = serializers.DecimalField(max_digits=5, decimal_places=2)
        
    def validate_cn_prod(self, cn_prod):
        if (cn_prod is None) or (cn_prod < 0):
            raise serializers.ValidationError('Codigo Nacional inválido.')
        return cn_prod
        
    def validate_nombre_prod(self,nombre):
        productoExists = Producto.objects.filter(cn_prod=self.initial_data['cn_prod'], cif_farm= self.initial_data['cif_farm']).first()
        
        farmaciaIntroducida = Farmacia.objects.filter(cif_farm=self.initial_data['cif_farm']).first()
        
        if(not productoExists is None):
                
            if(not self.instance is None and productoExists.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('El producto ya existe en esta farmacia')
        elif (not farmaciaIntroducida):
                raise serializers.ValidationError ('La farmacia asociada al producto no existe.')
        else:    
        
            return nombre
    
    def validate_descripcion(self,descripcion):
        if len(descripcion) < 10:
            raise serializers.ValidationError('La descripcion debe contener minimo 10 caracteres')
        return descripcion
    
    def validate_precio(self,precio):
        try:
            precio = float(precio)
        except ValueError:
            raise serializers.ValidationError('El precio no es un número válido')
    
        if precio < 0:
            raise serializers.ValidationError('El precio debe ser un número positivo')
    
        return precio
    
    
    def validate_cif_prov(self, cif_prov):
        if (cif_prov is None) or (len(cif_prov)<0):
            raise serializers.ValidationError('Codigo de Identificacion Fiscal inválido.')
        return cif_prov
    
    def validate_nombre_prov(self, nombre_prov):
        if (nombre_prov is None) or (len(nombre_prov)<5):
            raise serializers.ValidationError('Nombre de proveedor inválido.')
        
        return nombre_prov
    
    def validate_direccion_prov(self,direccion):
        if len(direccion) < 10:
            raise serializers.ValidationError('La dirección debe contener mínimo 10 caracteres')
        return direccion
    
    def validate_telefono_prov(self, telefono):
        administradorTelefono = Administrador.objects.filter(telefono_admin=telefono).first()    
        gerenteTelefono = Gerente.objects.filter(telefono_ger=telefono).first()
        empleadoTelefono = Empleado.objects.filter(telefono_emp=telefono).first()
        clienteTelefono = Cliente.objects.filter(telefono_cli=telefono).first()
        farmaciaTelefono = Farmacia.objects.filter(telefono_farm=telefono).first()
        proveedorTelefono = Proveedor.objects.filter(telefono_prov=telefono).first()    

        if (str(telefono)[0] not in ('6','7','9') or len(str(telefono)) != 9) or (not(administradorTelefono is None or gerenteTelefono is None or empleadoTelefono is None or clienteTelefono is None or farmaciaTelefono is None or proveedorTelefono is None)):
            raise serializers.ValidationError('El teléfono introducido no es válido o ya existe en un usuario.')
        return telefono
    
    def validate_fecha_pedido(self, fecha_pedido):
        fecha_actual = date.today()
        if (fecha_pedido > fecha_actual):
            raise serializers.ValidationError('La fecha no puede ser mayor a la de hoy.')
        return fecha_pedido
    
    def validate_cantidad(self,cantidad):
        if type(cantidad) != int or cantidad < 0:
            raise serializers.ValidationError('La cantidad introducida no es válida.')
        return cantidad

    def validate_costo_ud(self,costo_ud):
        try:
            costo_ud = float(costo_ud)
        except ValueError:
            raise serializers.ValidationError('El costo no es un número válido')
    
        if costo_ud < 0:
            raise serializers.ValidationError('El costo_ud debe ser un número positivo')
    
        return costo_ud

    
    def create(self, validated_data):

        proveedor_existe = Proveedor.objects.filter(cif_prov= validated_data['cif_prov']).first()
        if (proveedor_existe is None):        
            modeloProveedor = Proveedor.objects.create(cif_prov=validated_data['cif_prov'], nombre_prov=validated_data['nombre_prov'], direccion_prov = validated_data['direccion_prov'], telefono_prov = validated_data['telefono_prov'])
        else:
            modeloProveedor = Proveedor.objects.get(cif_prov=validated_data['cif_prov'])
        
        
        farmaciaProducto = Farmacia.objects.get(cif_farm=validated_data['cif_farm'])
        
        producto = Producto.objects.create(
            cn_prod = validated_data['cn_prod'],
            nombre_prod = validated_data['nombre_prod'],
            descripcion = validated_data['descripcion'],
            precio = validated_data['precio'],
            stock = validated_data['cantidad'],
            cif_farm = validated_data['cif_farm'],
            farmacia_id = farmaciaProducto
            )
        
        
        SuministroProducto.objects.create(fecha_pedido=validated_data['fecha_pedido'], cantidad=validated_data['cantidad'], costo_ud=validated_data['costo_ud'], cn_prod = validated_data['cn_prod'], cif_prov = validated_data['cif_prov'], producto_id=producto, proveedor_id = modeloProveedor, )
        
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