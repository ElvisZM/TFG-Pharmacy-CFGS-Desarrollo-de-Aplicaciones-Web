from django.shortcuts import render
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .forms import *
from rest_framework.permissions import AllowAny


@api_view(['POST'])
def producto_create(request):
    if(request.user.is_authenticated and request.user.has_perm('App_ProductProvider.add_producto')):
        if request.method == 'POST':
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
            return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response('Usuario no autenticado o Sin permisos para esta operación', status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])   
def registrar_producto_csv(request):
    if(request.user.is_authenticated and request.user.has_perm('App_ProductProvider.add_producto')):
        if(request.method == 'POST'):
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
            return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
    else:
        return Response('Usuario no autenticado o Sin permisos para esta operación', status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def productos_list(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def farmacias_list(request):
    if request.method == 'GET':
        farmacias = Farmacia.objects.all()
        serializer = FarmaciaSerializer(farmacias, many=True)
        return Response(serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def proveedores_list(request):
    if request.method == 'GET':
        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def categorias_list(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaProductoSerializer(categorias, many=True)
        return Response(serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def suministro_productos_list(request):
    if request.user.is_authenticated and request.user.has_perm('App_ProductProvider.view_suministroproducto'):
        if request.method == 'GET':
            suministro = SuministroProducto.objects.all()
            serializer = SuministroProductoSerializer(suministro, many=True)
            return Response(serializer.data)

        else:
            return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response('Sin permisos para esta operación', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def producto_editar(request, cn_prod):
    if(request.user.is_authenticated and request.user.has_perm("App_ProductProvider.change_producto")):
        if request.method == "PUT":
            producto = Producto.objects.get(cn_prod=cn_prod)
            productoCreateSerializer = ProductoSerializerCreate(instance=producto, data=request.data, partial=True)
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
            return Response("Metodo no permitido", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response("Usuario no autenticado o Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def producto_eliminar(request, cn_prod, cif_farm):
    if(request.user.is_authenticated and request.user.has_perm("App_ProductProvider.delete_producto")):
        if request.method == 'DELETE':
            producto = Producto.objects.get(cn_prod=cn_prod, cif_farm=cif_farm)
            try:
                producto.delete()
                return Response("Producto ELIMINADO")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response("Metodo no permitido", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response("Usuario no autenticado o Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def producto_obtener(request, cn_prod, cif_farm):
    if request.method == 'GET':
        try:
            producto = Producto.objects.get(cn_prod=cn_prod, cif_farm=cif_farm)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            return Response("Producto no encontrado")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def categoria_obtener(request, id):
    if request.method == 'GET':
        categoria = Categoria.objects.get(id=id)
        serializer = CategoriaProductoSerializer(categoria)
        return Response(serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def provider_obtener(request, cif_prov):
    if request.method == 'GET':
        provider = Proveedor.objects.get(cif_prov=cif_prov)
        serializer = ProveedorSerializer(provider)
        return Response(serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def farmacia_obtener(request, cif_farm):
    if request.method == 'GET':
        farmacia = Farmacia.objects.get(cif_farm=cif_farm)
        serializer = FarmaciaSerializer(farmacia)
        return Response(serializer.data)
    
    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def helper_cif_prov(request, nombre_prov):
    proveedor = Proveedor.objects.get(nombre_prov=nombre_prov)
    serializer = ProveedorSerializer(proveedor)
    return Response(serializer.data)


@api_view(['GET'])
def helper_id_cat(request, nombre_cat):
    categoria = Categoria.objects.get(nombre_cat=nombre_cat)
    serializer = CategoriaProductoSerializer(categoria)
    return Response(serializer.data)


@api_view(['GET'])
def productos_buscador_simple(request, busqueda):
    if request.method == 'GET':
        data = {'textoBusqueda': busqueda}
        formulario = BusquedaProductoForm(data)
        if (formulario.is_valid()):
            texto = formulario.cleaned_data['textoBusqueda'].lower().strip()
            
            productos = Producto.objects.all()

            try:
                numero_busqueda = int(texto)

                productos = productos.filter(cn_prod=numero_busqueda)
            except ValueError:

                productos = productos.filter(Q(nombre_prod__icontains=texto)).all()
            
            serializer = ProductoSerializer(productos, many=True)
            return Response(serializer.data)
        else:
            
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
def productos_recomendados(request, nombre_cat):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat=nombre_cat).first()
        productos_recomendados = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos_recomendados, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def productos_cat_analgesicos(request):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat="Analgesicos").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def productos_cat_antiacidos(request):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat="Antiacidos").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def productos_cat_antialergicos(request):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat="Antialergicos").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def productos_cat_antisepticos(request):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat="Antisepticos").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def productos_cat_hipolipemiantes(request):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat="Hipolipemiantes").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def productos_cat_asma(request):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat="Asma").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def productos_cat_vitaminas(request):
    if request.method == 'GET':
        categoria = Categoria.objects.filter(nombre_cat="Vitaminas").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def productos_cat_corticosteroides(request):
    if request.method=='GET':
        categoria = Categoria.objects.filter(nombre_cat="Corticosteroides").first()
        productos = Producto.objects.filter(categoria_id=categoria)
        productos_serializer = ProductoSerializer(productos, many=True)
        return Response(productos_serializer.data)

    else:
        return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
