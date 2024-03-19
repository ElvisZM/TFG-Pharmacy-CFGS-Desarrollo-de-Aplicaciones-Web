from rest_framework import serializers
from .models import *
from .forms import *
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile





class UsuarioSerializerRegistro(serializers.Serializer):
    
    username = serializers.CharField()
    first_name = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    domicilio = serializers.CharField()
    telefono = serializers.CharField()
    birthday_date = serializers.DateField()
    
    def validate_username(self, username):
        usuario = Usuario.objects.filter(username=username).first()
        
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre.')
        return username
    
    def validate_telefono(self, telefono):
        administradorTelefono = Administrador.objects.filter(telefono_admin=telefono).first()    
        gerenteTelefono = Gerente.objects.filter(telefono_ger=telefono).first()
        empleadoTelefono = Empleado.objects.filter(telefono_emp=telefono).first()
        clienteTelefono = Cliente.objects.filter(telefono_cli=telefono).first()    

        if (str(telefono)[0] not in ('6','7','9') or len(str(telefono)) != 9) or (not(administradorTelefono is None or gerenteTelefono is None or empleadoTelefono is None or clienteTelefono is None)):
            raise serializers.ValidationError('El teléfono introducido no es válido o ya existe en un usuario.')

        return telefono
        



class UsuarioSerializerRegistroGoogle(serializers.Serializer):
    
    username = serializers.CharField()
    first_name = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    domicilio = serializers.CharField(required=False, allow_blank=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    birthday_date = serializers.DateField()
    
    def validate_username(self, username):
        usuario = Usuario.objects.filter(username=username).first()
        
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre.')
        return username



class UsuarioSerializer(serializers.ModelSerializer):
    
    date_joined = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    last_login = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    class Meta:
        model = Usuario
        fields = '__all__'

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_on',)

class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
    
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
        
class ProductoSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne o OneToOne
    farmacia_prod = FarmaciaSerializer()
    
    #Para relaciones ManyToMany
    prov_sum_prod = ProveedorSerializer(read_only=True, many=True)
    
    class Meta:
        fields = ('id', 'imagen_prod', 'nombre_prod', 'descripcion', 'precio', 'stock','farmacia_prod', 'prov_sum_prod')
        model = Producto
        
        
class EmpleadoSerializer(serializers.ModelSerializer):
    
    class Meta:        
        model = Empleado
        fields = '__all__'
    
    
class EmpleadoSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    farm_emp = FarmaciaSerializer()
    usuario = UsuarioSerializer()
    
    #Para formatear fechas si estan heredadas de AbstractUser, se realizan en el campo Usuario
    
    class Meta:
        model = Empleado
        fields = ('id', 'usuario', 'direccion_emp', 'telefono_emp', 'salario', 'farm_emp')
        
class ClienteSerializerMejorado(serializers.ModelSerializer):

    
    #Para relaciones ManyToOne u OneToOne
    usuario = UsuarioSerializer()
    
    #Para relaciones ManyToMany
    productos_favoritos = ProductoSerializerMejorado(read_only=True, many=True)
    votacion_prod = ProductoSerializerMejorado(read_only=True, many=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'
    

class VotacionSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    voto_producto = ProductoSerializerMejorado()
    voto_cliente = ClienteSerializerMejorado()
    
    #Para obtener el valor de un Choice
    puntuacion = serializers.IntegerField(source='get_puntuacion_display')
    
    #Para formatear fechas
    fecha_votacion = serializers.DateField(format=('%d-%m-%Y'))
    
    class Meta:
        model = Votacion
        fields = '__all__'
    
    
class SuministroProductoSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    producto = ProductoSerializerMejorado()
    proveedor = ProveedorSerializer()
    
    class Meta:
        model = SuministroProducto
        fields = '__all__'
    
    
class ProductoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Producto
        fields = ['nombre_prod','descripcion','precio', 'stock', 'farmacia_prod','prov_sum_prod']
            
    def validate_nombre_prod(self,nombre):
        productoNombre = Producto.objects.filter(nombre_prod=nombre, farmacia_prod=self.initial_data['farmacia_prod']).first()
        if(not productoNombre is None):
            if(not self.instance is None and productoNombre.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un producto con ese nombre en esta farmacia.')        
        return nombre
    
    def validate_descripcion(self,descripcion):
        if len(descripcion) < 10:
            raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return descripcion
    
    def validate_precio(self,precio):
        if type(precio) != Decimal:
            raise serializers.ValidationError('El precio introducido no es válido')
        return precio
    
    def validate_stock(self, stock):
        if type(stock) != int or stock < 0:
            raise serializers.ValidationError('El stock introducido no es válido')
        return stock
    
    def create(self, validated_data):
        if('prov_sum_prod' not  in self.initial_data):
            raise serializers.ValidationError(
                {'prov_sum_prod':
                ['No ha enviado proveedores']
                })
        proveedores = self.initial_data['prov_sum_prod']
        if len(proveedores) < 2:
            raise serializers.ValidationError(
                {'prov_sum_prod':
                ['Debe seleccionar al menos dos proveedores.']
                })
        
        imagen_prod = base64.b64decode(self.initial_data["imagen_prod"])
        contenido_archivo = ContentFile(imagen_prod)
        
        archivo = InMemoryUploadedFile(
            contenido_archivo,
            None,
            validated_data["nombre_prod"],
            self.initial_data["formato_imagen"],
            contenido_archivo.size,
            None
        )
        
        producto = Producto.objects.create(
            nombre_prod = validated_data['nombre_prod'],
            descripcion = validated_data['descripcion'],
            precio = validated_data['precio'],
            stock = validated_data['stock'],
            farmacia_prod = validated_data['farmacia_prod'],
            imagen_prod = archivo,
            )

        for proveedor in proveedores:
            modeloProveedor = Proveedor.objects.get(id=proveedor)
            SuministroProducto.objects.create(proveedor=modeloProveedor, producto=producto)
        
        return producto
    
    def update(self, instance, validated_data):
        proveedores = self.initial_data['prov_sum_prod']
        if len(proveedores) < 1:
            raise serializers.ValidationError(
                {'prov_sum_prod':
                ['Debe seleccionar al menos un proveedor']
                })
        
        instance.nombre_prod = validated_data["nombre_prod"]
        instance.descripcion = validated_data["descripcion"]
        instance.precio = validated_data["precio"]
        instance.stock = validated_data["stock"]
        instance.farmacia_prod = validated_data["farmacia_prod"]
        instance.save()
        
        instance.prov_sum_prod.clear()
        for proveedor in proveedores:
            modeloProveedor = Proveedor.objects.get(id=proveedor)
            SuministroProducto.objects.create(proveedor=modeloProveedor, producto=instance)
        return instance
 
   
class ProductoSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre_prod']
        
    def validate_nombre_prod(self, nombre_prod):
        productoNombre = Producto.objects.filter(nombre_prod=nombre_prod).first()
        if(not productoNombre is None and productoNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe un producto con ese nombre')
        return nombre_prod
    
    
    

    
    
class FarmaciaSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Farmacia
        fields = ['nombre_farm','direccion_farm','telefono_farm']
        
    def validate_nombre_farm(self,nombre):
        farmaciaNombre = Farmacia.objects.filter(nombre_farm=nombre).first()
        if(not (farmaciaNombre is None or (not self.instance is None and farmaciaNombre.id == self.instance.id))):
            raise serializers.ValidationError('Ya existe una farmacia con ese nombre.')        
        return nombre
    
    def validate_direccion_farm(self,direccion):
        if len(direccion) < 10:
            raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return direccion
    
    def validate_telefono_farm(self,telefono):
        if (str(telefono)[0] not in ('6','7','9') or len(str(telefono)) != 9):
            raise serializers.ValidationError('Debe especificar un número espanyol de 9 dígitos.')
        return telefono
    
    def update(self, instance, validated_data):
        
        instance.nombre_farm = validated_data["nombre_farm"]
        instance.direccion_farm = validated_data["direccion_farm"]
        instance.telefono_farm = validated_data["telefono_farm"]
        instance.save()
        
        return instance
   
class FarmaciaSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = ['nombre_farm']
        
    def validate_nombre_farm(self, nombre):
        farmaciaNombre = Farmacia.objects.filter(nombre_farm=nombre).first()
        if(not farmaciaNombre is None and farmaciaNombre.id != self.instance.id):
            raise serializers.ValidationError('Ya existe una farmacia con ese nombre')
        return nombre
        
    
    



   
class VotacionSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Votacion
        fields = ['numeros','puntuacion','fecha_votacion','comenta_votacion','voto_producto','voto_cliente']
        
    def validate_comenta_votacion(self,comentario):
        if len(comentario) < 10:
            raise serializers.ValidationError('Al menos debes indicar 10 caracteres')
        return comentario
    
    def validate_voto_producto(self,productoSeleccionado):
        if (productoSeleccionado is None):
            raise serializers.ValidationError('Debe seleccionar un producto a votar.')
        return productoSeleccionado
    
    def validate_voto_cliente(self,clienteVota):
        if (clienteVota is None):
            raise serializers.ValidationError('Debe seleccionar quien realizo la votación.')
        return clienteVota
    
    
    def update(self, instance, validated_data):
        
        instance.puntuacion = validated_data["puntuacion"]
        instance.comenta_votacion = validated_data["comenta_votacion"]
        instance.voto_producto = validated_data["voto_producto"]
        instance.voto_cliente = validated_data["voto_cliente"]
        instance.save()
        
        return instance
   
class VotacionSerializerActualizarPuntuacion(serializers.ModelSerializer):
    class Meta:
        model = Votacion
        fields = ['puntuacion']
    
    
       
class PromocionSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToMany
    cliente_promo = ClienteSerializerMejorado(read_only=True, many=True)
    
    class Meta:
        fields = '__all__'
        model = Promocion
        

class CarritoCompraSerializerMejorado(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    usuario = UsuarioSerializer()
    
    #Para relaciones ManyToMany
    producto_carrito = ProductoSerializerMejorado(read_only=True, many=True)
    
    class Meta:
        fields = '__all__'
        model = CarritoCompra
        
        
class ProductoProspectoSerializerMejorado(serializers.ModelSerializer):
    producto = ProductoSerializerMejorado()

    class Meta:
        fields = '__all__'
        model = Prospecto
        
        
class TratamientoSerializerMejorado(serializers.ModelSerializer):
    cliente = ClienteSerializerMejorado()
    producto = ProductoSerializerMejorado()
        
    class Meta:
        fields = '__all__'
        model = Tratamiento
        
        
   
class TratamientoSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Tratamiento
        fields = ['cliente','producto','veces_al_dia','fecha_inicio','fecha_fin','activo']

            
    def validate_cliente(self,cliente):
        if(cliente is None):
            raise serializers.ValidationError('Necesita aplicar el tratamiento a un cliente.')        
        return cliente
    
    def validate_producto(self,producto):
        if (producto is None):
            raise serializers.ValidationError('Necesita seleccionar un producto para el tratamiento.')
        return producto
    
    def validate_veces_al_dia(self,veces_al_dia):
        if (veces_al_dia is None or veces_al_dia == 0):
            raise serializers.ValidationError('Hay que especificar cuantas veces al dia usa el producto.')
        return veces_al_dia
    
    def validate_fecha_inicio(self, fecha_inicio):
        hoy = date.today()
        if fecha_inicio < hoy:
            raise serializers.ValidationError('Fecha de inicio inválida.')
        fecha_inicio = self.initial_data["fecha_inicio"]
        return fecha_inicio
    
    def validate_fecha_fin(self, fecha_fin):
        
        hoy = date.today()
        if fecha_fin <= hoy:
            raise serializers.ValidationError('Fecha de fin inválida.')

        fecha_fin = self.initial_data["fecha_inicio"]
        return fecha_fin

    
    def create(self, validated_data):        
        
        tratamiento = Tratamiento.objects.create(
            cliente = validated_data['cliente'],
            producto = validated_data['producto'],
            veces_al_dia = validated_data['veces_al_dia'],
            fecha_inicio = validated_data['fecha_inicio'],
            fecha_fin = validated_data['fecha_fin'],
            activo = self.initial_data['activo'],
            )

        return tratamiento