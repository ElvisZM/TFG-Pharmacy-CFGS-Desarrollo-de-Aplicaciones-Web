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
from .forms import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
from oauth2_provider.models import AccessToken
from datetime import date, timedelta
    






class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = int(request.data.get('rol'))
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"),
                        first_name = serializers.data.get("first_name"),
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Cliente') 
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create( usuario = user, direccion_cli = serializers.data.get("domicilio"), telefono_cli = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    cliente.save()
                    
                elif(rol == Usuario.EMPLEADO):
                    grupo = Group.objects.get(name='Empleado') 
                    grupo.user_set.add(user)
                    empleado = Empleado.objects.create( usuario = user, direccion_emp = serializers.data.get("domicilio"), telefono_emp = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    empleado.save()
                
                elif(rol == Usuario.GERENTE):
                    grupo = Group.objects.get(name='Gerente') 
                    grupo.user_set.add(user)
                    gerente = Gerente.objects.create( usuario = user, direccion_ger = serializers.data.get("domicilio"), telefono_ger = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    gerente.save()
                    
                elif(rol == Usuario.ADMINISTRADOR):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    cliente = Administrador.objects.create( usuario = user, direccion_admin = serializers.data.get("domicilio"), telefono_admin = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    cliente.save()
                    
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)






class registrar_usuario_google(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistroGoogle
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistroGoogle(data=request.data)
        if serializers.is_valid():
            try:
                rol = int(request.data.get('rol'))
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"),
                        first_name = serializers.data.get("first_name"),
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol == Usuario.CLIENTE):
                    domicilio = self.request.data.get("domicilio")
                    telefono = 0
                    fecha_cumple = self.request.data.get("birthday_date")
                    grupo = Group.objects.get(name='Cliente') 
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create( usuario = user, direccion_cli = domicilio, telefono_cli = telefono, birthday_date = fecha_cumple)
                    cliente.save()
                    
                elif(rol == Usuario.EMPLEADO):
                    grupo = Group.objects.get(name='Empleado') 
                    grupo.user_set.add(user)
                    empleado = Empleado.objects.create( usuario = user, direccion_emp = serializers.data.get("domicilio"), telefono_emp = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    empleado.save()
                
                elif(rol == Usuario.GERENTE):
                    grupo = Group.objects.get(name='Gerente') 
                    grupo.user_set.add(user)
                    gerente = Gerente.objects.create( usuario = user, direccion_ger = serializers.data.get("domicilio"), telefono_ger = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    gerente.save()
                    
                elif(rol == Usuario.ADMINISTRADOR):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    cliente = Administrador.objects.create( usuario = user, direccion_admin = serializers.data.get("domicilio"), telefono_admin = serializers.data.get("telefono"), birthday_date = serializers.data.get("birthday_date"))
                    cliente.save()
                    
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
def obtener_usuario_token(request,token):
    
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)
    

class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def put(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        try:
            return UploadedFile.objects.get(pk=pk)
        except UploadedFile.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def producto_list(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def producto_list_mejorado(request):
    productos = Producto.objects.all()
    serializer_mejorado = ProductoSerializerMejorado(productos, many=True)
    return Response(serializer_mejorado.data)

@api_view(['GET'])
def producto_buscar(request):
    if (request.user.has_perm('AppFarmacia.view_producto')):
        formulario = BusquedaProductoForm(request.query_params)
        if (formulario.is_valid()):
            texto = formulario.data.get('textoBusqueda')
            productos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
            productos = productos.filter(Q(nombre_prod__contains=texto) | Q(descripcion__contains=texto)).all()
            serializer = ProductoSerializerMejorado(productos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])    
def producto_busqueda_avanzada(request):
    if (len(request.GET) > 0):
        formulario = BusquedaAvanzadaProductoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "\nSe ha buscado por los siguientes valores:\n"
            
            QSproductos = Producto.objects.select_related('farmacia_prod').prefetch_related('prov_sum_prod')
            
            nombre_prod = formulario.cleaned_data.get('nombre_prod')
            descripcion = formulario.cleaned_data.get('descripcion')
            precio = formulario.cleaned_data.get('precio')
            stock = formulario.cleaned_data.get('stock')
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
            
            serializer = ProductoSerializerMejorado(productos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def empleado_list(request):
    if(request.user.has_perm("App_Farmacia.add_empleado")):
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)
    else:
       return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def empleado_list_mejorado(request):
    if(request.user.has_perm("App_Farmacia.view_empleado")):
        empleados = Empleado.objects.all()
        serializer_mejorado = EmpleadoSerializerMejorado(empleados, many=True)
        return Response(serializer_mejorado.data)
    else:
       return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def votacion_list_mejorado(request):
    votaciones = Votacion.objects.all()
    serializer_mejorado = VotacionSerializerMejorado(votaciones, many=True)
    return Response(serializer_mejorado.data)

@api_view(['GET'])
def farmacia_list(request):
    farmacias = Farmacia.objects.all()
    serializer = FarmaciaSerializer(farmacias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def proveedor_list(request):
    if(request.user.has_perm("App_Farmacia.view_proveedor")):
        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)
    else:
       return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def producto_create(request):
    if(request.user.has_perm("App_Farmacia.add_producto")):
        producto_serializers = ProductoSerializerCreate(data=request.data)
        if producto_serializers.is_valid():
            try:
                producto_serializers.save()
                return Response("Producto CREADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(error)
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
                return Response(producto_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])  
def producto_obtener(request, producto_id):
    producto = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod")
    producto = producto.get(id=producto_id)
    serializer = ProductoSerializerMejorado(producto)
    return Response(serializer.data)  
  
    
@api_view(['PUT'])
def producto_editar(request, producto_id):
    if(request.user.has_perm("App_Farmacia.change_producto")):
        producto = Producto.objects.get(id=producto_id)
        productoCreateSerializer = ProductoSerializerCreate(instance=producto, data=request.data)
        if productoCreateSerializer.is_valid():
            try:
                productoCreateSerializer.save()
                return Response("Producto EDITADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        else:
            return Response(productoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)



@api_view(['PATCH'])
def producto_actualizar_nombre(request, producto_id):
    if(request.user.has_perm("App_Farmacia.change_producto")):

        serializers = ProductoSerializerCreate(data=request.data)
        producto = Producto.objects.get(id=producto_id)
        serializers = ProductoSerializerActualizarNombre(data=request.data, instance=producto)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response("Producto EDITADO")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)

        
    
@api_view(['DELETE'])
def producto_eliminar(request, producto_id):
    if(request.user.has_perm("App_Farmacia.delete_producto")):

        producto = Producto.objects.get(id=producto_id)
        try:
            producto.delete()
            return Response("Producto DELETEADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)

 
 




@api_view(['GET'])
def farmacia_buscar(request):
    formulario = BusquedaFarmaciaForm(request.query_params)
    if (formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        farmacias = Farmacia.objects.all()
        farmacias = farmacias.filter(Q(nombre_farm__contains=texto) | Q(direccion_farm__contains=texto)).all()
        serializer = FarmaciaSerializer(farmacias, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def farmacia_create(request):
    if(request.user.has_perm("App_Farmacia.add_farmacia")):

        farmacia_serializers = FarmaciaSerializerCreate(data=request.data)
        if farmacia_serializers.is_valid():
            try:
                farmacia_serializers.save()
                return Response("Farmacia CREADA")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(error)
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(farmacia_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])  
def farmacia_obtener(request, farmacia_id):
    farmacia = Farmacia.objects.all()
    farmacia = farmacia.get(id=farmacia_id)
    serializer = FarmaciaSerializer(farmacia)
    return Response(serializer.data)  
  
    
@api_view(['PUT'])
def farmacia_editar(request, farmacia_id):
    if(request.user.has_perm("App_Farmacia.change_farmacia")):

        farmacia = Farmacia.objects.get(id=farmacia_id)
        farmaciaCreateSerializer = FarmaciaSerializerCreate(instance=farmacia, data=request.data)
        if farmaciaCreateSerializer.is_valid():
            try:
                farmaciaCreateSerializer.save()
                return Response("Farmacia EDITADA")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        else:
            return Response(farmaciaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)




@api_view(['PATCH'])
def farmacia_actualizar_nombre(request, farmacia_id):
    if(request.user.has_perm("App_Farmacia.change_farmacia")):

        serializers = FarmaciaSerializerCreate(data=request.data)
        farmacia = Farmacia.objects.get(id=farmacia_id)
        serializers = FarmaciaSerializerActualizarNombre(data=request.data, instance=farmacia)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response("Farmacia EDITADA")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


    
    
@api_view(['DELETE'])
def farmacia_eliminar(request, farmacia_id):
    if(request.user.has_perm("App_Farmacia.change_farmacia")):

        farmacia = Farmacia.objects.get(id=farmacia_id)
        try:
            farmacia.delete()
            return Response("Farmacia DELETEADA")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


 
 

 

 
 
 
    

@api_view(['GET'])    
def empleado_busqueda_avanzada(request):
    if(request.user.has_perm("App_Farmacia.view_empleado")):

        if (len(request.query_params) > 0):
            formulario = BusquedaAvanzadaEmpleadoForm(request.query_params)
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
                
                serializer = EmpleadoSerializerMejorado(empleados, many=True)
                return Response(serializer.data)
            else:
                return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)

 
 
 
 
 
    
@api_view(['GET']) 
def clientes_list(request):
    if(request.user.has_perm("App_Farmacia.view_cliente")):

        clientes = Cliente.objects.all()
        serializer = ClienteSerializerMejorado(clientes, many=True)
        return Response(serializer.data)

    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)









@api_view(['POST'])
def votacion_create(request):
    if(request.user.has_perm("App_Farmacia.add_votacion")):

        votacion_serializers = VotacionSerializerCreate(data=request.data)
        if votacion_serializers.is_valid():
            try:
                votacion_serializers.save()
                return Response("Votacion CREADA")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(error)
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(votacion_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])  
def votacion_obtener(request, votacion_id):
    votacion = Votacion.objects.select_related("voto_producto", "voto_cliente")
    votacion = votacion.get(id=votacion_id)
    serializer = VotacionSerializerMejorado(votacion)
    return Response(serializer.data)  
  
    
@api_view(['PUT'])
def votacion_editar(request, votacion_id):
    if(request.user.has_perm("App_Farmacia.change_votacion")):
        votacion = Votacion.objects.get(id=votacion_id)
        votacionCreateSerializer = VotacionSerializerCreate(instance=votacion, data=request.data)
        if votacionCreateSerializer.is_valid():
            try:
                votacionCreateSerializer.save()
                return Response("Votacion EDITADA")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        else:
            return Response(votacionCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def votacion_buscar(request):
    formulario = BusquedaVotacionForm(request.query_params)
    if (formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        votaciones = Votacion.objects.all()
        votaciones = votaciones.filter(Q(puntuacion__contains=texto) | Q(comenta_votacion__contains=texto)).all()
        serializer = VotacionSerializerMejorado(votaciones, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])    
def votacion_busqueda_avanzada(request):
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
            
            serializer = VotacionSerializerMejorado(votaciones, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def votacion_actualizar_puntuacion(request, votacion_id):
    if(request.user.has_perm("App_Farmacia.change_votacion")):

        serializers = VotacionSerializerCreate(data=request.data)
        votacion = Votacion.objects.get(id=votacion_id)
        serializers = VotacionSerializerActualizarPuntuacion(data=request.data, instance=votacion)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response("Votacion EDITADO")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)

    
    
@api_view(['DELETE'])
def votacion_eliminar(request, votacion_id):
    if(request.user.has_perm("App_Farmacia.delete_votacion")):
        votacion = Votacion.objects.get(id=votacion_id)
        try:
            votacion.delete()
            return Response("Votacion DELETEADA")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)




@api_view(['GET']) 
def promociones_list(request):
    promociones = Promocion.objects.all()
    serializer = PromocionSerializerMejorado(promociones, many=True)
    return Response(serializer.data)






@api_view(['GET'])
def es_cumpleanyos_elegible(cliente):
    if cliente.fecha_nacimiento and cliente.fecha_registro:
        hoy = date.today()
        cumpleanyos_cliente = cliente.fecha_nacimiento.replace(year=hoy.year)
        if cumpleanyos_cliente > hoy and (cumpleanyos_cliente - cliente.fecha_registro) >= timedelta(days=30):
            return True
    return False



@api_view(['GET'])
def productos_stock_asc(request):
    productos = Producto.objects.all().order_by('stock')
    serializer_mejorado = ProductoSerializerMejorado(productos, many=True)
    return Response(serializer_mejorado.data)


@api_view(['GET'])
def productos_stock_desc(request):
    productos = Producto.objects.all().order_by('-stock')
    serializer_mejorado = ProductoSerializerMejorado(productos, many=True)
    return Response(serializer_mejorado.data)



@api_view(['POST'])
def agregar_al_carrito(request, producto_id):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            producto_anyadir = Producto.objects.get(id=producto_id)
        
            carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, realizado=False).first()
            
            
            if (carrito_usuario):
                producto_carrito = UsuarioCarrito.objects.select_related("carrito", "producto").filter(carrito = carrito_usuario, producto = producto_anyadir)
                if (producto_carrito):                    
                    producto_aumentar = UsuarioCarrito.objects.get(carrito=carrito_usuario, producto = producto_anyadir)
                    producto_aumentar.cantidad_producto += 1
                    producto_aumentar.save()
                else:
                    UsuarioCarrito.objects.create(carrito=carrito_usuario, producto = producto_anyadir, cantidad_producto=1)

            else:
                CarritoCompra.objects.create(usuario=request.user, realizado=False)
                carrito_usuario = CarritoCompra.objects.get(usuario = request.user, realizado=False)
                UsuarioCarrito.objects.create(carrito=carrito_usuario, producto = producto_anyadir,cantidad_producto = 1)
            
            return Response({"Producto agregado al carrito correctamente"}, status=status.HTTP_200_OK)

    else:
        return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def carrito_usuario(request):
    if(request.user.is_authenticated):
        
        try:
            carrito_usuario = CarritoCompra.objects.get(usuario=request.user, realizado=False) 
            serializer_mejorado = CarritoCompraSerializerMejorado(carrito_usuario)
            serializer_mejorado = serializer_mejorado.data
            total_carrito = 0
            for detalle_producto in carrito_usuario.usuariocarrito_set.all():
                precio_producto = detalle_producto.producto.precio
                cantidad_producto = detalle_producto.cantidad_producto
                total_carrito += cantidad_producto * precio_producto
            
            serializer_mejorado['total_carrito'] = total_carrito
            
            return Response(serializer_mejorado)
        
        except CarritoCompra.DoesNotExist:
            CarritoCompra.objects.create(usuario=request.user, realizado=False)
            carrito_usuario = CarritoCompra.objects.get(usuario=request.user, realizado=False)
            serializer_mejorado=CarritoCompraSerializerMejorado(carrito_usuario)
            return Response(serializer_mejorado.data)
        
    else:
        return Response("Necesita iniciar sesion", status=status.HTTP_405_METHOD_NOT_ALLOWED)        
        

@api_view(['DELETE'])
def quitar_del_carrito(request, producto_id):
    if(request.user.is_authenticated):
        if request.method == 'DELETE':
            try:
                producto_eliminar = Producto.objects.get(id=producto_id)
        
                carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, realizado=False).first()
                
                
                UsuarioCarrito.objects.select_related("carrito", "producto").filter(carrito = carrito_usuario, producto = producto_eliminar).delete()

                return Response({"Producto eliminado del carrito correctamente"}, status=status.HTTP_200_OK)
            
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def bajar_unidad_carrito(request, producto_id):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            try:
                producto_bajar_ud = Producto.objects.get(id=producto_id)
        
                carrito_usuario = CarritoCompra.objects.select_related("usuario").prefetch_related("producto_carrito").filter(usuario=request.user, realizado=False).first()
                
                producto_carrito = UsuarioCarrito.objects.select_related("carrito", "producto").filter(carrito = carrito_usuario, producto = producto_bajar_ud).first()
                
                if (producto_carrito and producto_carrito.cantidad_producto > 1):
                    producto_carrito.cantidad_producto -= 1
                    producto_carrito.save()
                    
                elif(producto_carrito and producto_carrito.cantidad_producto <= 1):
                    producto_carrito.delete()
                    
                else:
                    return Response({"Error en eliminar el producto, parece que no existe el producto seleccionado"}, status=status.HTTP_404_NOT_FOUND)

                return Response({"Se ha quitado una unidad del producto correctamente"}, status=status.HTTP_200_OK)
            
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"Necesita iniciar sesion"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET'])  
def producto_prospecto(request, producto_id):
    producto_prospecto = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod").get(id=producto_id)

    try:
    
        # Obtener el prospecto asociado al producto
        prospecto = producto_prospecto.prospecto
    
        # Serializar el prospecto y agregarlo al serializer
        serializer = ProductoProspectoSerializerMejorado(instance=prospecto)
    
        return Response(serializer.data)
    
    except Exception as error:
        Prospecto.objects.create(producto=producto_prospecto)
        
        prospecto = producto_prospecto.prospecto
        
        serializer = ProductoProspectoSerializerMejorado(instance=prospecto)
        
        return Response(serializer.data)
            
            
            
            

@api_view(['GET'])
def tratamiento_lista_mejorada(request):
    tratamientos = Tratamiento.objects.all()
    serializer_mejorado = TratamientoSerializerMejorado(tratamientos, many=True)
    return Response(serializer_mejorado.data)



@api_view(['DELETE'])
def tratamiento_eliminar(request, tratamiento_id):
    if(request.user.has_perm("App_Farmacia.delete_tratamiento")):

        tratamiento = Tratamiento.objects.get(id=tratamiento_id)
        try:
            tratamiento.delete( )
            return Response("Producto DELETEADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)





@api_view(['POST'])
def tratamiento_create(request):
    if(request.user.has_perm("App_Farmacia.add_tratamiento")):
        tratamiento_serializers = TratamientoSerializerCreate(data=request.data)
        if tratamiento_serializers.is_valid():
            try:
                tratamiento_serializers.save()
                return Response("Tratamiento CREADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                print(error)
                return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
                return Response(tratamiento_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])  
def producto_obtener(request, producto_id):
    producto = Producto.objects.select_related("farmacia_prod").prefetch_related("prov_sum_prod")
    producto = producto.get(id=producto_id)
    serializer = ProductoSerializerMejorado(producto)
    return Response(serializer.data)  
  
    
@api_view(['PUT'])
def producto_editar(request, producto_id):
    if(request.user.has_perm("App_Farmacia.change_producto")):
        producto = Producto.objects.get(id=producto_id)
        productoCreateSerializer = ProductoSerializerCreate(instance=producto, data=request.data)
        if productoCreateSerializer.is_valid():
            try:
                productoCreateSerializer.save()
                return Response("Producto EDITADO")
            except serializers.ValidationError as error:
                return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        else:
            return Response(productoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)



@api_view(['PATCH'])
def producto_actualizar_nombre(request, producto_id):
    if(request.user.has_perm("App_Farmacia.change_producto")):

        serializers = ProductoSerializerCreate(data=request.data)
        producto = Producto.objects.get(id=producto_id)
        serializers = ProductoSerializerActualizarNombre(data=request.data, instance=producto)
        if serializers.is_valid():
            try:
                serializers.save()
                return Response("Producto EDITADO")
            except Exception as error:
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Sin permisos para esta operación", status=status.HTTP_401_UNAUTHORIZED)

        
    
 