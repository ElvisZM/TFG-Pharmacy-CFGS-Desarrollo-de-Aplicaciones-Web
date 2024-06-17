from django.db import models
from django.conf import settings


class Chat(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey('App_AuthUsers.Usuario', on_delete=models.CASCADE)
    

class Mensajes(models.Model):
    author = models.CharField(max_length=20)
    texto = models.TextField()
    hora = models.DateTimeField()
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, db_column='chat_id')
    