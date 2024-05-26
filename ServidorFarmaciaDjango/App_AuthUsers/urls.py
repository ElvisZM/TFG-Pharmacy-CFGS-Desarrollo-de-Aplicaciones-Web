from django.urls import path
from .views import *
from .import views

urlpatterns = [
    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),
    path('registrar/usuario/google', registrar_usuario_google.as_view()),
    path('registrar/usuario/facebook', registrar_usuario_facebook.as_view()),

]
