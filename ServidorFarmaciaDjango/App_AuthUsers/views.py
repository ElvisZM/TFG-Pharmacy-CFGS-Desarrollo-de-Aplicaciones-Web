from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from .forms import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from oauth2_provider.models import AccessToken
from datetime import date, timedelta


class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        
        if serializers.is_valid():
            try:
                rol = int(request.data.get('rol'))
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"),
                        first_name = serializers.data.get("first_name"),
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Cliente') 
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create( usuario = user, direccion_cli = serializers.data.get("domicilio"), telefono_cli = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    cliente.save()
                    
                elif(rol == Usuario.EMPLEADO):
                    grupo = Group.objects.get(name='Empleado') 
                    grupo.user_set.add(user)
                    empleado = Empleado.objects.create( usuario = user, direccion_emp = serializers.data.get("domicilio"), telefono_emp = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    empleado.save()
                
                elif(rol == Usuario.GERENTE):
                    grupo = Group.objects.get(name='Gerente') 
                    grupo.user_set.add(user)
                    gerente = Gerente.objects.create( usuario = user, direccion_ger = serializers.data.get("domicilio"), telefono_ger = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    gerente.save()
                    
                elif(rol == Usuario.ADMINISTRADOR):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    cliente = Administrador.objects.create( usuario = user, direccion_admin = serializers.data.get("domicilio"), telefono_admin = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    cliente.save()
                    
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

def obtener_usuario_token(request,token):
    
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)
    