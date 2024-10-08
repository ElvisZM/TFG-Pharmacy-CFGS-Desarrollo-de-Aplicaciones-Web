from django.shortcuts import render
import requests
import urllib.parse
from django.contrib.auth import authenticate
from django.http import JsonResponse
import jwt
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
from oauth2_provider.models import AccessToken, Application
from django.conf import settings
from datetime import date, timedelta
import numpy as np


class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
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
                        cliente = Cliente.objects.create( usuario = user, source='app',direccion_cli = serializers.data.get("domicilio"), telefono_cli = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                        cliente.save()
                        
                    elif(rol == Usuario.EMPLEADO):
                        grupo = Group.objects.get(name='Empleado') 
                        grupo.user_set.add(user)
                        empleado = Empleado.objects.create( usuario = user, source='app', direccion_emp = serializers.data.get("domicilio"), telefono_emp = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                        empleado.save()
                    
                    elif(rol == Usuario.GERENTE):
                        grupo = Group.objects.get(name='Gerente') 
                        grupo.user_set.add(user)
                        gerente = Gerente.objects.create( usuario = user, source='app', direccion_ger = serializers.data.get("domicilio"), telefono_ger = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                        gerente.save()
                        
                    elif(rol == Usuario.ADMINISTRADOR):
                        grupo = Group.objects.get(name='Administrador') 
                        grupo.user_set.add(user)
                        administrador = Administrador.objects.create( usuario = user, source='app', direccion_admin = serializers.data.get("domicilio"), telefono_admin = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                        administrador.save()
                        
                    usuarioSerializado = UsuarioSerializer(user)
                    return Response(usuarioSerializado.data)
                except Exception as error:
                    return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def obtener_usuario_token(request,token):
    
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    if (usuario.is_superuser):
        usuario.first_name = 'Administrador'
        usuario.rol=1
        usuario.save()
    usuario_serializer = UsuarioSerializer(usuario)
    data_user = usuario_serializer.data
    
    try:
        if data_user['rol'] == 1:
            admin_data = Administrador.objects.all()
            admin_data = admin_data.get(usuario_id=data_user['id'])
            administrador_serializer = AdministradorSerializer(admin_data)
            
            response_data = {"usuario": data_user, "administrador":administrador_serializer.data}
        
        elif data_user['rol'] == 2:
            cliente_data = Cliente.objects.get(usuario=data_user['id'])
            cliente_serializer = ClienteSerializer(cliente_data)
                
            response_data = {"usuario": data_user, "cliente":cliente_serializer.data}
        
        elif data_user['rol'] == 3:
            empleado_data = Empleado.objects.get(usuario=data_user['id'])
            empleado_serializer = EmpleadoSerializer(empleado_data)
            
            response_data = {"usuario": data_user, "empleado":empleado_serializer.data}
        
        elif data_user['rol'] == 4:
            gerente_data = Gerente.objects.get(usuario=data_user['id'])
            gerente_serializer = GerenteSerializer(gerente_data)
            
            response_data = {"usuario": data_user, "gerente":gerente_serializer.data}
        
        else:
            return Response('Invalid')
    
    except Administrador.DoesNotExist as error:
        if data_user['rol'] == 1:
            grupo = Group.objects.get(name='Administrador') 
            grupo.user_set.add(usuario)
            administrador = Administrador.objects.create( usuario = usuario, source='app')
            administrador.save()
            
            administrador_serializer = AdministradorSerializer(administrador)

            response_data = {"usuario": data_user, "administrador":administrador_serializer.data}   

    return Response(response_data)

class registrar_usuario_google(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistroGoogle
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        default_birthday_date = date(2000, 1, 1)
        self.request.data['birthday_date'] = default_birthday_date
        serializers = UsuarioSerializerRegistroGoogle(data=request.data)
        num_aleatorios = list(map(str, np.random.randint(1,10,5)))
        self.request.data['username'] = self.request.data['first_name']+''.join(num_aleatorios)
        try:
            if serializers.is_valid():
                try:
                    
                    comprobar_usuario_existente = Usuario.objects.filter(email=serializers.data.get('email')).first()

                    rol = serializers.data.get('rol')
                    
                    token_expiration = timezone.now() + timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
                    aplicacion = Application.objects.all().first()                    
                    
                    if comprobar_usuario_existente:
                        
                        if comprobar_usuario_existente.first_name == serializers.data.get('first_name'):
                            AccessToken.objects.create(token=self.request.data['token'], expires=token_expiration, scope="read write groups", application_id=aplicacion.id, user_id=comprobar_usuario_existente.id, created=datetime.datetime.now(), updated=datetime.datetime.now())
                            
                            if serializers.data.get('rol') == 2:
                                cliente = Cliente.objects.get(usuario=comprobar_usuario_existente)
                                cliente_serializer = ClienteSerializer(cliente)
                            
                                return Response(cliente_serializer.data, status=status.HTTP_200_OK)
                        
                        
                            elif serializers.data.get('rol') == 1:
                                administrador = Administrador.objects.get(usuario=comprobar_usuario_existente)
                                administrador_serializer = AdministradorSerializer(administrador)
                            
                                return Response(administrador_serializer.data, status=status.HTTP_200_OK)
                        
                        
                            elif serializers.data.get('rol') == 3:
                                empleado = Empleado.objects.get(usuario=comprobar_usuario_existente)
                                empleado_serializer = EmpleadoSerializer(empleado)
                            
                                return Response(empleado_serializer.data, status=status.HTTP_200_OK)
                        
                        
                            else:
                                gerente = Gerente.objects.get(usuario=comprobar_usuario_existente)
                                gerente_serializer = GerenteSerializer(gerente)
                            
                                return Response(gerente_serializer.data, status=status.HTTP_200_OK)
                        
                        else:
                            return Response('El email ya existe en otro usuario', status=status.HTTP_400_BAD_REQUEST)
                        
                    user = Usuario.objects.create_user(
                            username= serializers.data.get('username'),
                            first_name = serializers.data.get("first_name"),
                            last_name = serializers.data.get("last_name"),
                            email = serializers.data.get("email"), 
                            rol = rol,
                            )
                    
                    AccessToken.objects.create(token=self.request.data['token'], expires=token_expiration, scope="read write groups", application_id=aplicacion.id, user_id=user.id, created=datetime.datetime.now(), updated=datetime.datetime.now())
                    
                    
                    if(rol == Usuario.CLIENTE):
                        grupo = Group.objects.get(name='Cliente') 
                        grupo.user_set.add(user)
                        cliente = Cliente.objects.create( usuario = user, source='google', profile_pic = request.data["profile_pic"], direccion_cli = None, telefono_cli = None, birthday_date = serializers.data.get('birthday_date'))
                        cliente.save()
                        
                    elif(rol == Usuario.EMPLEADO):
                        grupo = Group.objects.get(name='Empleado') 
                        grupo.user_set.add(user)
                        empleado = Empleado.objects.create( usuario = user, source='google', profile_pic = request.data["profile_pic"], direccion_emp = None, telefono_emp = None, birthday_date = serializers.data.get('birthday_date'))
                        empleado.save()
                    
                    elif(rol == Usuario.GERENTE):
                        grupo = Group.objects.get(name='Gerente') 
                        grupo.user_set.add(user)
                        gerente = Gerente.objects.create( usuario = user, source='google', profile_pic = request.data["profile_pic"], direccion_ger = None, telefono_ger = None, birthday_date = serializers.data.get('birthday_date'))
                        gerente.save()
                        
                    elif(rol == Usuario.ADMINISTRADOR):
                        grupo = Group.objects.get(name='Administrador') 
                        grupo.user_set.add(user)
                        administrador = Administrador.objects.create( usuario = user, source='google', profile_pic = request.data["profile_pic"], direccion_admin = None, telefono_admin = None, birthday_date = serializers.data.get('birthday_date'))
                        administrador.save()
                        
                    usuarioSerializado = UsuarioSerializer(user)
                    return Response('Usuario registrado con exito', status=status.HTTP_200_OK)
                except Exception as error:
                    return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except serializers.ValidationError as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(repr(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class registrar_usuario_facebook(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistroFacebook
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        default_birthday_date = date(2000, 1, 1)
        self.request.data['birthday_date'] = default_birthday_date
        
        self.request.data['first_name'], *apellidos = self.request.data['first_name'].split(maxsplit=1)
        
        self.request.data['last_name'] = ' '.join(apellidos)
        
        num_aleatorios = list(map(str, np.random.randint(1,10,5)))
        self.request.data['username'] = self.request.data['first_name']+''.join(num_aleatorios)
        
        serializers = UsuarioSerializerRegistroFacebook(data=request.data)

        try:
            if serializers.is_valid():
                try:
                    
                    comprobar_usuario_existente = Usuario.objects.filter(email=serializers.data.get('email')).first()

                    rol = serializers.data.get('rol')
                    
                    token_expiration = timezone.now() + timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
                    aplicacion = Application.objects.all().first()                    
                    if comprobar_usuario_existente:
                        
                        if comprobar_usuario_existente.first_name == serializers.data.get('first_name'):
                            AccessToken.objects.create(token=self.request.data['token'], expires=token_expiration, scope="read write groups", application_id=aplicacion.id, user_id=comprobar_usuario_existente.id, created=datetime.datetime.now(), updated=datetime.datetime.now())
                        
                            if serializers.data.get('rol') == 2:
                                cliente = Cliente.objects.get(usuario=comprobar_usuario_existente)
                                cliente_serializer = ClienteSerializer(cliente)
                            
                                return Response(cliente_serializer.data, status=status.HTTP_200_OK)
                        
                        
                            elif serializers.data.get('rol') == 1:
                                administrador = Administrador.objects.get(usuario=comprobar_usuario_existente)
                                administrador_serializer = AdministradorSerializer(administrador)
                            
                                return Response(administrador_serializer.data, status=status.HTTP_200_OK)
                        
                        
                            elif serializers.data.get('rol') == 3:
                                empleado = Empleado.objects.get(usuario=comprobar_usuario_existente)
                                empleado_serializer = EmpleadoSerializer(empleado)
                            
                                return Response(empleado_serializer.data, status=status.HTTP_200_OK)
                        
                        
                            else:
                                gerente = Gerente.objects.get(usuario=comprobar_usuario_existente)
                                gerente_serializer = GerenteSerializer(gerente)
                            
                                return Response(gerente_serializer.data, status=status.HTTP_200_OK)
                        
                        else:
                        
                            return Response('El email ya existe en otro usuario', status=status.HTTP_400_BAD_REQUEST)
                    
                    
                    user = Usuario.objects.create_user(
                            username= serializers.data.get('username'),
                            first_name = serializers.data.get("first_name"),
                            last_name = serializers.data.get("last_name"),
                            email = serializers.data.get("email"), 
                            rol = rol,
                            )
                    
                    AccessToken.objects.create(token=self.request.data['token'], expires=token_expiration, scope="read write groups", application_id=aplicacion.id, user_id=user.id, created=datetime.datetime.now(), updated=datetime.datetime.now())
                    
                    
                    if(rol == Usuario.CLIENTE):
                        grupo = Group.objects.get(name='Cliente') 
                        grupo.user_set.add(user)
                        cliente = Cliente.objects.create( usuario = user, source='facebook', profile_pic = request.data["profile_pic"], direccion_cli = None, telefono_cli = None, birthday_date = serializers.data.get('birthday_date'))
                        cliente.save()
                        
                    elif(rol == Usuario.EMPLEADO):
                        grupo = Group.objects.get(name='Empleado') 
                        grupo.user_set.add(user)
                        empleado = Empleado.objects.create( usuario = user, source='facebook', profile_pic = request.data["profile_pic"], direccion_emp = None, telefono_emp = None, birthday_date = serializers.data.get('birthday_date'))
                        empleado.save()
                    
                    elif(rol == Usuario.GERENTE):
                        grupo = Group.objects.get(name='Gerente') 
                        grupo.user_set.add(user)
                        gerente = Gerente.objects.create( usuario = user, source='facebook', profile_pic = request.data["profile_pic"], direccion_ger = None, telefono_ger = None, birthday_date = serializers.data.get('birthday_date'))
                        gerente.save()
                        
                    elif(rol == Usuario.ADMINISTRADOR):
                        grupo = Group.objects.get(name='Clientes') 
                        grupo.user_set.add(user)
                        administrador = Administrador.objects.create( usuario = user, source='facebook', profile_pic = request.data["profile_pic"], direccion_admin = None, telefono_admin = None, birthday_date = serializers.data.get('birthday_date'))
                        administrador.save()
                        
                    usuarioSerializado = UsuarioSerializer(user)
                    return Response("Usuario Creado", status=status.HTTP_200_OK)
                except Exception as error:
                    return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except serializers.ValidationError as error:
            return Response('Inicio de sesión en FB correcto', status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response(repr(err), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
