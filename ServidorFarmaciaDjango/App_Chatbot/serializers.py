from rest_framework import serializers
from .models import *
from App_AuthUsers.serializers import *
from datetime import datetime, date


class ChatSerializer(serializers.ModelSerializer):
        
        usuario = UsuarioSerializer()
        
        class Meta:
            model = Chat
            fields = ['id', 'fecha_inicio', 'fecha_fin', 'usuario']


class MensajeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mensajes
        fields = ['author', 'texto', 'hora']
        
    def validate_author(self, author):
        if author != 'user' and author != 'bot':
            raise serializers.ValidationError('El author debe ser user o bot')
        return author
    
    def validate_texto(self, texto):
        if len(texto) < 1:
            raise serializers.ValidationError('El texto no puede estar vacio')
        
        elif self.initial_data == 'user' and len(texto) > 250:
            raise serializers.ValidationError('El texto no puede tener mas de 250 caracteres')
        else:
            return texto
        
    def validate_hora(self, hora):
        # Obtener la hora actual con zona horaria
        now = timezone.now()

        if hora.tzinfo is None or hora.utcoffset() is None:
            # Convertir `hora` a aware si es naive usando la zona horaria local
            hora = timezone.make_aware(hora, timezone.get_current_timezone())
        
        if hora is None or hora > now:
            raise serializers.ValidationError('La hora no es válida')
        return hora
            