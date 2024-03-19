from django.shortcuts import render, redirect

# Create your views here.
from .models import *
from django.db.models import Q, Prefetch
from django.views.defaults import page_not_found
from datetime import datetime as dt, date
from django.db.models import Avg
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required



def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = dt.now().strftime("%d/%m/%Y %H:%M")
        
    productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod').all()[:6]
    
    return render(request, 'index.html', {'productos': productos})

def borrar_sesion(request):
    del request.session["fecha_inicio"]
    
    return render(request, 'index.html')

def registrar_usuario(request):
    
    if request.method == "POST":
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if (rol == Usuario.CLIENTE):
                grupo = Group.objects.get(name="Cliente")
                grupo.user_set.add(user)
                cliente = Cliente.objects.create(usuario = user,
                                                direccion_cli=formulario.cleaned_data.get('domicilio'),
                                                telefono_cli=formulario.cleaned_data.get('telefono'))
                cliente.save()
            if (rol == Usuario.EMPLEADO):
                grupo = Group.objects.get(name="Empleado")
                grupo.user_set.add(user)
                empleado = Empleado.objects.create(usuario = user, 
                                                direccion_emp=formulario.cleaned_data.get('domicilio'),
                                                telefono_emp=formulario.cleaned_data.get('telefono'))
                empleado.save()
            if (rol == Usuario.GERENTE):
                grupo = Group.objects.get(name="Gerente")
                grupo.user_set.add(user)
                gerente = Gerente.objects.create(usuario = user,
                                                direccion_ger=formulario.cleaned_data.get('domicilio'),
                                                telefono_ger=formulario.cleaned_data.get('telefono'))
                gerente.save()
            if (rol == Usuario.ADMINISTRADOR):
                grupo = Group.objects.get(name="Administrador")
                grupo.user_set.add(user)
                administrador = Administrador.objects.create(usuario = user, 
                                                direccion_admin=formulario.cleaned_data.get('domicilio'),
                                                telefono_admin=formulario.cleaned_data.get('telefono'))
                administrador.save()
                
            login(request, user)
            return redirect('index')
        
    else:
        formulario = RegistroForm()
    
    return render(request, 'registration/signup.html', {'formulario': formulario})

