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
    if(request.user.has_perm('App_ProductProvider.add_producto')):
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
                    return Response('Uno o más productos ya existen en esa farmacia o la farmacia no existe.', status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response('Producto CREADO', status=status.HTTP_200_OK)

        else:
            return Response('Se esperaba una lista de objetos JSON', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    else:
        return Response('Sin permisos para esta operación', status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def productos_list(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def farmacias_list(request):
    farmacias = Farmacia.objects.all()
    serializer = FarmaciaSerializer(farmacias, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def proveedores_list(request):
    proveedores = Proveedor.objects.all()
    serializer = ProveedorSerializer(proveedores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def categorias_list(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaProductoSerializer(categorias, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def suministro_productos_list(request):
    suministro = SuministroProducto.objects.all()
    serializer = SuministroProductoSerializer(suministro, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def producto_buscar(request):
    formulario = BusquedaProductoForm(request.query_params)
    if (formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
        productos = productos.filter(Q(nombre_prod__contains=texto) | Q(descripcion__contains=texto)).all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def producto_editar(request, codigo_nacional_prod):
    if(request.user.has_perm("App_ProductProvider.change_producto")):
        producto = Producto.objects.get(cn_prod=codigo_nacional_prod)
        productoCreateSerializer = ProductoSerializerCreate(instance=producto, data=request.data)
        if productoCreateSerializer.is_valid():
            try:
                productoCreateSerializer.save()
                return Response("Producto EDITADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        else:
            return Response(productoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def producto_obtener(request, cn_prod):
    producto = Producto.objects.get(cn_prod=cn_prod)
    serializer = ProductoSerializer(producto)
    return Response(serializer.data)