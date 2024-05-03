from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .forms import *

@api_view(['POST'])
def producto_create(request):
    if(request.user.has_perm('App_Farmacia.add_producto')):
        producto_serializers = ProductoSerializerCreate(data=request.data)
        if producto_serializers.is_valid():
            try:
                producto_serializers.save()
                return Response('Producto CREADO')
            
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(f'Error creando producto:\n{error}')
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(producto_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Sin permisos para esta operación', status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])   
def registrar_producto_csv(request):
    if(request.user.has_perm('App_Farmacia.add_producto')):
        print("hola csv")