def login_menu (request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Credenciales incorrectas. Por favor, inténtalo de nuevo.')

            return redirect('index')
        
    return render(request, 'registration/login_menu.html')




def crear_administrador_modelo(formulario):
        
    administrador_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            usuario = Usuario.objects.create(
                username=formulario.cleaned_data.get('username'),
                first_name=formulario.cleaned_data.get('first_name'),
                email=formulario.cleaned_data.get('email'),
                date_joined=formulario.cleaned_data.get('date_joined'),
                rol=Usuario.ADMINISTRADOR
            )
            usuario.set_password(formulario.cleaned_data.get("password1"))
            usuario.save()
            administrador = Administrador.objects.create(
                usuario= usuario,
                direccion_admin= formulario.cleaned_data.get("direccion_admin"),
                telefono_admin= formulario.cleaned_data.get("telefono_admin"),
            )
            administrador.save()            
            administrador_creado = True
        except:
            pass
    return administrador_creado                

@permission_required('App_Farmacia.add_administrador')
def administrador_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = AdministradorModelForm(datosFormulario)
    if (request.method == 'POST'):
        administrador_creado = crear_administrador_modelo(formulario)
        if (administrador_creado):
            messages.success(request, 'Se ha anyadido el administrador '+formulario.cleaned_data.get('first_name')+" correctamente")
            return redirect("lista_administradores")       

    return render(request, 'admin/create_administrador.html', {'formulario':formulario})



@permission_required('App_Farmacia.view_administrador')
def administrador_buscar(request):
    formulario = BusquedaAdministradorForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        administradores = Administrador.objects.all()
        administradores = administradores.filter(usuario__first_name__contains=texto).all()
        return render(request, 'admin/administrador_busqueda.html',{'administradores_mostrar':administradores, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
@permission_required('App_Farmacia.view_administrador')
def administrador_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaAdministradorForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSadministradores = Administrador.objects.all()
            
            first_name = formulario.cleaned_data.get('first_name')
            email = formulario.cleaned_data.get('email')
            direccion_admin = formulario.cleaned_data.get('direccion_admin')
            date_joined = formulario.cleaned_data.get('date_joined')
            telefono_admin = formulario.cleaned_data.get('telefono_admin')
            
            if (first_name != ""):
                QSadministradores = QSadministradores.filter(usuario__first_name__contains=first_name)
                mensaje_busqueda += "Nombre o que contenga la palabra "+first_name+"\n"
                
            if (email != ""):
                QSadministradores = QSadministradores.filter(usuario__email=email)
                mensaje_busqueda += "Email que sea igual a "+email+"\n"
                
            if (direccion_admin != ""):
                QSadministradores = QSadministradores.filter(direccion_admin__contains=direccion_admin)
                mensaje_busqueda += "Direccion o que contenga la palabra "+direccion_admin+"\n"
            
            if (not date_joined is None):
                mensaje_busqueda += f"Fecha de registro que sea igual o mayor a "+str(date_joined)+"\n"
                QSadministradores = QSadministradores.filter(usuario__date_joined__gte = date_joined)
            
            if (not telefono_admin is None):
                mensaje_busqueda += f"Telefono que sea igual a "+str(telefono_admin)+"\n"
                QSadministradores = QSadministradores.filter(telefono_admin = telefono_admin)
            
            administradores = QSadministradores.all()
            
            return render(request, 'admin/administrador_busqueda.html', {'administradores_mostrar':administradores, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaAdministradorForm(None)
        
    return render(request, 'admin/busqueda_avanzada_administrador.html',{'formulario':formulario})    
    
    
@permission_required('App_Farmacia.change_administrador')
def administrador_editar(request, administrador_id):
    administrador = Administrador.objects.get(id=administrador_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = AdministradorEditarModelForm(datosFormulario, instance = administrador)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el administrador {administrador.usuario.first_name} correctamente")
                return redirect('lista_administradores')
            except Exception as error:
                pass
    return render(request, 'admin/actualizar_administrador.html', {'formulario': formulario, 'administrador':administrador})    
    
       
@permission_required('App_Farmacia.delete_administrador')
def administrador_eliminar(request, administrador_id):
    administrador = Administrador.objects.get(id=administrador_id)
    try:
        administrador.delete()
        messages.success(request, f"Se ha eliminado el administrador {administrador.usuario.first_name} correctamente.")
    except:
        pass
    return redirect('lista_administradores')

@permission_required('App_Farmacia.view_administrador')
def administradores_lista(request):
    
    administradores = Administrador.objects.select_related('usuario').all()

    return render(request, 'admin/lista_administradores.html', {'administradores':administradores})





# PARA FORMULARIOS 
def crear_producto_modelo(formulario):
        
    producto_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            producto_creado = True
        except:
            pass
    return producto_creado                

@permission_required('App_Farmacia.add_producto')
def producto_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = ProductoModelForm(datosFormulario)
    if (request.method == 'POST'):
        producto_creado = crear_producto_modelo(formulario)
        if (producto_creado):
            messages.success(request, 'Se ha creado el producto '+formulario.cleaned_data.get('nombre_prod')+" correctamente")
            return redirect("lista_productos")       

    return render(request, 'producto/create.html', {'formulario':formulario})


def producto_buscar(request):
    
    formulario = BusquedaProductoForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
        productos = productos.filter(Q(nombre_prod__contains=texto) | Q(descripcion__contains=texto)).all()
        return render(request, 'producto/producto_busqueda.html',{"productos_mostrar":productos, "texto_busqueda":texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")

def producto_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaProductoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSproductos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
            
            nombre_prod = formulario.cleaned_data.get('nombre_prod')
            descripcion = formulario.cleaned_data.get('descripcion')
            precio = formulario.cleaned_data.get('precio')
            farmacia_prod = formulario.cleaned_data.get('farmacia_prod')
            prov_sum_prod = formulario.cleaned_data.get('prov_sum_prod')
                            
            if (nombre_prod != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=nombre_prod) | Q(descripcion__contains=nombre_prod))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+nombre_prod+"\n"
                
            if (descripcion != ""):
                QSproductos = QSproductos.filter(Q(nombre_prod__contains=descripcion) | Q(descripcion__contains=descripcion))
                mensaje_busqueda += "Nombre o descripcion que contenga la palabra "+descripcion+"\n"
            
            if (not precio is None):
                QSproductos = QSproductos.filter(precio__gte= precio)
                mensaje_busqueda += f"Precio que sea igual o mayor a {precio}\n"
            
            if (not farmacia_prod is None):
                QSproductos = QSproductos.filter(farmacia_prod=farmacia_prod)
                mensaje_busqueda += "Que la farmacia a la que pertence sea "+farmacia_prod.nombre_farm+"\n"
                
            if (not prov_sum_prod is None):
                QSproductos = QSproductos.filter(prov_sum_prod=prov_sum_prod)
                mensaje_busqueda += "Que el proveedor sea "+prov_sum_prod.nombre_prov+"\n"
        
            
            
            productos = QSproductos.all()
            
            return render(request, 'producto/producto_busqueda.html', {'productos_mostrar':productos, 'texto_busqueda':mensaje_busqueda})    
                
                
    else:
        formulario = BusquedaAvanzadaProductoForm(None)
    return render(request, 'producto/busqueda_avanzada.html',{"formulario":formulario})
                
@permission_required('App_Farmacia.change_producto')
def producto_editar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)

    datosFormulario = None
    
    if request.method == 'POST':
        datosFormulario = request.POST

    formulario = ProductoModelForm(datosFormulario, instance=producto)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el producto {producto.nombre_prod} correctamente")
                return redirect('lista_productos')
            except Exception as error:
                print(error)
            
    return render(request, 'producto/actualizar.html',{"formulario":formulario, "producto":producto})

@permission_required('App_Farmacia.delete_producto')
def producto_eliminar(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    try:
        producto.delete()
        messages.success(request, f"Se ha eliminado el producto {producto.nombre_prod} correctamente.")
    except:
        pass
    return redirect('lista_productos')

def crear_farmacia_modelo(formulario):
    farmacia_creada = False
    
    if formulario.is_valid():
        try:
            formulario.save()
            farmacia_creada = True
        except:
            pass
    return farmacia_creada

@permission_required('App_Farmacia.add_farmacia')
def farmacia_create(request):
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
        
    formulario = FarmaciaModelForm(datosFormulario)
    
    if (request.method == 'POST'):
        farmacia_creada = crear_farmacia_modelo(formulario)
        
        if(farmacia_creada):
            messages.success(request, 'Se ha creado la farmacia '+formulario.cleaned_data.get('nombre_farm')+' correctamente.')
            return redirect("lista_farmacias")
    
    return render(request, 'farmacia/create_farmacia.html',{'formulario':formulario})

def farmacia_buscar(request):
    formulario = BusquedaFarmaciaForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        farmacias = Farmacia.objects.all()
        farmacias = farmacias.filter(nombre_farm__contains=texto).all()
        return render(request, 'farmacia/farmacia_busqueda.html',{'farmacias_mostrar':farmacias, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def farmacia_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaFarmaciaForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSfarmacias = Farmacia.objects.all()
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            nombre_farm = formulario.cleaned_data.get('nombre_farm')
            direccion_farm = formulario.cleaned_data.get('direccion_farm')
            telefono_farm = formulario.cleaned_data.get('telefono_farm')
            
            if (textoBusqueda != ""):
                QSfarmacias = QSfarmacias.filter(nombre_farm__contains=textoBusqueda)
                mensaje_busqueda += "Nombre o que contenga la palabra "+textoBusqueda+"\n"
                
            if (nombre_farm != ""):
                QSfarmacias = QSfarmacias.filter(nombre_farm__contains=nombre_farm)
                mensaje_busqueda += "Nombre o que contenga la palabra "+nombre_farm+"\n"
                
            if (direccion_farm != ""):
                QSfarmacias = QSfarmacias.filter(direccion_farm__contains=direccion_farm)
                mensaje_busqueda += "Direccion o que contenga la palabra "+direccion_farm+"\n"
            
            if (not telefono_farm is None):
                QSfarmacias = QSfarmacias.filter(telefono_farm = telefono_farm)
                mensaje_busqueda += f"Numero de telefono que sea igual a {telefono_farm}\n"
                
            farmacias = QSfarmacias.all()
            
            return render(request, 'farmacia/farmacia_busqueda.html', {'farmacias_mostrar':farmacias, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaFarmaciaForm(None)
    return render(request, 'farmacia/busqueda_avanzada_farmacia.html',{'formulario':formulario})    
    
    
@permission_required('App_Farmacia.change_farmacia')
def farmacia_editar(request, farmacia_id):
    farmacia = Farmacia.objects.get(id=farmacia_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = FarmaciaModelForm(datosFormulario, instance = farmacia)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado la farmacia {farmacia.nombre_farm} correctamente")
                return redirect('lista_farmacias')
            except Exception as error:
                pass
    return render(request, 'farmacia/actualizar_farmacia.html', {'formulario': formulario, 'farmacia':farmacia})    
    
    

@permission_required('App_Farmacia.delete_farmacia')
def farmacia_eliminar(request, farmacia_id):
    farmacia = Farmacia.objects.get(id=farmacia_id)
    try:
        farmacia.delete()
        messages.success(request, f"Se ha eliminado la farmacia {farmacia.nombre_farm} correctamente.")
    except:
        pass
    return redirect('lista_farmacias')


def crear_gerente_modelo(formulario):
        
    gerente_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            usuario = Usuario.objects.create(
                username=formulario.cleaned_data.get('username'),
                first_name=formulario.cleaned_data.get('first_name'),
                email=formulario.cleaned_data.get('email'),
                date_joined=formulario.cleaned_data.get('date_joined'),
                rol=Usuario.GERENTE
            )
            usuario.set_password(formulario.cleaned_data.get("password1"))
            usuario.save()
            gerente = Gerente.objects.create(
                usuario= usuario,
                salario_ger= formulario.cleaned_data.get("salario_ger"),
                gerente_farm= formulario.cleaned_data.get("gerente_farm"),
                direccion_ger= formulario.cleaned_data.get("direccion_ger"),
                telefono_ger= formulario.cleaned_data.get("telefono_ger"),
            )
            gerente.save()            
            gerente_creado = True
        except:
            pass
    return gerente_creado                

@permission_required('App_Farmacia.add_gerente')
def gerente_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = GerenteModelForm(datosFormulario)
    if (request.method == 'POST'):
        gerente_creado = crear_gerente_modelo(formulario)
        if (gerente_creado):
            messages.success(request, 'Se ha anyadido el gerente '+formulario.cleaned_data.get('first_name')+" correctamente")
            return redirect("lista_gerentes")       

    return render(request, 'gerente/create_gerente.html', {'formulario':formulario})

@permission_required('App_Farmacia.view_gerente')
def gerente_buscar(request):
    formulario = BusquedaGerenteForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        gerentes = Gerente.objects.all()
        gerentes = gerentes.filter(usuario__first_name__contains=texto).all()
        return render(request, 'gerente/gerente_busqueda.html',{'gerentes_mostrar':gerentes, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
@permission_required('App_Farmacia.view_gerente')
def gerente_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaGerenteForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSgerentes = Gerente.objects.all()
            
            first_name = formulario.cleaned_data.get('first_name')
            email = formulario.cleaned_data.get('email')
            direccion_ger = formulario.cleaned_data.get('direccion_ger')
            date_joined = formulario.cleaned_data.get('date_joined')
            telefono_ger = formulario.cleaned_data.get('telefono_ger')
            salario_ger = formulario.cleaned_data.get('salario_ger')
            gerente_farm = formulario.cleaned_data.get('gerente_farm')
            
            if (first_name != ""):
                QSgerentes = QSgerentes.filter(usuario__first_name__contains=first_name)
                mensaje_busqueda += "Nombre o que contenga la palabra "+first_name+"\n"
                
            if (email != ""):
                QSgerentes = QSgerentes.filter(usuario__email=email)
                mensaje_busqueda += "Email que sea igual a "+email+"\n"
                
            if (direccion_ger != ""):
                QSgerentes = QSgerentes.filter(direccion_ger__contains=direccion_ger)
                mensaje_busqueda += "Direccion o que contenga la palabra "+direccion_ger+"\n"
            
            if (not date_joined is None):
                mensaje_busqueda += f"Fecha de registro que sea igual o mayor a "+str(date_joined)+"\n"
                QSgerentes = QSgerentes.filter(usuario__date_joined__gte = date_joined)
            
            if (not telefono_ger is None):
                mensaje_busqueda += f"Telefono que sea igual a "+str(telefono_ger)+"\n"
                QSgerentes = QSgerentes.filter(telefono_ger = telefono_ger)
            
            if (not salario_ger is None):
                mensaje_busqueda += f"Salario que sea igual o mayor a "+str(salario_ger)+"\n"
                QSgerentes = QSgerentes.filter(salario_ger__gte = salario_ger)
                
            if (not gerente_farm is None):
                mensaje_busqueda += "Gerente que tenga asignado la farmacia "+gerente_farm.nombre_farm+"\n"
                QSgerentes = QSgerentes.filter(gerente_farm=gerente_farm)
                
            gerentes = QSgerentes.all()
            
            return render(request, 'gerente/gerente_busqueda.html', {'gerentes_mostrar':gerentes, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaGerenteForm(None)
        
    return render(request, 'gerente/busqueda_avanzada_gerente.html',{'formulario':formulario})    
    
@permission_required('App_Farmacia.change_gerente')
def gerente_editar(request, gerente_id):
    gerente = Gerente.objects.get(id=gerente_id)
    formulario = GerenteEdicionForm( initial={
                        "username":gerente.usuario.username,
                        "first_name":gerente.usuario.first_name,
                        "email":gerente.usuario.email,
                        "date_joined":gerente.usuario.date_joined,
                        "direccion_ger":gerente.direccion_ger,
                        "telefono_ger":gerente.telefono_ger,
                        "salario_ger":gerente.salario_ger,
                        "gerente_farm":gerente.gerente_farm
                        
                        })

    if request.method == "POST":    
        formulario = GerenteEdicionForm(request.POST)
        if formulario.is_valid():
            gerente.usuario.username = formulario.cleaned_data['username']
            gerente.usuario.first_name = formulario.cleaned_data['first_name']
            gerente.usuario.email = formulario.cleaned_data['email']
            gerente.usuario.date_joined = formulario.cleaned_data['date_joined']
            gerente.direccion_ger = formulario.cleaned_data['direccion_ger']
            gerente.telefono_ger = formulario.cleaned_data['telefono_ger']
            gerente.salario_ger = formulario.cleaned_data['salario_ger']
            gerente.gerente_farm = formulario.cleaned_data['gerente_farm']
            gerente.usuario.save()
            gerente.save()
            messages.success(request, f"Se ha editado el gerente {gerente.usuario.first_name} correctamente")
            return redirect('lista_gerentes')
        else:
            print("Formulario inválido:", formulario.errors)

    return render(request, 'gerente/actualizar_gerente.html', {'formulario': formulario, 'gerente': gerente})

    
    
    
@permission_required('App_Farmacia.delete_gerente')
def gerente_eliminar(request, gerente_id):
    gerente = Gerente.objects.get(id=gerente_id)
    try:
        gerente.delete()
        messages.success(request, f"Se ha eliminado el gerente {gerente.usuario.first_name} correctamente.")
    except:
        pass
    return redirect('lista_gerentes')



def crear_empleado_modelo(formulario):
        
    empleado_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            username = formulario.cleaned_data.get('username')
            password = formulario.cleaned_data.get("password")
            password1 = formulario.cleaned_data.get("password1")

            # Imprimir información relevante
            print("Username:", username)
            print("Password antes de encriptar:", password)
            print("Password antes de encriptar:", password1)
            #Guarda el producto en la base de datos
            usuario = Usuario.objects.create(
                username=formulario.cleaned_data.get('username'),
                first_name=formulario.cleaned_data.get('first_name'),
                email=formulario.cleaned_data.get('email'),
                date_joined=formulario.cleaned_data.get('date_joined'),
                rol=Usuario.EMPLEADO
            )
            usuario.set_password(formulario.cleaned_data.get("password1"))
            usuario.save()
            print("Password después de encriptar:", usuario.password)

            empleado = Empleado.objects.create(
                usuario= usuario,
                salario= formulario.cleaned_data.get("salario"),
                farm_emp= formulario.cleaned_data.get("farm_emp"),
                direccion_emp= formulario.cleaned_data.get("direccion_emp"),
                telefono_emp= formulario.cleaned_data.get("telefono_emp"),
            )
            empleado.save() 
            empleado_creado = True
        except Exception as e: 
            print(e)
    return empleado_creado                

@permission_required('App_Farmacia.add_empleado')
def empleado_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = EmpleadoModelForm(datosFormulario)
    if (request.method == 'POST'):
        empleado_creado = crear_empleado_modelo(formulario)
        if (empleado_creado):
            messages.success(request, 'Se ha anyadido '+formulario.cleaned_data.get('first_name')+" correctamente")
            return redirect("lista_empleados")       

    return render(request, 'empleado/create_empleado.html', {'formulario':formulario})

@permission_required('App_Farmacia.view_empleado')
def empleado_buscar(request):
    formulario = BusquedaEmpleadoForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        empleados = Empleado.objects.all()
        empleados = empleados.filter(usuario__first_name__contains=texto).all()
        return render(request, 'empleado/empleado_busqueda.html',{'empleados_mostrar':empleados, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
@permission_required('App_Farmacia.view_empleado')
def empleado_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaEmpleadoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSempleados = Empleado.objects.all()
            
            first_name = formulario.cleaned_data.get('first_name')
            email = formulario.cleaned_data.get('email')
            direccion_emp = formulario.cleaned_data.get('direccion_emp')
            date_joined = formulario.cleaned_data.get('date_joined')
            telefono_emp = formulario.cleaned_data.get('telefono_emp')
            salario = formulario.cleaned_data.get('salario')
            farm_emp = formulario.cleaned_data.get('farm_emp')
            
            if (first_name != ""):
                QSempleados = QSempleados.filter(usuario__first_name__contains=first_name)
                mensaje_busqueda += "Nombre o que contenga la palabra "+first_name+"\n"
                
            if (email != ""):
                QSempleados = QSempleados.filter(usuario__email=email)
                mensaje_busqueda += "Email sea igual a "+email+"\n"
            
            if (direccion_emp != ""):
                mensaje_busqueda += f"Direccion o que contenga la palabra "+direccion_emp+"\n"
                QSempleados = QSempleados.filter(direccion_emp__contains = direccion_emp)
            
            if (not date_joined is None):
                mensaje_busqueda += f"Fecha de registro que sea igual o mayor a "+str(date_joined)+"\n"
                QSempleados = QSempleados.filter(usuario__date_joined__gte = date_joined)
            
            if (not telefono_emp is None):
                mensaje_busqueda += f"Telefono que sea igual a "+str(telefono_emp)+"\n"
                QSempleados = QSempleados.filter(telefono_emp = telefono_emp)
            
            if (not salario is None):
                mensaje_busqueda += f"Salario que sea igual o mayor a "+str(salario)+"\n"
                QSempleados = QSempleados.filter(salario__gte = salario)
                
            if (not farm_emp is None):
                QSempleados = QSempleados.filter(farm_emp=farm_emp)
                mensaje_busqueda += "Que este asignado/a a la Farmacia "+farm_emp.nombre_farm+"\n"
            
            empleados = QSempleados.all()
            
            return render(request, 'empleado/empleado_busqueda.html', {'empleados_mostrar':empleados, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaEmpleadoForm(None)
        
    return render(request, 'empleado/busqueda_avanzada_empleado.html',{'formulario':formulario})    
  
    
@permission_required('App_Farmacia.change_empleado')
def empleado_editar(request, empleado_id):
    empleado = Empleado.objects.select_related('usuario', 'farm_emp').get(id=empleado_id)
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = EmpleadoEditarModelForm(datosFormulario, instance = empleado)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el empleado {empleado.usuario.first_name} correctamente")
                return redirect('lista_empleados')
            except Exception as error:
                pass
    return render(request, 'empleado/actualizar_empleado.html', {'formulario': formulario, 'empleado':empleado})    
        
@permission_required('App_Farmacia.delete_empleado')
def empleado_eliminar(request, empleado_id):
    empleado = Empleado.objects.get(id=empleado_id)
    try:
        empleado.delete()
        messages.success(request, f"Se ha eliminado el empleado {empleado.usuario.first_name} correctamente.")
    except:
        pass
    return redirect('lista_empleados')


def crear_votacion_modelo(formulario):
        
    votacion_creada = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            votacion_creada = True
        except:
            pass
    return votacion_creada                

@permission_required('App_Farmacia.add_votacion')
def votacion_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = VotacionModelForm(datosFormulario)
    if (request.method == 'POST'):
        votacion_creada = crear_votacion_modelo(formulario)
        if (votacion_creada):
            messages.success(request, 'Se ha anyadido la votación al producto '+formulario.cleaned_data.get('voto_producto').nombre_prod+" correctamente")
            return redirect("lista_votaciones")       

    return render(request, 'votacion/create_votacion.html', {'formulario':formulario})

def votacion_buscar(request):
    formulario = BusquedaVotacionForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        votaciones = Votacion.objects.all()
        votaciones = votaciones.filter(Q(comenta_votacion__contains=texto) | Q(voto_producto__nombre_prod__contains=texto)).all()
        return render(request, 'votacion/votacion_busqueda.html',{'votaciones_mostrar':votaciones, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def votacion_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaVotacionForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSvotaciones = Votacion.objects.all()
            
            puntuacion = formulario.cleaned_data.get('puntuacion')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            comenta_votacion = formulario.cleaned_data.get('comenta_votacion')
            voto_producto = formulario.cleaned_data.get('voto_producto')
            voto_cliente = formulario.cleaned_data.get('voto_cliente')
            
            if (not puntuacion is None):
                QSvotaciones = QSvotaciones.filter(puntuacion=puntuacion)
                mensaje_busqueda += "Puntuacion sea "+str(puntuacion)+"\n"
                
            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+date.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                QSvotaciones = QSvotaciones.filter(fecha_votacion__gte=fechaDesde)
            
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+date.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                QSvotaciones = QSvotaciones.filter(fecha_votacion__lte=fechaHasta)
            
            if (comenta_votacion != ""):
                QSvotaciones = QSvotaciones.filter(comenta_votacion__contains=comenta_votacion)
                mensaje_busqueda += "Comentario o que contenga la palabra "+comenta_votacion+"\n"
            
            if (not voto_producto is None):
                QSvotaciones = QSvotaciones.filter(voto_producto=voto_producto)
                mensaje_busqueda += "Que el producto sea "+voto_producto.nombre_prod+"\n"
                
            if (not voto_cliente is None):
                QSvotaciones = QSvotaciones.filter(voto_cliente=voto_cliente)
                mensaje_busqueda += "Que el cliente sea "+voto_cliente.usuario.first_name+"\n"
        
            
            votaciones = QSvotaciones.all()
            
            return render(request, 'votacion/votacion_busqueda.html', {'votaciones_mostrar':votaciones, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaVotacionForm(None)
        
    return render(request, 'votacion/busqueda_avanzada_votacion.html',{'formulario':formulario})    
    
    
@permission_required('App_Farmacia.change_votacion')
def votacion_editar(request, votacion_id):
    votacion = Votacion.objects.get(id=votacion_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = VotacionModelForm(datosFormulario, instance = votacion)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado la votación al producto {votacion.voto_producto.nombre_prod} correctamente")
                return redirect('lista_votaciones')
            except Exception as error:
                pass
    return render(request, 'votacion/actualizar_votacion.html', {'formulario': formulario, 'votacion':votacion})    
        
    
@permission_required('App_Farmacia.delete_votacion')
def votacion_eliminar(request, votacion_id):
    votacion = Votacion.objects.get(id=votacion_id)
    try:
        votacion.delete()
        messages.success(request, f"Se ha eliminado la votación al producto {votacion.voto_producto.nombre_prod} correctamente.")
    except:
        pass
    return redirect('lista_votaciones')




def crear_cliente_modelo(formulario):
        
    cliente_creado = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            usuario = Usuario.objects.create(
                username=formulario.cleaned_data.get('username'),
                first_name=formulario.cleaned_data.get('first_name'),
                email=formulario.cleaned_data.get('email'),
                date_joined=formulario.cleaned_data.get('date_joined'),
                rol=Usuario.CLIENTE
            )
            usuario.set_password(formulario.cleaned_data.get("password1"))
            usuario.save()
            cliente = Cliente.objects.create(
                usuario= usuario,
                direccion_cli= formulario.cleaned_data.get("direccion_cli"),
                telefono_cli= formulario.cleaned_data.get("telefono_cli"),
            )
            
            productos_favoritos = formulario.cleaned_data.get("productos_favoritos")
            if productos_favoritos:
                cliente.productos_favoritos.set(productos_favoritos)

            votacion_prod = formulario.cleaned_data.get("votacion_prod")
            if votacion_prod:
                cliente.votacion_prod.set(votacion_prod)
                
            cliente.save()            
            cliente_creado = True
        except Exception as e: 
            print(e)
    return cliente_creado                

@permission_required('App_Farmacia.add_cliente')
def cliente_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = ClienteModelForm(datosFormulario)
    if (request.method == 'POST'):
        cliente_creado = crear_cliente_modelo(formulario)
        
        if (cliente_creado):
            messages.success(request, 'Se ha anyadido el cliente '+formulario.cleaned_data.get('first_name')+" correctamente")
            return redirect("lista_clientes")       

    return render(request, 'cliente/create_cliente.html', {'formulario':formulario})

@permission_required('App_Farmacia.view_cliente')
def cliente_buscar(request):
    formulario = BusquedaClienteForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        clientes = Cliente.objects.all()
        clientes = clientes.filter(usuario__first_name__contains=texto).all()
        return render(request, 'cliente/cliente_busqueda.html',{'clientes_mostrar':clientes, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
@permission_required('App_Farmacia.view_cliente')
def cliente_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaClienteForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSclientes = Cliente.objects.all()
            
            first_name = formulario.cleaned_data.get('first_name')
            email = formulario.cleaned_data.get('email')
            direccion_cli = formulario.cleaned_data.get('direccion_cli')
            date_joined = formulario.cleaned_data.get('date_joined')
            telefono_cli = formulario.cleaned_data.get('telefono_cli')
            productos_favoritos = formulario.cleaned_data.get('productos_favoritos')
            votacion_prod = formulario.cleaned_data.get('votacion_prod')
                
            if (first_name != ""):
                QSclientes = QSclientes.filter(usuario__first_name__contains=first_name)
                mensaje_busqueda += "Nombre o que contenga la palabra "+first_name+"\n"
                
            if (email != ""):
                QSclientes = QSclientes.filter(usuario__email=email)
                mensaje_busqueda += "Email que sea igual a "+email+"\n"
                
            if (direccion_cli != ""):
                QSclientes = QSclientes.filter(direccion_cli__contains=direccion_cli)
                mensaje_busqueda += "Direccion o que contenga la palabra "+direccion_cli+"\n"
            
            if (not date_joined is None):
                mensaje_busqueda += f"Fecha de registro que sea igual o mayor a "+str(date_joined)+"\n"
                QSclientes = QSclientes.filter(usuario__date_joined__gte = date_joined)
            
            if (not telefono_cli is None):
                mensaje_busqueda += f"Telefono que sea igual a "+str(telefono_cli)+"\n"
                QSclientes = QSclientes.filter(telefono_cli = telefono_cli)
            
            if (not productos_favoritos is None):
                QSclientes = QSclientes.filter(productos_favoritos=productos_favoritos)
                mensaje_busqueda += "Que el producto favorito sea "+productos_favoritos.nombre_prod+"\n"
            
            if (not votacion_prod is None):
                QSclientes = QSclientes.filter(votacion_prod=votacion_prod)
                mensaje_busqueda += "Que el producto que ha votado sea  "+votacion_prod.nombre_prod+"\n"
            
            clientes = QSclientes.all()
            
            return render(request, 'cliente/cliente_busqueda.html', {'clientes_mostrar':clientes, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaClienteForm(None)
        
    return render(request, 'cliente/busqueda_avanzada_cliente.html',{'formulario':formulario})    
    
@permission_required('App_Farmacia.change_cliente')    
def cliente_editar(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = ClienteEditarModelForm(datosFormulario, instance = cliente)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado el cliente {cliente.usuario.first_name} correctamente")
                return redirect('lista_clientes')
            except Exception as error:
                pass
    return render(request, 'cliente/actualizar_cliente.html', {'formulario': formulario, 'cliente':cliente})    
        
@permission_required('App_Farmacia.delete_cliente')      
def cliente_eliminar(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    try:
        cliente.delete()
        messages.success(request, f"Se ha eliminado el cliente {cliente.usuario.first_name} correctamente.")
    except:
        pass
    return redirect('lista_clientes')

















def crear_promocion_modelo(formulario):
        
    promocion_creada = False
    #Comprueba si el formulario es válido
    if formulario.is_valid():
        try:
            #Guarda el producto en la base de datos
            formulario.save()
            promocion_creada = True
        except:
            pass
    return promocion_creada                

@permission_required('App_Farmacia.add_promocion')
def promocion_create(request):
    
    # Si la petición es GET se creará el formulario Vacio
    # Si la petición es POST se creará el formulario con Datos
    datosFormulario = None
    if (request.method == 'POST'):
        datosFormulario = request.POST
    
    formulario = PromocionModelForm(datosFormulario)
    if (request.method == 'POST'):
        promocion_creada = crear_promocion_modelo(formulario)
        if (promocion_creada):
            messages.success(request, 'Se ha anyadido la promocion '+formulario.cleaned_data.get('nombre_promo')+" correctamente")
            return redirect("lista_promociones")       

    return render(request, 'promocion/create_promocion.html', {'formulario':formulario})

def promocion_buscar(request):
    formulario = BusquedaPromocionForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get('textoBusqueda')
        promociones = Promocion.objects.all()
        promociones = promociones.filter(Q(nombre_promo__contains=texto) | Q(descripcion_promo__contains=texto)).all()
        return render(request, 'promocion/promocion_busqueda.html',{'promociones_mostrar':promociones, 'texto_busqueda':texto})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def promocion_buscar_avanzado(request):
    
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSpromociones = Promocion.objects.all()
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            nombre_promo = formulario.cleaned_data.get('nombre_promo')
            descripcion_promo = formulario.cleaned_data.get('descripcion_promo')
            valor_promo = formulario.cleaned_data.get('valor_promo')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            cliente_promo = formulario.cleaned_data.get('cliente_promo')
            
            if (textoBusqueda != ""):
                QSvotaciones = QSvotaciones.filter(Q(nombre_promo__contains=textoBusqueda) | Q(descripcion_promo__contains=textoBusqueda))
                mensaje_busqueda += "Que su comentario sea o contenga la palabra "+textoBusqueda+"\n"
                
            if (nombre_promo != ""):
                QSpromociones = QSpromociones.filter(nombre_promo__contains=nombre_promo)
                mensaje_busqueda += "Nombre sea o que contenga la palabra "+nombre_promo+"\n"
                
            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+date.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                QSpromociones = QSpromociones.filter(fecha_fin_promo__gte=fechaDesde)
            
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+date.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                QSpromociones = QSpromociones.filter(fecha_fin_promo__lte=fechaHasta)
            
                
            if (descripcion_promo != ""):
                QSpromociones = QSpromociones.filter(descripcion_promo__contains=descripcion_promo)
                mensaje_busqueda += "Descripcion sea o que contenga la palabra "+descripcion_promo+"\n"
            
            if (not valor_promo is None):
                QSpromociones = QSpromociones.filter(valor_promo__gte=valor_promo)
                mensaje_busqueda += "Promociones que sean mayor a "+valor_promo+"\n"
                
            if (not cliente_promo is None):
                QSpromociones = QSpromociones.filter(cliente_promo=cliente_promo)
                mensaje_busqueda += "Cliente/s que tienen promociones "+cliente_promo.usuario.first_name+"\n"
        
            
            promociones = QSpromociones.all()
            
            return render(request, 'promocion/promocion_busqueda.html', {'promociones_mostrar':promociones, 'texto_busqueda':mensaje_busqueda})  
                      
    else:
        formulario = BusquedaAvanzadaPromocionForm(None)
        
    return render(request, 'promocion/busqueda_avanzada_promocion.html',{'formulario':formulario})    
    
    
@permission_required('App_Farmacia.change_promocion')
def promocion_editar(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario = None
    
    if (request.method == "POST"):
        datosFormulario = request.POST
        
    formulario = PromocionModelForm(datosFormulario, instance = promocion)
    
    if (request.method == "POST"):
        
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                messages.success(request, f"Se ha editado la promocion {promocion.nombre_promo} correctamente")
                return redirect('lista_promociones')
            except Exception as error:
                pass
    return render(request, 'promocion/actualizar_promocion.html', {'formulario': formulario, 'promocion':promocion})    
        
    
@permission_required('App_Farmacia.delete_promocion')
def promocion_eliminar(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, f"Se ha eliminado la promocion {promocion.nombre_promo} correctamente.")
    except:
        pass
    return redirect('lista_promociones')






@permission_required('App_Farmacia.view_cliente')
def administradores_lista(request):
    administradores = Administrador.objects.select_related('usuario').all()
    
    return render(request, 'admin/lista_administradores.html', {'administradores': administradores})


@permission_required('App_Farmacia.view_cliente')
def clientes_lista(request):
    clientes = Cliente.objects.select_related('usuario').prefetch_related('productos_favoritos', 'votacion_prod').all()
    
    return render(request, 'cliente/lista_clientes.html', {'clientes': clientes})


def promociones_lista(request):
    promociones = Promocion.objects.select_related('cliente_promo').all()
    
    return render(request, 'promocion/lista_promociones.html', {'promociones': promociones})


def votaciones_lista(request):
    votaciones = Votacion.objects.select_related('voto_producto', 'voto_cliente').all()
    
    return render(request, 'votacion/lista_votaciones.html', {'votaciones': votaciones})

@permission_required('App_Farmacia.view_empleado')
def empleados_lista(request):
    empleados = Empleado.objects.select_related('farm_emp', 'usuario').all()
    
    return render(request, 'empleado/lista_empleados.html', {'empleados':empleados})

def farmacias_lista(request):
    farmacias = Farmacia.objects.all()
    
    return render(request, 'farmacia/lista_farmacias.html', {'farmacias':farmacias})

@permission_required('App_Farmacia.view_gerente')
def gerentes_lista(request):
    gerentes = Gerente.objects.select_related('gerente_farm','usuario').all()
    
    return render(request, 'gerente/lista_gerentes.html', {'gerentes':gerentes})

def productos_lista(request):
    productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod').all()

    return render(request, 'producto/lista_productos.html', {'productos':productos})




def farmacia_ordenada_fecha(request):
    datos = DatosFarmacia.objects.select_related("farmacia_datos").order_by("fecha_creacion").all()
    return render(request, 'farmacia/farmaciaydatos.html', {'farmacias_fecha':datos})

def gerente_nombre(request, nombre_introducido):
    gerentes = Gerente.objects.select_related('gerente_farm', 'usuario').filter(usuario__first_name__contains=nombre_introducido)
    return render(request, 'gerente/gerentes_filtrado_nombre.html', {'gerentes':gerentes})

def farmacias_con_gerentes(request):
    farmacias = Farmacia.objects.select_related('gerente').all()
    return render(request, 'farmacia/farmaciaygerentes.html', {'farmacias':farmacias, 'gerente':request})

def productos_con_proveedores(request):
    productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod').all()
    return render(request, 'producto/producto_proveedores.html', {'productos':productos})

def empleado_compras(request):
    compras = Compra.objects.select_related("empleado_compra").prefetch_related("producto_compra").all()
    return render(request, 'empleado/empleado_y_compras.html', {'compras_empleados':compras})

def detalle_compra(request):
    compra = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').all()
    return render(request, 'compra/compra_detalle_empleado.html', {'compras':compra})

def detalle_compra_id(request, id_compra):
    compra = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').filter(id=id_compra)
    return render(request, 'compra/compraydetalles_id.html', {'compras_id':compra})

def clientes_productosfavoritos(request):
    clientes = Cliente.objects.select_related('usuario').prefetch_related('productos_favoritos').all()
    return render(request, 'cliente/cliente_prod_fav.html', {'clientes':clientes})

def empleado_salariosuperior(request, cantidad_salario):
    empleados = Empleado.objects.select_related('usuario', 'farm_emp').filter(salario__gte=cantidad_salario).all()   #IMPORTANTE gte = mayor o igual que  y  lte = menor o igual que
    return render(request, 'empleado/empleados_salario_superior.html', {'empleados':empleados})

def productos_disponibles_farmacia_especifica(request, id_farmacia):
    farmacia = Farmacia.objects.get(id=id_farmacia)
    productos = Producto.objects.filter(farmacia_prod = farmacia).order_by('-precio').all()
    return render(request, 'farmacia/farmaciayproductos.html', {'productos':productos, 'farmacia': farmacia})

def compras_entre_fechas(request, fecha_inicio, fecha_fin):
    fecha_inicio = dt.strptime(fecha_inicio, '%Y-%m-%d').date()
    fecha_fin = dt.strptime(fecha_fin, '%Y-%m-%d').date()
    compras = Compra.objects.select_related('cliente_compra', 'empleado_compra').prefetch_related('producto_compra').filter(fecha_compra__gte=fecha_inicio, fecha_compra__lte=fecha_fin)
    return render(request, 'compra/compra_entre_fechas.html', {'compras':compras})

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request, exception=None):
    return render(request, 'errores/500.html',None,None,500)


def ultimo_voto_producto_concreto(request, producto_id):

    ultimo_voto = Votacion.objects.select_related("voto_producto", "voto_cliente").filter(voto_producto__id=producto_id).order_by('-fecha_votacion')[:1].get()
    return render(request, 'votacion/ultimo_voto.html', {'votacion':ultimo_voto})




def productos_con_puntuacion_3_cliente_concreto(request, cliente_id):
    cliente = Cliente.objects.select_related('usuario').prefetch_related("productos_favoritos", "votacion_prod").get(pk=cliente_id)
    
    votaciones_cliente = Votacion.objects.filter(voto_cliente=cliente, puntuacion=3).values_list('id', flat=True)
    
    productos_con_votos = Producto.objects.filter(votacion_prod__in=votaciones_cliente).all()
    
    return render(request, 'producto/productos_con_3.html', {'productos_con_votos': productos_con_votos})

    
def clientes_nunca_votaron(request):
    clientes_no_votaron = Cliente.objects.select_related('usuario').prefetch_related("productos_favoritos", "votacion_prod").filter(votacion__isnull=True).all()
    return render(request, 'cliente/clientesinvoto.html', {'clientes_no_votaron':clientes_no_votaron})    

def cuentas_bancarias_propietario_nombre(request, nombre_propietario):
    cuentas_bancarias = Pago.objects.select_related("cliente_pago", "subscripcion_pago").filter(
        Q(banco='CA') | Q(banco='UN'),Q(cliente_pago__usuario__first_name__icontains=nombre_propietario)
    )
    return render(request, 'cuentas/cuentas_bancarias.html', {'cuentas_bancarias': cuentas_bancarias})

def modelos_con_media_superior(request):    
    media_votaciones = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod").annotate(media=Avg('votacion__puntuacion'))

    productos_con_media_superior = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod").filter(media__gt=2.5)

    return render(request, 'producto.html', {'productos_con_media_superior': productos_con_media_superior})





    