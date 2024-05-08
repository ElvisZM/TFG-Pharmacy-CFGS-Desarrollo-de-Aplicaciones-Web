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
    if(request.user.is_authenticated and request.user.has_perm('App_ProductProvider.add_producto')):
        csv_data = request.data
        
        if isinstance(csv_data, list):
            for item in csv_data[:-1]:
        
                producto_serializers = CsvProductoSerializerCreate(data=item)
                try:
                    if producto_serializers.is_valid():
                        try:
                            producto_serializers.save()
                        except serializers.ValidationError as error:
                            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
                        except Exception as error:
                            print(error)
                            return Response(error.detail, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except serializers.ValidationError as error:
                    return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
                
                except Exception as err:
                    return Response(err, status=status.HTTP_400_BAD_REQUEST)
                
            if (producto_serializers.errors):
                if(len(producto_serializers.errors) ==1 and producto_serializers.errors['nombre_prod']):
                    return Response('Uno o más productos ya existen en esa farmacia', status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response('Producto CREADO', status=status.HTTP_200_OK)

        else:
            return Response('Se esperaba una lista de objetos JSON', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Sin permisos para esta operación', status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def productos_list(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def proveedores_list(request):
    proveedores = Proveedor.objects.all()
    serializer = ProveedorSerializer(proveedores, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def suministro_productos_list(request):
    suministro = SuministroProducto.objects.all()
    serializer = SuministroProductoSerializer(suministro, many=True)
    return Response(serializer.data)