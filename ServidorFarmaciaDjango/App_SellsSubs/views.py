from django.shortcuts import render
from .models import *

from .serializers import *
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from oauth2_provider.models import AccessToken, Application


@api_view(['POST'])
def save_payment(request):
    if (request.user.is_authenticated):
        if (request.method == 'POST'):
            try:
                compra_data={
                   "fecha_compra": request.data['fecha_compra'],
                   "direccion_envio": request.data['direccion_envio'],
                   "codigo_postal": request.data['codigo_postal'],
                   "municipio": request.data['municipio'],
                   "provincia": request.data['provincia'],
                   "total_pago": request.data['total_pago'],
                }
                
                if request.data['tipo_pago'] == 'creditcard':
                    pago_data={
                    "tipo_pago": request.data['tipo_pago'],
                    "titular_tarjeta": request.data['titular_tarjeta'],
                    "numero_tarjeta": request.data['numero_tarjeta'],
                    "tipo_tarjeta": request.data['tipo_tarjeta'],
                    "fecha_pago": request.data['fecha_pago'],
                    }
                    pago_serializer = PagoSerializerCreditCard(data=pago_data)
                
                elif request.data['tipo_pago'] == 'paypal':
                    
                    pago_data={
                    "tipo_pago": request.data['tipo_pago'],
                    "id_transaccion": request.data['id_transaccion'],
                    "paypal_email_transaccion": request.data['email_transaccion'],
                    "fecha_pago": request.data['fecha_pago'],
                    }
                    pago_serializer = PagoSerializerPayPal(data=pago_data)
                    
                else:
                    return Response('Tipo de pago no valido', status=status.HTTP_400_BAD_REQUEST)
                
                compra_serializer = CompraSerializer(data=compra_data)
                
                if pago_serializer.is_valid() and compra_serializer.is_valid():
                    cliente = Cliente.objects.get(usuario = request.data['cliente'])
                    carrito = CarritoCompra.objects.get(codigo_compra = request.data['carrito'])
                    
                    compra_creada = Compra.objects.create(fecha_compra=compra_serializer.data['fecha_compra'], direccion_envio=compra_serializer.data['direccion_envio'],
                    codigo_postal = compra_serializer.data['codigo_postal'],
                    municipio = compra_serializer.data['municipio'],
                    provincia= compra_serializer.data['provincia'],
                    total_pago=compra_serializer.data['total_pago'],
                    cliente_id=cliente,
                    carrito_id=carrito                    
                    )

                    if request.data['tipo_pago'] == 'creditcard':
                        pago_realizado = Pago.objects.create(
                            tipo_pago=pago_serializer.data['tipo_pago'],
                            titular_tarjeta =pago_serializer.data['titular_tarjeta'],
                            numero_tarjeta=pago_serializer.data['numero_tarjeta'],
                            tipo_tarjeta=pago_serializer.data['tipo_tarjeta'],
                            id_transaccion=None,
                            paypal_email_transaccion=None,
                            fecha_pago=pago_serializer.data['fecha_pago'],
                            cliente_id = cliente,
                            compra_id = compra_creada
                            )
                        
                    else:
                        pago_realizado = Pago.objects.create(
                            tipo_pago=pago_serializer.data['tipo_pago'],
                            titular_tarjeta =None,
                            numero_tarjeta=None,
                            tipo_tarjeta=None,
                            id_transaccion=pago_serializer.data['id_transaccion'],
                            paypal_email_transaccion=pago_serializer.data['paypal_email_transaccion'],
                            fecha_pago=pago_serializer.data['fecha_pago'],
                            cliente_id = cliente,
                            compra_id = compra_creada
                            )
                    
                    carrito.finalizado=True
                    carrito.save()
                    
                    contenido_carrito = ContenidoCarrito.objects.filter(carrito_id=carrito).all()
                    
                    for item in contenido_carrito:
                        producto = item.producto_id
                        producto.stock -= item.cantidad_producto
                        producto.ventas += item.cantidad_producto
                        producto.save()
                    
                    return Response("Compra registrada correctamente", status=status.HTTP_200_OK)
                
                else:
                    errors = {**pago_serializer.errors, **compra_serializer.errors}
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)  
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Metodo no permitido', status=status.HTTP_405_BAD_REQUEST)
        
    else:
        return Response('Necesita iniciar sesion', status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])        
def create_review(request):
    if (request.user.is_authenticated):
        if request.method == 'POST':
            try:
                cliente = Cliente.objects.get(usuario=request.user.id)
                producto_review = Producto.objects.get(id=request.data['producto_id'])
                
                datos = request.data
                serializer = ReviewSerializerCreate(data=datos)
                if serializer.is_valid():
                    
                    Votacion.objects.create(titulo=serializer.data['titulo'], puntuacion=serializer.data['puntuacion'], fecha_votacion=serializer.data['fecha_votacion'], comenta_votacion = serializer.data['comenta_votacion'], producto_id=producto_review, cliente_id=cliente)
                    
                    return Response('Review añadida', status=status.HTTP_200_OK)
                
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as error:
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        else:
            return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    else:
        return Response('Necesita iniciar sesion', status=status.HTTP_401_UNAUTHORIZED)
    
    
@api_view(['GET'])    
def reviews_list(request):
    reviews = Votacion.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_reviews(request, product_id):
    producto = Producto.objects.get(id=product_id)
    producto_reviews = Votacion.objects.filter(producto_id=producto)
    serializer = ReviewSerializer(producto_reviews, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def eliminar_review(request, review_id):
    if (request.user.has_perm('App_SellsSubs.delete_votacion')):
        review = Votacion.objects.get(id = review_id)
        try:
            review.delete()
            return Response('Review eliminada')
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Sin permisos para esta operacion', status=status.HTTP_403_FORBIDDEN)