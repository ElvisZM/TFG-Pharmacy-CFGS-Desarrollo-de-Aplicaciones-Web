from django.shortcuts import render
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# Create your views here.
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
                    
                    return Response("Compra registrada correctamente", status=status.HTTP_200_OK)
                
                else:
                    errors = {**pago_serializer.errors, **compra_serializer.errors}
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)  
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Metodo no permitido', status=status.HTTP_405_BAD_REQUEST)
        
    else:
        return Response('Necesita iniciar sesion', status=status.HTTP_401_UNAUTHORIZED)
        