from django import forms
from django.forms import ModelForm
from .models import *
from decimal import Decimal
from datetime import date
import datetime
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.forms import UserCreationForm

  
class BusquedaProductoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
         
class BusquedaAvanzadaProductoForm(forms.Form):
    
    nombre_prod = forms.CharField (required=False, label="Nombre del Producto")
    
    descripcion = forms.CharField (required=False)
    
    precio = forms.DecimalField(required=False)
    
    stock = forms.IntegerField(required=False)
    
    farmacia_prod = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia", widget=forms.Select())  
    
    prov_sum_prod = forms.ModelChoiceField (queryset=Proveedor.objects.all(), required=False, label="Proveedor", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        nombre_prod = self.cleaned_data.get('nombre_prod')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        stock = self.cleaned_data.get('stock')
        farmacia_prod = self.cleaned_data.get('farmacia_prod')
        prov_sum_prod = self.cleaned_data.get('prov_sum_prod')
        
        if(nombre_prod == ""
           and descripcion == ""
           and farmacia_prod is None
           and prov_sum_prod is None
           and precio is None
           and stock is None):
            self.add_error('nombre_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('descripcion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('farmacia_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('prov_sum_prod', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('precio', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(nombre_prod != "" and len(nombre_prod) < 3):
                self.add_error('nombre_prod', 'Debe introducir al menos 3 caracteres')
                
            if(descripcion != "" and len(descripcion) < 10):
                self.add_error('descripcion', 'Debe introducir al menos 10 caracteres')
                
            if(type(stock) != int or stock < 0):
                self.add_error('stock', 'Debe introducir un dato válido')    
                
        return self.cleaned_data
    
