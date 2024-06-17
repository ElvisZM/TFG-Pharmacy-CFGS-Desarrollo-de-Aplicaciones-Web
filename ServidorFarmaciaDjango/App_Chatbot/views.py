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
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from oauth2_provider.models import AccessToken, Application
from django.conf import settings
from datetime import date, timedelta, datetime
from App_AuthUsers.models import Usuario, Cliente
from App_ProductProvider.models import Producto, Proveedor, Categoria, Farmacia
import environ
import os
from pathlib import Path
import json
import openai

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)

@api_view(['POST'])
def get_answer_bot_openai(request):
    if (request.user.is_authenticated):
        if (request.method == 'POST'):
            request.data['hora']=datetime.now()
            serializers = MensajeSerializer(data=request.data)
            
            if serializers.is_valid():
                try:
                    chat = Chat.objects.get(usuario = request.user, fecha_fin = None)
                    
                except Chat.DoesNotExist:
                    time_now = datetime.now()
                    chat = Chat.objects.create(usuario = request.user, fecha_inicio = time_now)
                
                try:
                    
                    mensaje =  Mensajes.objects.create(author = serializers.data.get('author'), texto = serializers.data.get('texto'), hora = serializers.data.get('hora'), chat_id = chat)

                    datos_productos = preparar_datos_productos()
                    datos_ventas = preparar_datos_ventas()
                    datos_reviews = preparar_datos_reviews()
                    datos_farmacias = preparar_datos_farmacias()
                    datos_proveedores = preparar_datos_proveedores()
                    datos_usuario = preparar_user_data(request.user.id)
                    
                    pregunta_usuario = serializers.data.get('texto')
                      
                    openai.api_key=env('OPENAI_TOKEN')

                                    
                    response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo-0125', messages=[
                        {'content': """ 
                            Your name is Doc and you are a virtual assistant for the pharmacy which name is Poligono Sur Pharmacy.
                             
                            Your creator is Elvis and he is a web developer who studied in IES Poligono Sur.
                            
                            You speak different languages. 
                            
                            You can extract and provide information about products, categories, reviews, providers and sales. 
                            
                            You can take your time searching for the correct information. 
                            
                            If anyone asks you something else that is not about the products, categories, reviews, providers, sales, self user info or any other topic related with our pharmacy, you just say that you are a virtual assistant for the pharmacy and you can only provide information about products in our pharmacy.
                            
                            If someone asks you what the amount of money the pharmacy has made so far with sales is, you must check the UserRolData and if it is Administrador respond with the answer. For answer this question you must check the Sales in total venta and then summarize the total_venta of each sale.
                            
                            Never indicate that it is because the user does not have permission or the rol, just say you do not have that information.
                            
                            If you don't know what is the user asking for, you can ask for more information.
                            
                            If anyone asks you who is him, you can get his information from the UserData, you give him his first name and his last name if he has. If the user has elfabri28@gmail.com as email you add in the answer that he is the creator of the virtual assistant.
                            
                            If someone asks about the pharmacy's contact information, provide the relevant details from the Pharmacy data.

                            In any of the cases, you must indicate the username or password of the users. Only the first name of the user and the last name of the user if he has it. You must pay attention to the UserRol and the UserData.
                            
                            If someone asks you for the reviews or valorations of any product, you must provide the reviews of the product. You can get this information from the ReviewsData.
                            
                            If someone asks you what is the best product, you must provide the product with the highest sales. You can get this information from the ProductsData.
                            
                            If someone asks you for the total number of reviews, you must provide the answer only if the user is Administrador. You can get the user information from the UserRolData and the review information from the ReviewsData.
                            
                        """, 'role': 'system'},
                    {'content': f'''User: {pregunta_usuario}\n
                                    \n
                                    UserData: {datos_usuario[0]}\n
                                    \n
                                    UserRolData: {datos_usuario[1]}\n
                                    \n
                                    PharmacyData: {datos_farmacias}\n
                                    \n
                                    ProductsData: {datos_productos}\n
                                    \n
                                    ProvidersData: {datos_proveedores}\n
                                    \n
                                    SalesData: {datos_ventas}\n
                                    \n
                                    ReviewsData: {datos_reviews}\n
                                    \n
                                    ''',
                    'role': 'user'}], temperature=0, max_tokens=100
                    )
                    respuesta_gtp = response.choices[0].message.content
                    
                    time_answer=datetime.now()
                    Mensajes.objects.create(author='bot', texto=respuesta_gtp, hora=time_answer, chat_id=chat)
                    
                    return Response({'respuesta_bot':respuesta_gtp}, status=status.HTTP_200_OK)
                    
                except Exception as error:
                    return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    else:
        return Response('Usuario no autenticado', status=status.HTTP_401_UNAUTHORIZED)




