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


class CategoriaProductoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne o OneToOne
    farmacia_id = FarmaciaSerializer()
    categoria_id = CategoriaProductoSerializer()
    
    #Para relaciones ManyToMany
    proveedor_id = ProveedorSerializer(read_only=True, many=True)
    
    
    class Meta:
        fields = ('id', 'cn_prod', 'imagen_prod', 'nombre_prod', 'descripcion', 'precio', 'stock', 'cif_farm', 'categoria_id', 'farmacia_id', 'proveedor_id')
        model = Producto
        
   
class SuministroProductoSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    producto = ProductoSerializer()
    proveedor = ProveedorSerializer()
    
    class Meta:
        model = SuministroProducto
        fields = '__all__'




class ProductoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Producto
        fields = ['cn_prod', 'nombre_prod', 'descripcion', 'precio', 'stock', 'cif_farm', 'categoria_id']
        
        
    def validate_cn_prod(self, cn_prod):
        
        if(cn_prod is None or cn_prod < 0):
            raise serializers.ValidationError('El código nacional no es válido.')
        
        modeloFarmacia = Farmacia.objects.filter(cif_farm=self.initial_data['cif_farm']).first()
        if(modeloFarmacia is None):
            raise serializers.ValidationError('La farmacia no existe')

        modeloProveedor = Proveedor.objects.filter(cif_prov=self.initial_data['cif_prov']).first()        
        if(modeloProveedor is None):
            raise serializers.ValidationError('El proveedor no existe')

        modeloProducto = Producto.objects.filter(cn_prod=cn_prod, farmacia_id=modeloFarmacia).first()
        
        if(not modeloProducto is None):
            if(not self.instance is None and modeloProducto.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('El producto ya existe en esta farmacia')    
        
        return cn_prod
    
    def validate_nombre_prod(self,nombre):
        
        if(nombre is None):
            raise serializers.ValidationError('El producto no tiene nombre.')
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
    
    def validate_stock(self,stock):
        if type(stock) != int or stock < 0:
            raise serializers.ValidationError('La cantidad introducida no es válida.')
        return stock

    
    def create(self, validated_data):

        modeloFarmacia = Farmacia.objects.filter(cif_farm=self.initial_data['cif_farm']).first()
        
        modeloCategoria = Categoria.objects.filter(id=self.initial_data['categoria_id']).first()
        
        modeloProveedor = Proveedor.objects.filter(cif_prov=self.initial_data['cif_prov']).first()
        
        if (modeloFarmacia is None or modeloCategoria is None or modeloProveedor is None):
            raise serializers.ValidationError('La farmacia, la categoria o el proveedor no existen')
        
        elif (self.initial_data['imagen_prod'] == ""):
            
            modeloProducto = Producto.objects.create(
            cn_prod = validated_data['cn_prod'],
            imagen_prod = self.initial_data['imagen_prod'],
            nombre_prod = validated_data['nombre_prod'],
            descripcion = validated_data['descripcion'],
            precio = validated_data['precio'],
            stock = validated_data['stock'],
            cif_farm = validated_data['cif_farm'],
            categoria_id = modeloCategoria,
            farmacia_id = modeloFarmacia,
            )
        else:
            
            format, img_str = self.initial_data['imagen_prod'].split(';base64,')
            
            ext = format.split('/')[-1] 

            archivo = ContentFile(base64.b64decode(img_str), name=validated_data['nombre_prod']+ ext)
        
            modeloProducto = Producto.objects.create(
            cn_prod = validated_data['cn_prod'],
            imagen_prod = archivo,
            nombre_prod = validated_data['nombre_prod'],
            descripcion = validated_data['descripcion'],
            precio = validated_data['precio'],
            stock = validated_data['stock'],
            cif_farm = validated_data['cif_farm'],
            categoria_id = modeloCategoria,
            farmacia_id = modeloFarmacia,
            )
        
        fecha_hoy = date.today()
        
        #La farmacia compra al proveedor un 40% más barato que el precio de venta al público
        precio_compra_proveedor = validated_data['precio']*0.6
        
        SuministroProducto.objects.create(fecha_pedido=fecha_hoy, cantidad=validated_data['stock'], costo_ud=precio_compra_proveedor, cn_prod = validated_data['cn_prod'], cif_prov = self.initial_data['cif_prov'], producto_id=modeloProducto, proveedor_id = modeloProveedor)
        
        return modeloProducto


        
    def update(self, instance, validated_data):
        
        modeloFarmacia = Farmacia.objects.filter(cif_farm=self.initial_data['cif_farm']).first()
        
        modeloCategoria = Categoria.objects.filter(id=self.initial_data['categoria_id']).first()
        
        modeloProveedor = Proveedor.objects.filter(cif_prov=self.initial_data['cif_prov']).first()


        if (modeloFarmacia is None or modeloCategoria is None or modeloProveedor is None):
            raise serializers.ValidationError('La farmacia, la categoria o el proveedor no existen')
        
        
        elif (self.initial_data['imagen_prod'] == ""):
        
        
            
            instance.cn_prod = validated_data['cn_prod']
            instance.imagen_prod = self.initial_data['imagen_prod']
            instance.nombre_prod = validated_data['nombre_prod']
            instance.descripcion = validated_data['descripcion']
            instance.precio = validated_data['precio']
            instance.stock = validated_data['stock']
            instance.cif_farm = validated_data['cif_farm']
            instance.categoria_id = modeloCategoria
            instance.farmacia_id = modeloFarmacia
            instance.save()
            
        
        else:
            
            format, img_str = self.initial_data['imagen_prod'].split(';base64,')
            
            ext = format.split('/')[-1] 

            archivo = ContentFile(base64.b64decode(img_str), name=validated_data['nombre_prod']+ ext)
                
            instance.cn_prod = validated_data['cn_prod']
            instance.imagen_prod = archivo
            instance.nombre_prod = validated_data['nombre_prod']
            instance.descripcion = validated_data['descripcion']
            instance.precio = validated_data['precio']
            instance.stock = validated_data['stock']
            instance.cif_farm = validated_data['cif_farm']
            instance.categoria_id = modeloCategoria
            instance.farmacia_id = modeloFarmacia
            instance.save()
            
        
        precio_compra_proveedor = validated_data['precio'] * 0.6
            
        modeloFarmacia = Farmacia.objects.filter(cif_farm = validated_data['cif_farm']).first()
        
        modeloProducto = Producto.objects.filter(cn_prod=validated_data['cn_prod'], cif_farm=validated_data['cif_farm']).first()
            
        SuministroProducto.objects.filter(producto_id=instance, cantidad=instance.stock).update(fecha_pedido=date.today(),
        cantidad=validated_data['stock'],
        costo_ud=precio_compra_proveedor,
        cn_prod=validated_data['cn_prod'],
        cif_prov=self.initial_data['cif_prov'],
        producto_id=instance,
        proveedor_id=modeloProveedor)

        
        
            
        return instance
    
            
            
            
            

class CsvProductoSerializerCreate(serializers.Serializer):
    
    #Campos de Producto
    cn_prod = serializers.IntegerField()
    nombre_prod = serializers.CharField()
    descripcion = serializers.CharField()
    precio = serializers.DecimalField(max_digits=5, decimal_places=2)
    cif_farm = serializers.CharField()
    nombre_cat = serializers.CharField()
    
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
        
        categoria_existe = Categoria.objects.filter(nombre_cat=validated_data['nombre_cat']).first()
        
        if categoria_existe is None:
            modeloCategoria = Categoria.objects.create(nombre_cat=validated_data['nombre_cat'])
        else:
            modeloCategoria = Categoria.objects.get(nombre_cat=validated_data['nombre_cat'])
        
        farmaciaProducto = Farmacia.objects.get(cif_farm=validated_data['cif_farm'])
        
        modeloProducto = Producto.objects.create(
            cn_prod = validated_data['cn_prod'],
            nombre_prod = validated_data['nombre_prod'],
            descripcion = validated_data['descripcion'],
            precio = validated_data['precio'],
            stock = validated_data['cantidad'],
            cif_farm = validated_data['cif_farm'],
            categoria_id = modeloCategoria,
            farmacia_id = farmaciaProducto,
            )
        
        
        SuministroProducto.objects.create(fecha_pedido=validated_data['fecha_pedido'], cantidad=validated_data['cantidad'], costo_ud=validated_data['costo_ud'], cn_prod = validated_data['cn_prod'], cif_prov = validated_data['cif_prov'], producto_id=modeloProducto, proveedor_id = modeloProveedor, )
        
        return modeloProducto
    
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