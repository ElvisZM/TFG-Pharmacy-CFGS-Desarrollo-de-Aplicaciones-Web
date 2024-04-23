from django.urls import path
from .views import *


urlpatterns = [
    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),
    path('registro/google', registrar_usuario_google.as_view()),

]