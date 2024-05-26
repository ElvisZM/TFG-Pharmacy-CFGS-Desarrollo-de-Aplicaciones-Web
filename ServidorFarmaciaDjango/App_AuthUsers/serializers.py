from rest_framework import serializers
from .models import *
from .forms import *
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from App_ProductProvider.serializers import *




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
            raise serializers.ValidationError('Usuario existente.')
        return username
    
    def validate_email(self, email):
        email_existe = Usuario.objects.filter(email=email).first()
        if (not email_existe is None):
            raise serializers.ValidationError('Email ya en uso.')
        return email
    
    def validate_telefono(self, telefono):
        administradorTelefono = Administrador.objects.filter(telefono_admin=telefono).first()    
        gerenteTelefono = Gerente.objects.filter(telefono_ger=telefono).first()
        empleadoTelefono = Empleado.objects.filter(telefono_emp=telefono).first()
        clienteTelefono = Cliente.objects.filter(telefono_cli=telefono).first()    

        if (str(telefono)[0] not in ('6','7','9') or len(str(telefono)) != 9) or (not(administradorTelefono is None or gerenteTelefono is None or empleadoTelefono is None or clienteTelefono is None)):
            raise serializers.ValidationError('Teléfono inválido o en uso.')

        return telefono
        

class UsuarioSerializer(serializers.ModelSerializer):
    
    date_joined = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    last_login = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    class Meta:
        model = Usuario
        fields = '__all__'
        
        

class UsuarioSerializerRegistroGoogle(serializers.Serializer):
    
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField(required=False, allow_blank=True)
    password2 = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    domicilio = serializers.CharField(required=False, allow_blank=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    birthday_date = serializers.DateField()
    
    def validate_username(self, username):
        if username is None:
            raise serializers.ValidationError('Nombre de usuario necesario')
        return username
    
    def validate_email(self, email):
        if email is None:
            raise serializers.ValidationError('Email inexistente')
        return email


class AdministradorSerializer(serializers.ModelSerializer):
    
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Administrador
        fields = '__all__'
        
        
class ClienteSerializer(serializers.ModelSerializer):
    
    #Para relaciones ManyToOne u OneToOne
    usuario = UsuarioSerializer()
    
    #Para relaciones ManyToMany
    productos_favoritos = ProductoSerializer(read_only=True, many=True)
    votacion_prod = ProductoSerializer(read_only=True, many=True)
    
    class Meta:
        model = Cliente
        fields = ['id', 'usuario', 'profile_pic', 'direccion_cli', 'telefono_cli', 'birthday_date', 'productos_favoritos', 'votacion_prod']
        
        
class EmpleadoSerializer(serializers.ModelSerializer):
    
    usuario = UsuarioSerializer()
    farm_id = FarmaciaSerializer()
    
    class Meta:
        model = Empleado
        fields = '__all__'
        
        
class GerenteSerializer(serializers.ModelSerializer):
    
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Gerente
        fields = '__all__'
        
        
        

class UsuarioSerializerRegistroFacebook(serializers.Serializer):
    
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField(required=False, allow_blank=True)
    password2 = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    rol = serializers.IntegerField()
    domicilio = serializers.CharField(required=False, allow_blank=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    birthday_date = serializers.DateField()
    
    def validate_username(self, username):
        if username is None:
            raise serializers.ValidationError('Nombre de usuario necesario')
        return username
    
    def validate_email(self, email):
        if email is None:
            raise serializers.ValidationError('Email inexistente')
        return email