def preparar_datos_ventas():
    ventas = Compra.objects.all()
    datos_ventas = []

    for venta in ventas:
        cliente = Cliente.objects.filter(id=venta.cliente_id.id).first()
        usuario = Usuario.objects.filter(id=cliente.usuario.id).first()
        
        datos_venta = {
            'fecha_venta': venta.fecha_compra,
            'direccion_envio': venta.direccion_envio,
            'codigo_postal': venta.codigo_postal,
            'municipio': venta.municipio,
            'provincia': venta.provincia,
            'total_venta': venta.total_pago,
            'cliente': cliente,
            'usuario': usuario,
            'carrito': venta.carrito_id
        }
        datos_ventas.append(datos_venta)

    return datos_ventas

def preparar_datos_productos():
    productos = Producto.objects.all()
    datos_productos = []

    for producto in productos:
        categoria = Categoria.objects.filter(id=producto.categoria_id.id).first()
        farmacia = Farmacia.objects.filter(id=producto.farmacia_id.id).first()
        suministro_producto = SuministroProducto.objects.filter(producto_id=producto.id).first()
        proveedor = Proveedor.objects.filter(id=suministro_producto.proveedor_id.id).first()

        datos_producto = {
            'codigo_nacional': producto.cn_prod,
            'nombre_producto': producto.nombre_prod,
            'descripcion_producto': producto.descripcion,
            'precio_producto': producto.precio,
            'stock_producto': producto.stock,
            'ventas_producto': producto.ventas,
            'cif_farmacia_producto': producto.cif_farm,
            'categoria_producto': categoria,
            'farmacia_producto': farmacia,
            'proveedor_producto': proveedor,
        }
        datos_productos.append(datos_producto)

    return datos_productos

def preparar_datos_reviews():
    reviews = Votacion.objects.all()
    datos_reviews = []

    for review in reviews:
        cliente = Cliente.objects.filter(id=review.cliente_id.id).first()
        usuario = Usuario.objects.filter(id=cliente.usuario.id).first()
        producto = Producto.objects.filter(id=review.producto_id.id).first()

        datos_review = {
            'titulo_review': review.titulo,
            'puntuacion_review': review.puntuacion,
            'fecha_review': review.fecha_votacion,
            'comentario_review': review.comenta_votacion,
            'cliente_review': cliente,
            'usuario_review': usuario,
            'producto_review': producto
        }
        datos_reviews.append(datos_review)

    return datos_reviews

def preparar_datos_farmacias():
    farmacias = Farmacia.objects.all()
    datos_farmacias = []

    for farmacia in farmacias:
        datos_farmacia = {
            'cif_farmacia': farmacia.cif_farm,
            'nombre_farmacia': farmacia.nombre_farm,
            'direccion_farmacia': farmacia.direccion_farm,
            'telefono_farmacia': farmacia.telefono_farm
        }
        datos_farmacias.append(datos_farmacia)

    return datos_farmacias

def preparar_datos_proveedores():
    proveedores = Proveedor.objects.all()
    datos_proveedores = []

    for proveedor in proveedores:
        datos_proveedor = {
            'cif_proveedor': proveedor.cif_prov,
            'nombre_proveedor': proveedor.nombre_prov,
            'direccion_proveedor': proveedor.direccion_prov,
            'telefono_proveedor': proveedor.telefono_prov
        }
        datos_proveedores.append(datos_proveedor)

    return datos_proveedores

def preparar_user_data(id_usuario):
    usuario = Usuario.objects.filter(id=id_usuario).first()
    if usuario.rol == 2:
        cliente = Cliente.objects.filter(usuario=usuario).first()
        user_info = [usuario, cliente]
    elif usuario.rol == 1:
        administrador = Administrador.objects.filter(usuario=usuario).first()
        user_info = [usuario, administrador]
    elif usuario.rol == 3:
        empleado = Empleado.objects.filter(usuario=usuario).first()
        user_info = [usuario, empleado]
    elif usuario.rol == 4:
        gerente = Gerente.objects.filter(usuario=usuario).first()
        user_info = [usuario, gerente]
    else:
        return Response('El usuario no tiene un rol asignado', status=status.HTTP_400_BAD_REQUEST)
    return user_info