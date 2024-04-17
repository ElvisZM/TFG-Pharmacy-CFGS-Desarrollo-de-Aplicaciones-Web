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
        

class UsuarioSerializer(serializers.ModelSerializer):
    
    date_joined = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    last_login = serializers.DateTimeField(format=('%d-%m-%Y'))
    
    class Meta:
        model = Usuario
        fields = '__all__'
