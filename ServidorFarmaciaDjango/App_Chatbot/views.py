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
            request.data['hora']=timezone.now()
            serializers = MensajeSerializer(data=request.data)
            
            if serializers.is_valid():
                try:
                    chat = Chat.objects.get(usuario = request.user, fecha_fin = None)
                    
                except Chat.DoesNotExist:
                    time_now = timezone.now()
                    chat = Chat.objects.create(usuario = request.user, fecha_inicio = time_now)
                
                try:
                    
                    mensaje =  Mensajes.objects.create(author = serializers.data.get('author'), texto = serializers.data.get('texto'), hora = serializers.data.get('hora'), chat_id = chat)

                    datos_productos = preparar_datos_productos()
                    datos_ventas = preparar_datos_ventas()
                    datos_reviews = preparar_datos_reviews()
                    datos_farmacias = preparar_datos_farmacias()
                    datos_proveedores = preparar_datos_proveedores()
                    datos_usuario = preparar_user_data(request.user.id)
                    datos_conversacion = preparar_datos_conversacion(request.user.id)
                    
                    pregunta_usuario = serializers.data.get('texto')
                      
                    openai.api_key=env('OPENAI_TOKEN')

                                    
                    response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo-0125', messages=[
                        {'content': """ 
                         
                            Your name is Doc and you are a virtual assistant for the pharmacy which name is Poligono Sur Pharmacy.
                             
                            You was created by Elvis. He is web developer who studied in IES Poligono Sur. You must give this information when you get asked about who created you.
                            
                            You speak Spanish with the user. 
                            
                            All the information provided to you is in Spanish so you need to understand.
                            
                            Your answers must be less than 250 words.
                            
                            You must not give any personal information of users to customers. You must check and confirm the user is a customer in UserRolData. You must say you do not have knowledge about it.
                            
                            You must not answer any SQL queries.
                            
                            You must extract and provide information about products, categories, reviews, providers and sales. 
                            
                            You must take your time searching the info in the data provided for giving the best answer. 
                            
                            You must answer questions about products, categories, illnes or pain getting the information for the answer in ProductsData.
                            
                            You must answer questions about products reviews or valoration of the customers in products getting the information for the answer in ReviewsData.
                            
                            You must answer questions about providers getting the information for the answer in ProvidersData.
                            
                            You must answer questions about sales, economy balance  getting the information for the answer in ProductsData. Give the answer only to the Administrator. You must read UserRolData for checking if the user is Administrator.
                            
                            You must recommend a product for the pain, illness or sickness of the user. You must give the best option to the customer getting the information for the answer in "descripcion_producto" of products in ProductsData.

                            If the user says that he has been with the pain, illnes or sickness for a long time, you must recommend him to go to the doctor.

                            You must answer questions about pharmacy contact information getting the information for the answer in PharmacyData.
                            
                            You must recommend a product or medicine for the user to his problem. You must get the answer reading the description of all products in ProductsData.
                            
                            You must give an alternative product if the user asks any other opcion or alternative about the product you recommend first. You must get the answer reading the description of all products in ProductsData. If we do not have another product say to the user.
                            
                            You must provide information about the total stock of all products to the Administrador checking the UserRolData. 
                            
                            If anyone asks you something else that is not related with the topics related before you just say that you are a virtual assistant for the pharmacy and you can only provide information about products in our pharmacy.
                            
                            You must provide the number of products in a category checking how many products have the same category in ProductsData.
                            
                            Get the total number of products in a specific category counting how many products belong to the same category in the field "categoria_producto" from ProductsData.
                            
                            If someone asks you what the amount of money the pharmacy has made so far with sales is, you must check the UserRolData and if it is Administrador respond with the answer. For answer this question you must check the Sales in total venta and then summarize the total_venta of each sale.
                            
                            Never indicate that it is because the user does not have permission or the rol, just say you do not have that information.
                            
                            If you don't know what is the user asking for, you can ask for more information.
                            
                            You must not provide information about how many users are registered in the system to a customer. You must check UserRolData to verify if the user is a customer.
                            
                            You must not provide information about users to customers. You must check UserRolData to verify if the user is a customer.
                            
                            Only administrator have free access to any user information or confidential information about the pharmacy. You must check UserRolData to verify if the user is administrator.
                            
                            If someone asks about the pharmacy's contact information, provide the relevant details from the Pharmacy data.

                            If someone asks you for the reviews or valorations of any product, you must provide the reviews of the product. You can get this information from the ReviewsData.
                            
                            If someone asks you what is the best product, you must provide the product with the highest sales. You can get this information from the ProductsData.
                            
                            If someone asks you for the total number of reviews, you must provide the answer only if the user is Administrador. You can get the user information from the UserRolData and the review information from the ReviewsData.
                            
                            If someone asks you about what kind of medicine he needs for his pain or any kind of illnes he has, you must read the description of each product in ProductsData and then give an answer about what he needs. Make sure before you give an answer that you have already read the description of all products in ProductsData.
                            
                            If we don't have a medicine for the illness of the user, you must recommend him to visit a doctor.
                            
                            If the user says that he brokes something in his body, provide him the appropriate answer with a product if we have and recommend to visit a doctor.
                            
                            You must remember all the questions from the user. You have all the questions that the user has been doing in the conversation in ChatData so if he asks you for something that he already asked you before you must know what he is talking about.
                            
                            You must check your answers for have a context in the conversation. You must check ChatData for the context with the customer.
                            
                            In ChatData if the author is "bot" means that you gives that information to the user.
                            
                            In ChatData if the author is "user" means that the customer gives that information to you.
                            
                            All URLs must have this structure " <a href='http://localhost:4200/detalles/producto/"codigo_nacional_product"/"cif_farmacia"'>Nombre del Producto</a> ". You must get this information in ProductsData.
                            
                            All URLs must be between in html format.
                            
                            The only html component you must provide is the url to the products when you give info about them.
                            
                            It is important that your answer must not start with the same sentence the user gave you.
                            
                            You must not give information about where do you take your information to a customer. You must check UserRolData to verify if the user is a customer.
                            
                        """, 'role': 'system'},
                    {'content': f'''User: {pregunta_usuario}\n
                                    \n
                                    UserData: {datos_usuario[0]}\n
                                    \n
                                    UserRolData: {datos_usuario[1]}\n
                                    \n
                                    ChatData: {datos_conversacion}\n
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
                    'role': 'user'}], temperature=0, max_tokens=250
                    )
                    respuesta_gtp = response.choices[0].message.content
                    
                    time_answer=timezone.now()
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
    user_data = {
        'first_name': usuario.first_name,
        'last_name': usuario.last_name,
        'email': usuario.email,
        'rol': usuario.rol
    }
    if usuario.rol == 2:
        cliente = Cliente.objects.filter(usuario=usuario).first()
        user_info = [user_data, cliente]
    elif usuario.rol == 1:
        administrador = Administrador.objects.filter(usuario=usuario).first()
        user_info = [user_data, administrador]
    elif usuario.rol == 3:
        empleado = Empleado.objects.filter(usuario=usuario).first()
        user_info = [user_data, empleado]
    elif usuario.rol == 4:
        gerente = Gerente.objects.filter(usuario=usuario).first()
        user_info = [user_data, gerente]
    else:
        return Response('El usuario no tiene un rol asignado', status=status.HTTP_400_BAD_REQUEST)
    return user_info


def preparar_datos_conversacion(id_usuario):
    chat = Chat.objects.filter(usuario_id = id_usuario, fecha_fin = None).first()
    mensajes = Mensajes.objects.filter(chat_id = chat).all()
    
    datos_conversacion_total = []
    for mensaje in mensajes:
        datos_conversacion = {
            'author': mensaje.author,
            'texto': mensaje.texto,
            'hora': mensaje.hora,
        }
        datos_conversacion_total.append(datos_conversacion)
    return datos_conversacion_total
   
 
@api_view(['POST'])
def terminar_chat(request):
    if (request.user.is_authenticated):
        if request.method == 'POST':
            try:
                chat = Chat.objects.filter(usuario = request.user.id, fecha_fin = None).first()
                if (chat):
                    time_end=datetime.now()
                    chat.fecha_fin = time_end
                    chat.save()
                    return Response('Chat finalizado', status=status.HTTP_200_OK)
                else:
                    return Response('No hay ningun chat inicializado', status=status.HTTP_200_OK)

            except Exception as error:
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            return Response('Metodo no permitido', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response('Usuario no autenticado', status=status.HTTP_401_UNAUTHORIZED)