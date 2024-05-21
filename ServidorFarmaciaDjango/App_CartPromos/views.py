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
def agregar_al_carrito(request, producto_id):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            producto_anyadir = Producto.objects.get(id=producto_id)
        
            carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, finalizado=False).first()
            
            
            if (carrito_usuario):
                producto_carrito = ContenidoCarrito.objects.select_related("carrito_id", "producto_id").filter(carrito_id = carrito_usuario, producto_id = producto_anyadir)
                if (producto_carrito):                    
                    producto_aumentar = ContenidoCarrito.objects.get(carrito_id=carrito_usuario, producto = producto_anyadir)
                    producto_aumentar.cantidad_producto += 1
                    producto_aumentar.save()
                else:
                    ContenidoCarrito.objects.create(carrito_id=carrito_usuario, producto = producto_anyadir, cantidad_producto=1)

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
def carrito_usuario(request):
    if(request.user.is_authenticated):
        
        try:
            carrito_usuario = CarritoCompra.objects.get(usuario=request.user, realizado=False) 
            serializer = CarritoCompraSerializer(carrito_usuario)
            serializer = serializer.data
            total_carrito = 0
            for detalle_producto in carrito_usuario.contenidocarrito_set.all():
                precio_producto = detalle_producto.producto.precio
                cantidad_producto = detalle_producto.cantidad_producto
                total_carrito += cantidad_producto * precio_producto
            
            serializer['total_carrito'] = total_carrito
            
            return Response(serializer)
        
        except CarritoCompra.DoesNotExist:
            CarritoCompra.objects.create(usuario=request.user, realizado=False)
            carrito_usuario = CarritoCompra.objects.get(usuario=request.user, realizado=False)
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
        
                carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, realizado=False).first()
                
                
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
        
                carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, realizado=False).first()
                
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

