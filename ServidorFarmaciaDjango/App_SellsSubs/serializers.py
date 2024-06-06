from rest_framework import serializers
from .models import *
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from App_AuthUsers.models import *
from App_AuthUsers.serializers import ClienteSerializer
from App_ProductProvider.serializers import ProductoSerializer

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['fecha_compra', 'direccion_envio', 'codigo_postal', 'municipio', 'provincia', 'total_pago']
        
    def validate_fecha_compra(self, fecha_compra):
        if fecha_compra is None:
            raise serializers.ValidationError("La fecha de compra no puede ser nula")
        return fecha_compra
    
    def validate_direccion_envio(self, direccion_envio):
        if direccion_envio is None:
            raise serializers.ValidationError("La direccion de envio no puede ser nula")
        return direccion_envio
    
    def validate_codigo_postal(self, codigo_postal):
        if codigo_postal is None:
            raise serializers.ValidationError("El codigo postal no puede ser nulo")
        return codigo_postal
    
    def validate_municipio(self, municipio):
        if municipio is None:
            raise serializers.ValidationError("El municipio no puede ser nulo")
        return municipio
    
    def validate_provincia(self, provincia):
        if provincia is None:
            raise serializers.ValidationError("La provincia no puede ser nula")
        return provincia
    
    def validate_total_pago(self, total_pago):
        if total_pago is None:
            raise serializers.ValidationError("El total de pago no puede ser nulo")
        return total_pago
    
    
class PagoSerializerCreditCard(serializers.ModelSerializer):
    
    class Meta:
        model = Pago
        fields = ['tipo_pago','titular_tarjeta','numero_tarjeta','tipo_tarjeta','fecha_pago']
        
    def validate_tipo_pago(self, tipo_pago):
        if tipo_pago is None:
            raise serializers.ValidationError("El tipo de pago no puede ser nulo")
        return tipo_pago
    
    def validate_titular_tarjeta(self, titular_tarjeta):
        if self.initial_data['tipo_pago'] == 'creditcard' and titular_tarjeta is None:
            raise serializers.ValidationError("El titular de la tarjeta no puede ser nulo")
        return titular_tarjeta
    
    def validate_numero_tarjeta(self, numero_tarjeta):
        if self.initial_data['tipo_pago'] == 'creditcard' and  numero_tarjeta is None:
            raise serializers.ValidationError("El numero de tarjeta no puede ser nulo")
        return numero_tarjeta
    
    def validate_tipo_tarjeta(self, tipo_tarjeta):
        if self.initial_data['tipo_pago'] == 'creditcard' and  tipo_tarjeta is None:
            raise serializers.ValidationError("El tipo de tarjeta no puede ser nulo")
        return tipo_tarjeta
    
    def validate_fecha_pago(self, fecha_pago):
        if fecha_pago is None:
            raise serializers.ValidationError("La fecha de pago no puede ser nula")
        return fecha_pago
    
    
    
class PagoSerializerPayPal(serializers.ModelSerializer):
    
    class Meta:
        model = Pago
        fields = ['tipo_pago', 'id_transaccion', 'paypal_email_transaccion', 'fecha_pago']
        
    def validate_tipo_pago(self, tipo_pago):
        if tipo_pago is None:
            raise serializers.ValidationError("El tipo de pago no puede ser nulo")
        return tipo_pago
    
    def validate_id_transaccion(self, id_transaccion):
        if self.initial_data['tipo_pago'] == 'paypal' and  id_transaccion is None:
            raise serializers.ValidationError("El id de transaccion no puede ser nulo")
        return id_transaccion
    
    def validate_paypal_email_transaccion(self, paypal_email_transaccion):
        if self.initial_data['tipo_pago'] == 'paypal' and  paypal_email_transaccion is None:
            raise serializers.ValidationError("El email de paypal no puede ser nulo")
        return paypal_email_transaccion
    
    def validate_fecha_pago(self, fecha_pago):
        if fecha_pago is None:
            raise serializers.ValidationError("La fecha de pago no puede ser nula")
        return fecha_pago
    
    
class ReviewSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Votacion
        fields = ['titulo', 'puntuacion', 'fecha_votacion', 'comenta_votacion']
        
    def validate_titulo(self, titulo):
        if titulo is None:
            raise serializers.ValidationError('El titulo no puede ser nulo')
        return titulo
        
        
    def validate_puntuacion(self, puntuacion):
        try:
            puntuacion = int(puntuacion)
        except ValueError:
            raise serializers.ValidationError('La puntuacion no es un número válido')
        
        if puntuacion is None or (0 > puntuacion > 5):
            raise serializers.ValidationError('La puntuacion no es valida')
        return puntuacion


    def validate_fecha_votacion(self, fecha_votacion):
        if fecha_votacion is None:
            raise serializers.ValidationError('La fecha de votacion no puede ser nula')
        return fecha_votacion
    
    
    def validate_comenta_votacion(self, comenta_votacion):
        if comenta_votacion is None:
            raise serializers.ValidationError('El comentario no puede ser nula')            
        return comenta_votacion
    
        
class ReviewSerializer(serializers.ModelSerializer):
    producto_id = ProductoSerializer()
    cliente_id = ClienteSerializer()
    
    class Meta:
        fields = '__all__'
        model= Votacion