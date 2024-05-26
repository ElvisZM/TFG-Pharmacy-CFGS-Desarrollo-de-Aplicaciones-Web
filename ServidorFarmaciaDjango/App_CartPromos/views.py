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
from oauth2_provider.models import AccessToken




@api_view(['POST'])
def agregar_al_carrito(request, producto_id):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            producto_anyadir = Producto.objects.get(id=producto_id)
        
            carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, finalizado=False).first()
            
            
            if (carrito_usuario):
                producto_carrito = ContenidoCarrito.objects.select_related("carrito_id", "producto_id").filter(carrito_id = carrito_usuario, producto_id = producto_anyadir)
                if (producto_carrito):                    
                    producto_aumentar = ContenidoCarrito.objects.get(carrito_id=carrito_usuario, producto_id = producto_anyadir)
                    producto_aumentar.cantidad_producto += 1
                    producto_aumentar.save()
                else:
                    ContenidoCarrito.objects.create(carrito_id=carrito_usuario, producto_id = producto_anyadir, cantidad_producto=1)

            else:
                CarritoCompra.objects.create(usuario=request.user, finalizado=False)
                carrito_usuario = CarritoCompra.objects.get(usuario = request.user, realizado=False)
                ContenidoCarrito.objects.create(carrito_id=carrito_usuario, producto_id = producto_anyadir,cantidad_producto = 1)
            
            return Response({"Producto agregado al carrito correctamente"}, status=status.HTTP_200_OK)
        
        else:
            return Response('Metodo no permitido', status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
@permission_classes([AllowAny])
def carrito_usuario(request):
    if(request.user.is_authenticated):
        
        try:
            
            carrito_usuario = CarritoCompra.objects.get(usuario=request.user, finalizado=False) 
            serializer = CarritoCompraSerializer(carrito_usuario)
            serializer = serializer.data
            
            
            total_carrito = 0
            cantidad_prod_carrito = 0
            for detalle_producto in carrito_usuario.contenidocarrito_set.all():
                precio_producto = detalle_producto.producto_id.precio
                cantidad_producto = detalle_producto.cantidad_producto
                total_carrito += cantidad_producto * precio_producto
                cantidad_prod_carrito += cantidad_producto
            
            serializer['total_carrito'] = total_carrito
            serializer['cantidad_productos_total'] = cantidad_prod_carrito
            
             # Obtenemos todas las categorías de los productos en el carrito
            categorias_carrito = set([producto.producto_id.categoria_id for producto in carrito_usuario.contenidocarrito_set.all()])
            
            # Lista para almacenar los productos recomendados
            productos_recomendados = []
            
            # Obtenemos un producto recomendado de cada categoría en el carrito
            for categoria in categorias_carrito:
                producto_recomendado = Producto.objects.filter(categoria_id=categoria).exclude(id__in=[producto.producto_id.id for producto in carrito_usuario.contenidocarrito_set.all()]).first()
                if producto_recomendado:
                    productos_recomendados.append(producto_recomendado)
            
            # Serializamos los productos recomendados y los agregamos a la respuesta
            serializer_productos_recomendados = ProductoSerializer(productos_recomendados, many=True)
            serializer['productos_recomendados'] = serializer_productos_recomendados.data
            
            
            return Response(serializer)
        
        except CarritoCompra.DoesNotExist:
            CarritoCompra.objects.create(usuario=request.user, finalizado=False)
            carrito_usuario = CarritoCompra.objects.get(usuario=request.user, finalizado=False)
            serializer=CarritoCompraSerializer(carrito_usuario)
            return Response(serializer.data)
        
    else:
        return Response("Necesita iniciar sesion", status=status.HTTP_405_METHOD_NOT_ALLOWED)        
        

@api_view(['DELETE'])
def quitar_del_carrito(request, producto_id):
    if(request.user.is_authenticated):
        if request.method == 'DELETE':
            try:
                producto_eliminar = Producto.objects.get(id=producto_id)
        
                carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, finalizado=False).first()
                
                
                ContenidoCarrito.objects.select_related("carrito_id", "producto_id").filter(carrito_id = carrito_usuario, producto_id = producto_eliminar).delete()

                return Response({"Producto eliminado del carrito correctamente"}, status=status.HTTP_200_OK)
            
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def bajar_unidad_carrito(request, producto_id):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            try:
                producto_bajar_ud = Producto.objects.get(id=producto_id)
        
                carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, finalizado=False).first()
                
                producto_carrito = ContenidoCarrito.objects.select_related("carrito_id", "producto_id").filter(carrito_id = carrito_usuario, producto_id = producto_bajar_ud).first()
                
                if (producto_carrito and producto_carrito.cantidad_producto > 1):
                    producto_carrito.cantidad_producto -= 1
                    producto_carrito.save()
                    
                else:
                    producto_carrito.delete()
                    
                return Response({"Se ha quitado una unidad del producto correctamente"}, status=status.HTTP_200_OK)
            
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

