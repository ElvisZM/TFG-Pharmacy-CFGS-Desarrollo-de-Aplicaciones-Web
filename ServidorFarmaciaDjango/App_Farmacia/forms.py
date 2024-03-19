from django import forms
from django.forms import ModelForm
from .models import *
from decimal import Decimal
from datetime import date
import datetime
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    roles = (
                (Usuario.CLIENTE, 'Cliente'),
                (Usuario.EMPLEADO, 'Empleado'),
                (Usuario.GERENTE, 'Gerente'),
                (Usuario.ADMINISTRADOR, 'Administrador'),
    )
    domicilio = forms.CharField(max_length=255, label="Domicilio")
    telefono = forms.CharField(max_length=15, label="Teléfono")
    birthday_date = forms.DateField()
    
    rol = forms.ChoiceField(choices=roles, label="Tipo de Usuario")
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'rol')
        labels = {
            "first_name": "Nombre y Apellidos", 
        }





   
class AdministradorModelForm(UserCreationForm):
    
    email = forms.EmailField(label="Email del administrador")
    
    first_name = forms.CharField(label="Nombre y Apellidos")
    
    direccion_admin = forms.CharField(label="Direccion", required=True)
    
    telefono_admin = forms.IntegerField(label="Telefono", required=True)
    
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name','email', 'password1', 'password2', 'date_joined', 'direccion_admin', 'telefono_admin')
        
    
    def clean(self):
    
        super().clean()

        direccion_admin = self.cleaned_data.get('direccion_admin')
        telefono_admin = self.cleaned_data.get('telefono_admin')

        #Comprobamos que se inserte una dirección
        if (direccion_admin is None):
            self.add_error('direccion_admin','Debe indicar una dirección de contacto para el administrador.')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.
        if (str(telefono_admin)[0] not in ('6','7','9') or len(str(telefono_admin)) != 9):
            self.add_error('telefono_admin','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro gerente.
        administradorTelefono = Administrador.objects.filter(telefono_admin=telefono_admin).first()    
        if (not administradorTelefono is None):
            self.add_error('telefono_admin','Ya existe un administrador con ese teléfono.')
            
        return self.cleaned_data
               

  
class AdministradorEditarModelForm(forms.ModelForm):
    
    direccion_admin = forms.CharField(label="Direccion", required=True)
    
    telefono_admin = forms.IntegerField(label="Telefono", required=True)
    
    
    class Meta:
        model = Administrador
        fields = '__all__'
        exclude = ('usuario',)
        

    
    def clean(self):
    
        super().clean()

        direccion_admin = self.cleaned_data.get('direccion_admin')
        telefono_admin = self.cleaned_data.get('telefono_admin')

        #Comprobamos que se inserte una dirección
        if (direccion_admin is None):
            self.add_error('direccion_admin','Debe indicar una dirección de contacto para el administrador.')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.
        if (str(telefono_admin)[0] not in ('6','7','9') or len(str(telefono_admin)) != 9):
            self.add_error('telefono_admin','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro administrador.
        administradorTelefono = Administrador.objects.filter(telefono_admin=telefono_admin).exclude(id=self.instance.id).first()    
        if (not administradorTelefono is None):
            self.add_error('telefono_admin','Ya existe un administrador con ese teléfono.')
           
        return self.cleaned_data
               



class BusquedaAdministradorForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaAdministradorForm(forms.Form):
    
    first_name = forms.CharField (required=False, label="Nombre del Administrador")
    
    email = forms.EmailField(required=False, label="Email del Administrador")
    
    date_joined = forms.DateTimeField (required=False, label="Fecha de Registro | dd-mm-yyyy", widget=forms.DateTimeInput())
    
    direccion_admin = forms.CharField(label="Direccion", required=False)
    
    telefono_admin = forms.IntegerField(label="Telefono", required=False)
    
    def clean(self):
        
        super().clean()
        
        first_name = self.cleaned_data.get('first_name')
        email = self.cleaned_data.get('email')
        direccion_admin = self.cleaned_data.get('direccion_admin')
        date_joined = self.cleaned_data.get('date_joined')
        telefono_admin = self.cleaned_data.get('telefono_admin')
        if(first_name == ""
           and email == ""
           and direccion_admin == ""
           and date_joined is None
           and telefono_admin is None):
            self.add_error('first_name', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('email', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion_admin', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('date_joined', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono_admin', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(first_name != "" and len(first_name) < 3):
                self.add_error('first_name', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data









class ProductoModelForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_prod','descripcion','precio','farmacia_prod','prov_sum_prod']
        labels = {
            "nombre_prod": "Nombre del Producto",
            "descripcion": "Descripcion del Producto",
            "precio": "Precio",
            "farmacia_prod":"Farmacia",
            "prov_sum_prod": "Proveedor del Producto",
        }
        help_texts = {
            "nombre_prod": "200 carácteres como máximo",
            "descripcion": "Al menos 10 carácteres como mínimo",
            "precio": "Indique un precio para el Producto",
            "farmacia_prod": "Indique la Farmacia del Producto",
            "prov_sum_prod": "Indique quien es el Proveedor",
        }
        
        widgets = {   
            
        }
        
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        nombre_prod = self.cleaned_data.get('nombre_prod')
        descripcion = self.cleaned_data.get('descripcion')
        precio = self.cleaned_data.get('precio')
        farmacia_prod = self.cleaned_data.get('farmacia_prod')
        prov_sum_prod = self.cleaned_data.get('prov_sum_prod')
        
        #Comprobamos que no existe un producto con ese nombre
        productoNombre = Producto.objects.filter(nombre_prod=nombre_prod).first()
        if (not productoNombre is None):
            if(not self.instance is None and productoNombre.id == self.instance.id):
                pass
            else:
                self.add_error('nombre_prod','Ya existe un producto con ese nombre')
            
        #Comprobamos que la descripción tiene al menos 10 carácteres.            
        if len(descripcion) < 10:
            self.add_error('descripcion','Al menos debes indicar 10 carácteres')
            
        #Comprobamos que el precio está puesto en su formato con decimales (float)
        if type(precio) != Decimal:
            self.add_error('precio','El precio introducido no es válido')
                        
        #Comprobamos que al menos seleccione un Proveedor
        if len(prov_sum_prod) < 1:
            self.add_error('prov_sum_prod','Debe seleccionar al menos un proveedor')
        
        #Siempre devolver los datos    
        return self.cleaned_data
    
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
    


    
class FarmaciaModelForm(ModelForm):
    class Meta:
        model = Farmacia
        fields = ['nombre_farm','direccion_farm','telefono_farm']
        labels = {
            'nombre_farm': "Nombre de la Farmacia",
            'direccion_farm': "Dirección",
            'telefono_farm': "Telefono",
        }
        help_texts = {
            "nombre_farm": "200 carácteres como máximo",
            "direccion_farm": "Al menos 10 carácteres como mínimo",
            "telefono_farm": "Indique un número de contacto",
        }
        widgets ={
            
        }
        
    def clean(self):
        
        super().clean()
        
        nombre_farm = self.cleaned_data.get('nombre_farm')
        direccion_farm = self.cleaned_data.get('direccion_farm')
        telefono_farm = self.cleaned_data.get('telefono_farm')
        
        #Comprobamos que no exista una farmacia con ese nombre
        farmaciaNombre = Farmacia.objects.filter(nombre_farm=nombre_farm).first()
        if(not (farmaciaNombre is None or (not self.instance is None and farmaciaNombre.id == self.instance.id))):
            self.add_error('nombre_farm','Ya existe una farmacia con ese nombre')
            
        #Comprobamos que se inserte una dirección
        if (direccion_farm is None):
            self.add_error('direccion_farm','Debe especificar una dirección para la farmacia')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.
        if (str(telefono_farm)[0] not in ('6','7','9') or len(str(telefono_farm)) != 9):
            self.add_error('telefono_farm','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otra farmacia.
        farmaciaTelefono = Farmacia.objects.filter(telefono_farm=telefono_farm).first()    
        if (not farmaciaTelefono is None):
            self.add_error('telefono_farm','Ya existe una farmacia con ese teléfono.')
            
        return self.cleaned_data

class BusquedaFarmaciaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaFarmaciaForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
            
    nombre_farm = forms.CharField (required=False)
    
    direccion_farm = forms.CharField (required=False)
    
    telefono_farm = forms.IntegerField(required=False)
    
    def clean(self):
        
        super().clean()
        
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        nombre_farm = self.cleaned_data.get('nombre_farm')
        direccion_farm = self.cleaned_data.get('direccion_farm')
        telefono_farm = self.cleaned_data.get('telefono_farm')
        
        if(textoBusqueda == ""
           and nombre_farm == ""
           and direccion_farm == ""
           and telefono_farm is None):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nombre_farm', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion_farm', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono_farm', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data




  
    
class GerenteModelForm(UserCreationForm):
    
    
    email = forms.EmailField(label="Email del gerente")
    
    salario_ger = forms.FloatField(label="Salario", required=True, help_text='Salario del Gerente')
    
    first_name = forms.CharField(label="Nombre y Apellidos", required=True)
    
    direccion_ger = forms.CharField(label="Direccion", required=True)
    
    telefono_ger = forms.IntegerField(label="Telefono", required=True)
    
    gerente_farm = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia Asignada", widget=forms.Select())

    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name','email', 'password1', 'password2', 'date_joined', 'direccion_ger', 'telefono_ger', 'salario_ger','gerente_farm')

    
    def clean(self):
    
        super().clean()

        salario_ger = self.cleaned_data.get('salario_ger')
        gerente_farm = self.cleaned_data.get('gerente_farm')
        direccion_ger = self.cleaned_data.get('direccion_ger')
        telefono_ger = self.cleaned_data.get('telefono_ger')

        #Comprobamos que se inserte un salario para el gerente.
        if (salario_ger is None):
            self.add_error('salario_ger','Debe especificar un salario para el gerente.')
            
        #Comprobamos que se inserte una dirección
        if (direccion_ger is None):
            self.add_error('direccion_ger','Debe indicar una dirección de contacto para el gerente.')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol.
        if (str(telefono_ger)[0] not in ('6','7','9') or len(str(telefono_ger)) != 9):
            self.add_error('telefono_ger','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro gerente.
        gerenteTelefono = Gerente.objects.filter(telefono_ger=telefono_ger).exclude(id=self.instance.id).first()    
        if (not gerenteTelefono is None):
            self.add_error('telefono_ger','Ya existe un gerente con ese teléfono.')
           
        #Comprobamos que inserte una farmacia a gestionar    
        if (gerente_farm is None):
            self.add_error('gerente_farm','Debe introducir una farmacia a gestionar.')
            
        #Comprobamos que la farmacia no tenga ya a un gerente que la gestione
        farmaciaGestionada = Gerente.objects.filter(gerente_farm=gerente_farm).exclude(id=self.instance.id).first()
        if (farmaciaGestionada):
            self.add_error('gerente_farm','La farmacia ya tiene a un gerente asignado.')

        return self.cleaned_data
               
               
                
    
class GerenteEdicionForm(forms.Form):
    
    username = forms.CharField(label='Usuario' ,max_length=150)
    
    first_name = forms.CharField(label='Nombre y Apellidos', max_length=150)
    
    email = forms.EmailField(label='Email')
    
    date_joined = forms.DateField(label='Fecha de Registro')
    
    salario_ger = forms.FloatField(label="Salario", required=True, help_text='Salario del Gerente')
    
    direccion_ger = forms.CharField(label="Direccion", required=True)
    
    telefono_ger = forms.IntegerField(label="Telefono", required=True)
    
    gerente_farm = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=True, label="Farmacia Asignada", widget=forms.Select())


    def clean(self):
    
        super().clean()

        salario_ger = self.cleaned_data.get('salario_ger')
        gerente_farm = self.cleaned_data.get('gerente_farm')
        direccion_ger = self.cleaned_data.get('direccion_ger')
        telefono_ger = self.cleaned_data.get('telefono_ger')

        #Comprobamos que se inserte un salario para el gerente.
        if (salario_ger is None):
            self.add_error('salario_ger','Debe especificar un salario para el gerente.')
            
        #Comprobamos que se inserte una dirección
        if (direccion_ger is None):
            self.add_error('direccion_ger','Debe indicar una dirección de contacto para el gerente.')
            
        #Comprobamos que inserte una farmacia a gestionar    
        if (gerente_farm is None):
            self.add_error('gerente_farm','Debe introducir una farmacia a gestionar.')

        return self.cleaned_data
    
    def clean_telefono_ger(self):
        telefono_ger = self.cleaned_data.get('telefono_ger')

        #Comprobamos que el numero tenga 9 digitos, sea espanyol.
        if not str(telefono_ger).startswith(('6', '7', '9')) or len(str(telefono_ger)) != 9:
            raise forms.ValidationError('Debe especificar un número espanyol de 9 dígitos.')

        #Obtenemos la ID del gerente actual
        gerente_id = self.data.get('gerente_id')

        #Comprobamos que el numero no exista en otro gerente.
        if gerente_id and Gerente.objects.filter(telefono_ger=telefono_ger).exclude(id=gerente_id).exists():
            raise forms.ValidationError('Ya existe un gerente con ese teléfono.')

        return telefono_ger
    
    
    def clean_gerente_farm(self):
        gerente_farm = self.cleaned_data.get('gerente_farm')

        #Comprobamos que la farmacia no tenga ya a un gerente que la gestione
        if Gerente.objects.filter(gerente_farm=gerente_farm).exclude(gerente_farm=gerente_farm).exists():
            raise forms.ValidationError('La farmacia ya tiene un gerente asignado.')
        
        return gerente_farm
               
               

class BusquedaGerenteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaGerenteForm(forms.Form):
    
    first_name = forms.CharField (required=False, label="Nombre del Gerente")
    
    email = forms.EmailField(required=False, label="Email del Gerente")
    
    date_joined = forms.DateTimeField (required=False, label="Fecha de Registro | dd-mm-yyyy", widget=forms.DateTimeInput())
    
    salario_ger = forms.FloatField(required=False, label="Salario del Gerente")
    
    direccion_ger = forms.CharField(label="Direccion", required=False)
    
    telefono_ger = forms.IntegerField(label="Telefono", required=False)
    
    gerente_farm = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia Asignada", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        first_name = self.cleaned_data.get('first_name')
        email = self.cleaned_data.get('email')
        direccion_ger = self.cleaned_data.get('direccion_ger')
        date_joined = self.cleaned_data.get('date_joined')
        telefono_ger = self.cleaned_data.get('telefono_ger')
        salario_ger = self.cleaned_data.get('salario_ger')
        gerente_farm = self.cleaned_data.get('gerente_farm')
        fecha_hoy = date.today()
        if(first_name == ""
           and email == ""
           and direccion_ger == ""
           and date_joined is None
           and telefono_ger is None
           and salario_ger is None
           and gerente_farm is None):
            self.add_error('first_name', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('email', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion_ger', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('date_joined', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono_ger', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('salario_ger', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('gerente_farm', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(first_name != "" and len(first_name) < 3):
                self.add_error('first_name', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data
    
    
    
    
    
    

class EmpleadoModelForm(UserCreationForm):
    
    email = forms.EmailField(label="Email del empleado")
    
    salario = forms.FloatField(label="Salario", required=True, help_text='Salario del Empleado')
    
    farm_emp = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label='Farmacia Asignada', widget=forms.Select())
    
    first_name = forms.CharField(label="Nombre y Apellidos", required=True)
    
    direccion_emp = forms.CharField(label="Direccion", required=True)
    
    telefono_emp = forms.IntegerField(label="Telefono", required=True)
    
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name','email', 'password1', 'password2', 'date_joined', 'direccion_emp', 'telefono_emp', 'salario','farm_emp')

    
    def clean(self):
    
        super().clean()

        salario = self.cleaned_data.get('salario')
        farm_emp = self.cleaned_data.get('farm_emp')
        direccion_emp = self.cleaned_data.get('direccion_emp')
        telefono_emp = self.cleaned_data.get('telefono_emp')

        #Comprobamos que se inserte un salario para el empleado.
        if (salario is None):
            self.add_error('salario','Debe especificar un salario para el empleado.')
            
        #Comprobamos que se inserte una dirección
        if (direccion_emp is None):
            self.add_error('direccion_emp','Debe indicar una dirección de contacto para el empleado.')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.
        if (str(telefono_emp)[0] not in ('6','7','9') or len(str(telefono_emp)) != 9):
            self.add_error('telefono_emp','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro empleado.
        empleadoTelefono = Empleado.objects.filter(telefono_emp=telefono_emp).first()    
        if (not empleadoTelefono is None):
            self.add_error('telefono_emp','Ya existe un empleado con ese teléfono.')
            
        return self.cleaned_data
    
class EmpleadoEditarModelForm(forms.ModelForm):
    
    salario = forms.FloatField(label="Salario", required=True, help_text='Salario del Empleado')
    
    farm_emp = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=True, label='Farmacia Asignada', widget=forms.Select())
    
    direccion_emp = forms.CharField(label="Direccion", required=True)
    
    telefono_emp = forms.IntegerField(label="Telefono", required=True)
    
    class Meta:
        model = Empleado
        fields = '__all__'
        exclude = ('usuario',)

    
    def clean(self):
    
        super().clean()

        salario = self.cleaned_data.get('salario')
        farm_emp = self.cleaned_data.get('farm_emp')
        direccion_emp = self.cleaned_data.get('direccion_emp')
        telefono_emp = self.cleaned_data.get('telefono_emp')

        #Comprobamos que se inserte un salario para el empleado.
        if (salario is None):
            self.add_error('salario','Debe especificar un salario para el empleado.')
            
        #Comprobamos que se inserte una dirección
        if (direccion_emp is None):
            self.add_error('direccion_emp','Debe indicar una dirección de contacto para el empleado.')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.
        if (str(telefono_emp)[0] not in ('6','7','9') or len(str(telefono_emp)) != 9):
            self.add_error('telefono_emp','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro empleado.
        empleadoTelefono = Empleado.objects.filter(telefono_emp=telefono_emp).exclude(id=self.instance.id).first()    
        if (not empleadoTelefono is None):
            self.add_error('telefono_emp','Ya existe un empleado con ese teléfono.')
            
        if (farm_emp is None):
            self.add_error('farm_emp','Debe especificar a que farmacia pertenece el empleado.')    
            
        return self.cleaned_data


    
class BusquedaEmpleadoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaEmpleadoForm(forms.Form):
    
    first_name = forms.CharField (required=False, label="Nombre del Empleado")
    
    email = forms.EmailField(required=False, label="Email del Empleado")
    
    date_joined = forms.DateTimeField (required=False, label="Fecha de Registro | dd-mm-yyyy", widget=forms.DateTimeInput())
    
    salario = forms.FloatField(required=False, label="Salario del Empleado")
    
    direccion_emp = forms.CharField(label="Direccion", required=False)
    
    telefono_emp = forms.IntegerField(label="Telefono", required=False)
    
    farm_emp = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia Asignada", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        first_name = self.cleaned_data.get('first_name')
        email = self.cleaned_data.get('email')
        direccion_emp = self.cleaned_data.get('direccion_emp')
        date_joined = self.cleaned_data.get('date_joined')
        telefono_emp = self.cleaned_data.get('telefono_emp')
        salario = self.cleaned_data.get('salario')
        farm_emp = self.cleaned_data.get('farm_emp')
        fecha_hoy = date.today()
        if(first_name == ""
           and email == ""
           and direccion_emp == ""
           and date_joined is None
           and telefono_emp is None
           and salario is None
           and farm_emp is None):
            self.add_error('first_name', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('email', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion_emp', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('date_joined', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono_emp', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('salario', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('farm_emp', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(first_name != "" and len(first_name) < 3):
                self.add_error('first_name', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data
    
    
    
    
    
class VotacionModelForm(ModelForm):
    class Meta:
        model = Votacion
        fields = ['puntuacion', 'comenta_votacion','voto_producto','voto_cliente']
        labels = {
            "puntuacion": "Puntuacion del Producto",
            "comenta_votacion": "Comentario sobre la Votacion",
            "voto_producto": "Nombre del Producto",
            "voto_cliente": "Nombre del Cliente",
            
        }
        help_texts = {
            "puntuacion": "Indique una puntuacion",
            "comenta_votacion": "Indiquenos por qué ha dado esta puntuación",
            "voto_producto": "Indique el nombre del producto",
            "voto_cliente": "Indique su nombre",
        }
        widgets = {
        }
        
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        puntuacion = self.cleaned_data.get('puntuacion')
        comenta_votacion = self.cleaned_data.get('comenta_votacion')
        voto_producto = self.cleaned_data.get('voto_producto')
        voto_cliente = self.cleaned_data.get('voto_cliente')
        
        
        #Comprobamos que el comentario tiene al menos 10 carácteres.            
        if len(comenta_votacion) < 10:
            self.add_error('comenta_votacion','Al menos debes indicar 10 carácteres')
                            
        #Comprobamos que seleccione un Producto
        if (voto_producto is None):
            self.add_error('voto_producto','Debe seleccionar un producto')
        
        #Comprobamos que seleccione un cliente
        if (voto_cliente is None):
            self.add_error('voto_cliente','Debe seleccionar quien realizo la votación')
        
        #Siempre devolver los datos    
        return self.cleaned_data
    
class BusquedaVotacionForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
            
class BusquedaAvanzadaVotacionForm(forms.Form):
    
    puntuacion = forms.IntegerField (required=False, label="Puntuacion")
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2030))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2030))
                                )       
    
    comenta_votacion = forms.CharField(required=False)
    
    voto_producto = forms.ModelChoiceField (queryset=Producto.objects.all(), required=False, label="Producto", widget=forms.Select())  
    
    voto_cliente = forms.ModelChoiceField (queryset=Cliente.objects.all(), required=False, label="Cliente", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        puntuacion = self.cleaned_data.get('puntuacion')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        comenta_votacion = self.cleaned_data.get('comenta_votacion')
        voto_producto = self.cleaned_data.get('voto_producto')
        voto_cliente = self.cleaned_data.get('voto_cliente')
        
        if(puntuacion is None
           and fecha_desde is None
           and fecha_hasta is None
           and comenta_votacion == ""
           and voto_producto is None
           and voto_cliente is None):
            self.add_error('puntuacion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('comenta_votacion', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('voto_producto', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('voto_cliente', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(comenta_votacion != "" and len(comenta_votacion) < 3):
                self.add_error('comenta_votacion', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data
    
  
    
    
class ClienteModelForm(UserCreationForm):
    
    email = forms.EmailField(label="Email del cliente")
    
    first_name = forms.CharField(label="Nombre y Apellidos", required=True)
    
    direccion_cli = forms.CharField(label="Direccion", required=True)
    
    telefono_cli = forms.IntegerField(label="Telefono", required=True)
    
    productos_favoritos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False, label="Producto Favorito del Cliente", widget=forms.SelectMultiple())

    votacion_prod = forms.ModelMultipleChoiceField (queryset=Producto.objects.all(), required=False, label="Productos Votados por el Cliente", widget=forms.SelectMultiple())
 
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name','email', 'password1', 'password2', 'date_joined', 'direccion_cli', 'telefono_cli', 'productos_favoritos','votacion_prod')
    
    
    def clean(self):
    
        super().clean()

        direccion_cli = self.cleaned_data.get('direccion_cli')
        telefono_cli = self.cleaned_data.get('telefono_cli')

        #Comprobamos que se inserte una dirección para el cliente.
        if (direccion_cli is None):
            self.add_error('direccion_cli', 'Debe especificar una direccioón para el cliente.')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.
        if (str(telefono_cli)[0] not in ('6','7','9') or len(str(telefono_cli)) != 9):
            self.add_error('telefono_cli','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro cliente.
        clienteTelefono = Cliente.objects.filter(telefono_cli=telefono_cli).first()    
        if (not clienteTelefono is None):
            self.add_error('telefono_cli','Ya existe un cliente con ese teléfono.')
                
        return self.cleaned_data

  
class ClienteEditarModelForm(forms.ModelForm):
    
    direccion_cli = forms.CharField(label="Direccion", required=True)
    
    telefono_cli = forms.IntegerField(label="Telefono", required=True)
    
    productos_favoritos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), required=False, label="Producto Favorito del Cliente", widget=forms.SelectMultiple())

    votacion_prod = forms.ModelMultipleChoiceField (queryset=Producto.objects.all(), required=False, label="Productos Votados por el Cliente", widget=forms.SelectMultiple())
 
    
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ('usuario',)
    
    
    def clean(self):
    
        super().clean()

        direccion_cli = self.cleaned_data.get('direccion_cli')
        telefono_cli = self.cleaned_data.get('telefono_cli')

        #Comprobamos que se inserte una dirección para el cliente.
        if (direccion_cli is None):
            self.add_error('direccion_cli', 'Debe especificar una direccioón para el cliente.')
            
        #Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.
        if (str(telefono_cli)[0] not in ('6','7','9') or len(str(telefono_cli)) != 9):
            self.add_error('telefono_cli','Debe especificar un número espanyol de 9 dígitos.')
        
        #Comprobamos que el numero no exista en otro cliente.
        clienteTelefono = Cliente.objects.filter(telefono_cli=telefono_cli).first()    
        if (not clienteTelefono is None):
            self.add_error('telefono_cli','Ya existe un cliente con ese teléfono.')
                
        return self.cleaned_data
                              

class BusquedaClienteForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaClienteForm(forms.Form):
    
    first_name = forms.CharField (required=False, label="Nombre del Cliente")
    
    email = forms.EmailField(required=False, label="Email del Cliente")
    
    date_joined = forms.DateTimeField (required=False, label="Fecha de Registro | dd-mm-yyyy", widget=forms.DateTimeInput())
    
    direccion_cli = forms.CharField(label="Direccion", required=False)
    
    telefono_cli = forms.IntegerField(label="Telefono", required=False)
    
    productos_favoritos = forms.ModelChoiceField(queryset=Producto.objects.all(), required=False, label="Producto Favorito del Cliente", widget=forms.Select())
    
    votacion_prod = forms.ModelChoiceField (queryset=Producto.objects.all(), required=False, label="Productos Votados por el Cliente", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        first_name = self.cleaned_data.get('first_name')
        email = self.cleaned_data.get('email')
        direccion_cli = self.cleaned_data.get('direccion_cli')
        date_joined = self.cleaned_data.get('date_joined')
        telefono_cli = self.cleaned_data.get('telefono_cli')
        productos_favoritos = self.cleaned_data.get('productos_favoritos')
        votacion_prod = self.cleaned_data.get('votacion_prod')

        if(first_name == ""
           and email == ""
           and date_joined is None
           and telefono_cli is None
           and direccion_cli == ""
           and productos_favoritos is None
           and votacion_prod is None):
            self.add_error('first_name', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('email', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('direccion_cli', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('date_joined', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('telefono_cli', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('productos_favoritos', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('votacion_prod', 'Debe introducir al menos un valor en un campo del formulario')
                    
        else:
            if(first_name != "" and len(first_name) < 3):
                self.add_error('first_name', 'Debe introducir al menos 3 caracteres')
                
        return self.cleaned_data
        
    
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    
    
    
    
    
    
    
class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre_promo', 'descripcion_promo','valor_promo','fecha_fin_promo','cliente_promo']
        labels = {
            "nombre_promo": "Nombre de la Promocion",
            "descripcion_promo": "Describe la Promocion",
            "valor_promo": "Valor de la Promocion",
            "fecha_fin_promo": "Indique fin de la promocion",
            "cliente_promo": "Seleccione al cliente beneficiado",
            
        }
        help_texts = {
            "nombre_promo": "Nombre la promocion",
            "descripcion_promo": "Describa la promocion",
            "valor_promo": "Indique de cuanto es la promoción",
            "fecha_fin_promo": "Fecha de expiración de la promoción",
            "cliente_promo": "Seleccione al cliente beneficiado",
        }
        widgets = {
            "fecha_fin_promo":forms.SelectDateWidget(),
        }
        
    def clean(self):
        
        super().clean()
        
        #Obtenemos los campos
        nombre_promo = self.cleaned_data.get('nombre_promo')
        descripcion_promo = self.cleaned_data.get('descripcion_promo')
        valor_promo = self.cleaned_data.get('valor_promo')
        fecha_fin_promo = self.cleaned_data.get('fecha_fin_promo')
        cliente_promo = self.cleaned_data.get('cliente_promo')
        
        
        #Nombre de la Promoción es único
        promocionNombre = Promocion.objects.filter(nombre_promo=nombre_promo).first()
        if(not (promocionNombre is None or (not self.instance is None and promocionNombre.id == self.instance.id))):
            self.add_error('nombre_promo','Ya existe una promocion con ese nombre')
        
        #Comprobamos que la descripción tiene al menos 100 carácteres.            
        if len(descripcion_promo) < 100:
            self.add_error('descripcion_promo','Al menos debes indicar 100 carácteres')
            
        #Comprobamos que el cliente no tenga ya la misma promoción aplicada
        mismaPromocionFalse = Promocion.objects.filter(cliente_promo=cliente_promo, nombre_promo=nombre_promo).exists()
        
        if (mismaPromocionFalse):
            self.add_error('nombre_promo','El cliente ya tiene esta promoción aplicada.')    
        
        #Comprobamos que el valor del descuento sea un entero entre 0 y 100
        if (valor_promo is None or valor_promo not in range(0,101)):
            self.add_error('valor_promo','Debe introducir un valor entero entre 0 y 100')
        
        #Comprobamos la fecha de expiración no sea inferior a la actual.
        fechaHoy = date.today()
        if (fechaHoy > fecha_fin_promo):
            self.add_error('fecha_fin_promo','Debe seleccionar una fecha de expiración mayor a la de hoy.')
        
        #Siempre devolver los datos    
        return self.cleaned_data
    
class BusquedaPromocionForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
            
class BusquedaAvanzadaPromocionForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
            
    nombre_promo = forms.CharField (required=False, label="Nombre de la Promocion")
    
    descripcion_promo = forms.CharField(required=False)
    
    valor_promo = forms.IntegerField (required=False)
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2030))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2030))
                                )       
                                  
    cliente_promo = forms.ModelChoiceField(queryset=Cliente.objects.all() ,required=False, label="Cliente con promoción", widget=forms.Select())
    
    def clean(self):
        
        super().clean()
        
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        nombre_promo = self.cleaned_data.get('nombre_promo')
        descripcion_promo = self.cleaned_data.get('descripcion_promo')
        valor_promo = self.cleaned_data.get('valor_promo')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        cliente_promo = self.cleaned_data.get('cliente_promo')
        
        if(textoBusqueda == ""
           and nombre_promo == ""
           and descripcion_promo == ""
           and valor_promo is None
           and fecha_desde is None
           and fecha_hasta is None
           and cliente_promo is None):
            self.add_error('textoBusqueda', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('nombre_promo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('descripcion_promo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('valor_promo', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta', 'Debe introducir al menos un valor en un campo del formulario')
            self.add_error('cliente_promo', 'Debe introducir al menos un valor en un campo del formulario')
            
                    
        else:
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda', 'Debe introducir al menos 3 caracteres')
            
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
                
        return self.cleaned_data