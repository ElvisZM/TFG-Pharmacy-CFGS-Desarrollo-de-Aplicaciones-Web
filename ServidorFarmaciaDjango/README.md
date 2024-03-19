# APLICACION WEB FARMACIA | PROYECTO DE FIN DE GRADO




## PERMISOS API

### Administrador:

    * Permisos para todas las funciones de la aplicación al completo.

### Gerente:

    * Todos los permisos para "Empleados", "Farmacias", "Productos" y "Votaciones"

### Empleado:

    * Permisos para todas las funciones con "Clientes" excepto Eliminar.

    * Permisos para Ver los "Productos" y "Farmacias".

    * Todos los permisos para "Votaciones".

### Cliente:

    * Todos los permisos para "Votaciones".

    * Permisos para Ver los "Productos" y "Farmacias".







## CRUD | "PRODUCTOS"



URLs y VIEWS:

    * CREATE:
        
        path('producto/create',views.producto_create,name='producto_create')

    * BÚSQUEDA RÁPIDA:

        path('producto/buscar/',views.producto_buscar, name='producto_buscar')

    * BÚSQUEDA AVANZADA:
        
        path('producto/buscar/avanzado/',views.producto_buscar_avanzado, name='producto_buscar_avanzado'),

    * EDITAR:

        path('producto/editar/<int:producto_id>',views.producto_editar, name='producto_editar')

    * ELIMINAR:

        path('producto/eliminar/<int:producto_id>',views.producto_eliminar, name='producto_eliminar')

    * LISTA:

        path('productos/lista',views.productos_lista, name='lista_productos')


TEMPLATES:


    * CREATE:

        'producto/create_producto.html'

    * BUSQUEDA RÁPIDA:

        'producto/producto_busqueda.html'

    * BUSQUEDA AVANZADA:

        'producto/producto_busqueda.html'

    * EDITAR:

        'producto/actualizar_promocion.html'

    * ELIMINAR Y LISTA:

        'producto/lista_productos.html'


FORMULARIOS:


    * CREATE:
    
        class ProductoModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaProductoForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaProductoForm(forms.Form)


VALIDACIONES:


    * Comprobamos que no existe un producto con ese nombre

    * Comprobamos que la descripción tiene al menos 10 carácteres.

    * Comprobamos que el precio está puesto en su formato con decimales (float)

    * Comprobamos que al menos seleccione un Proveedor



## CRUD | "GERENTES"



URLs y VIEWS:

    * CREATE:
        
        path('gerente/create',views.gerente_create, name='gerente_create')

    * BÚSQUEDA RÁPIDA:

        path('gerente/buscar/',views.gerente_buscar, name='gerente_buscar')

    * BÚSQUEDA AVANZADA:
        
        path('gerente/buscar/avanzado/',views.gerente_buscar_avanzado, name='gerente_buscar_avanzado')

    * EDITAR:

        path('gerente/editar/<int:gerente_id>',views.gerente_editar, name='gerente_editar')

    * ELIMINAR:

        path('gerente/eliminar/<int:gerente_id>',views.gerente_eliminar, name='gerente_eliminar')

    * LISTA:

       path('gerentes/lista',views.gerentes_lista, name='lista_gerentes')


TEMPLATES:


    * CREATE:

        'gerente/create_gerente.html'

    * BÚSQUEDA RÁPIDA:

        'gerente/gerente_busqueda.html'

    * BÚSQUEDA AVANZADA:

        'gerente/busqueda_avanzada_gerente.html'

    * EDITAR:

        'gerente/actualizar_gerente.html'

    * ELIMINAR Y LISTA:

        'gerente/lista_gerentes.html'


FORMULARIOS:


    * CREATE:
    
        class GerenteModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaGerenteForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaGerenteForm(forms.Form)


VALIDACIONES:


    * Comprobamos que no exista un gerente con ese nombre

    * Comprobamos que se inserte un correo

    * Comprobamos que la fecha de inicio de gestion no sea mayor a la de hoy.

    * Comprobamos que inserte una farmacia a gestionar 

    * Comprobamos que la farmacia no tenga ya a un gerente que la gestione



## CRUD | "FARMACIAS"



URLs y VIEWS:

    * CREATE:
        
        path('farmacia/create',views.farmacia_create, name='farmacia_create'),

    * BÚSQUEDA RÁPIDA:

        path('farmacia/buscar/',views.farmacia_buscar, name='farmacia_buscar'),

    * BÚSQUEDA AVANZADA:
        
        path('farmacia/buscar/avanzado/',views.farmacia_buscar_avanzado, name='farmacia_buscar_avanzado'),

    * EDITAR:

        path('farmacia/editar/<int:farmacia_id>',views.farmacia_editar, name='farmacia_editar'),

    * ELIMINAR:

        path('farmacia/eliminar/<int:farmacia_id>',views.farmacia_eliminar, name='farmacia_eliminar'),

    * LISTA:

        path('farmacias/lista',views.farmacias_lista, name='lista_farmacias'),


TEMPLATES:


    * CREATE:

        'farmacia/create_farmacia.html'

    * BÚSQUEDA RÁPIDA:

        'farmacia/farmacia_busqueda.html'

    * BÚSQUEDA AVANZADA:

        'farmacia/busqueda_avanzada_farmacia.html'

    * EDITAR:

        'farmacia/actualizar_farmacia.html'

    * ELIMINAR Y LISTA:

        'farmacia/lista_farmacias.html'


FORMULARIOS:


    * CREATE:
    
        class FarmaciaModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaFarmaciaForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaFarmaciaForm(forms.Form)


VALIDACIONES:


    * Comprobamos que no exista una farmacia con ese nombre

    * Comprobamos que se inserte una dirección

    * Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.

    * Comprobamos que el numero no exista en otra farmacia.





## CRUD | "EMPLEADOS"



URLs y VIEWS:

    * CREATE:
        
        path('empleado/create',views.empleado_create, name='empleado_create'),

    * BÚSQUEDA RÁPIDA:

        path('empleado/buscar/',views.empleado_buscar, name='empleado_buscar'),

    * BÚSQUEDA AVANZADA:
        
        path('empleado/buscar/avanzado/',views.empleado_buscar_avanzado, name='empleado_buscar_avanzado'),

    * EDITAR:

        path('empleado/editar/<int:empleado_id>',views.empleado_editar, name='empleado_editar'),

    * ELIMINAR:

        path('empleado/eliminar/<int:empleado_id>',views.empleado_eliminar, name='empleado_eliminar'),

    * LISTA:

        path('empleados/lista',views.empleados_lista, name='lista_empleados'),


TEMPLATES:


    * CREATE:

        'empleado/create_empleado.html'

    * BÚSQUEDA RÁPIDA:

        'empleado/empleado_busqueda.html'

    * BÚSQUEDA AVANZADA:

        'empleado/busqueda_avanzada_empleado.html'

    * EDITAR:

        'empleado/actualizar_empleado.html'

    * ELIMINAR Y LISTA:

        'empleado/lista_empleados.html'


FORMULARIOS:


    * CREATE:
    
        class EmpleadoModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaEmpleadoForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaEmpleadoForm(forms.Form)


VALIDACIONES:


    * Comprobamos que no exista un empleado con ese nombre

    * Comprobamos que se inserte un cargo para el empleado.

    * Comprobamos que se inserte un salario para el empleado.

    * Comprobamos que se le asigne una farmacia al empleado.



## CRUD | "VOTACIONES"



URLs y VIEWS:

    * CREATE:
        
        path('votacion/create',views.votacion_create, name='votacion_create'),

    * BÚSQUEDA RÁPIDA:

        path('votacion/buscar/',views.votacion_buscar, name='votacion_buscar'),

    * BÚSQUEDA AVANZADA:
        
        path('votacion/buscar/avanzado/',views.votacion_buscar_avanzado, name='votacion_buscar_avanzado'),

    * EDITAR:

        path('votacion/editar/<int:votacion_id>',views.votacion_editar, name='votacion_editar'),

    * ELIMINAR:

        path('votacion/eliminar/<int:votacion_id>',views.votacion_eliminar, name='votacion_eliminar'),

    * LISTA:

        path('votaciones/lista',views.votaciones_lista, name='lista_votaciones'),


TEMPLATES:


    * CREATE:

        'votacion/create_votacion.html'

    * BÚSQUEDA RÁPIDA:

        'votacion/votacion_busqueda.html'

    * BÚSQUEDA AVANZADA:

        'votacion/busqueda_avanzada_votacion.html'

    * EDITAR:

        'votacion/actualizar_votacion.html'

    * ELIMINAR Y LISTA:

        'votacion/lista_votaciones.html'


FORMULARIOS:


    * CREATE:
    
        class VotacionModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaVotacionForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaVotacionForm(forms.Form)


VALIDACIONES:


    * Comprobamos que el comentario tiene al menos 10 carácteres.

    * Comprobamos que seleccione un Producto

    * Comprobamos que seleccione un cliente



## CRUD | "CLIENTES"



URLs y VIEWS:

    * CREATE:
        
        path('cliente/create',views.cliente_create, name='cliente_create'),

    * BÚSQUEDA RÁPIDA:

        path('cliente/buscar/',views.cliente_buscar, name='cliente_buscar'),

    * BÚSQUEDA AVANZADA:
        
        path('cliente/buscar/avanzado/',views.cliente_buscar_avanzado, name='cliente_buscar_avanzado'),

    * EDITAR:

        path('cliente/editar/<int:cliente_id>',views.cliente_editar, name='cliente_editar'),

    * ELIMINAR:

        path('cliente/eliminar/<int:cliente_id>',views.cliente_eliminar, name='cliente_eliminar'),

    * LISTA:

        path('clientes/lista',views.clientes_lista, name='lista_clientes'),


TEMPLATES:


    * CREATE:

        'cliente/create_cliente.html'

    * BÚSQUEDA RÁPIDA:

        'cliente/cliente_busqueda.html'

    * BÚSQUEDA AVANZADA:

        'cliente/busqueda_avanzada_cliente.html'

    * EDITAR:

        'cliente/actualizar_cliente.html'

    * ELIMINAR Y LISTA:

        'cliente/lista_clientes.html'


FORMULARIOS:


    * CREATE:
    
        class ClienteModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaClienteForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaClienteForm(forms.Form)


VALIDACIONES:


    * Comprobamos que no exista un cliente con ese nombre

    * Comprobamos que se inserte una dirección para el cliente.

    * Comprobamos que el numero tenga 9 digitos, sea espanyol y no exista ya.

    * Comprobamos que el numero no exista en otro cliente.





## EXAMEN CRUD | "PROMOCION"

14/12/2023

URLs y VIEWS:

    * CREATE:
        
        path('promocion/create',views.promocion_create, name='promocion_create')

    * BÚSQUEDA RÁPIDA:

        path('promocion/buscar/',views.promocion_buscar, name='promocion_buscar')

    * BÚSQUEDA AVANZADA:
        
        path('promocion/buscar/avanzado/',views.promocion_buscar_avanzado, name='promocion_buscar_avanzado')

    * EDITAR:

        path('promocion/editar/<int:promocion_id>',views.promocion_editar, name='promocion_editar')

    * ELIMINAR:

        path('promocion/eliminar/<int:promocion_id>',views.promocion_eliminar, name='promocion_eliminar')

    * LISTA:

        path('promociones/lista',views.promociones_lista, name='lista_promociones')


TEMPLATES:


    * CREATE:

        'promocion/create_promocion.html'

    * BÚSQUEDA RÁPIDA:

        'promocion/promocion_busqueda.html'

    * BÚSQUEDA AVANZADA:

        'promocion/busqueda_avanzada_promocion.html'

    * EDITAR:

        'promocion/actualizar_promocion.html'

    * ELIMINAR Y LISTA:

        'promocion/lista_promociones.html'


FORMULARIOS:


    * CREATE:
    
        class PromocionModelForm(ModelForm)

    * BÚSQUEDA RÁPIDA:

        class BusquedaPromocionForm(forms.Form)

    * BÚSQUEDA AVANZADA:
    
        class BusquedaAvanzadaPromocionForm(forms.Form)


VALIDACIONES:


    * Nombre de la Promoción es única

    * Comprobamos que la descripción tiene al menos 100 carácteres.

    * Comprobamos que el cliente no tenga ya la misma promoción aplicada

    * Comprobamos que el valor del descuento sea un entero entre 0 y 100

    * Comprobamos la fecha de expiración no sea inferior a la actual.















## PEQUEnyA ANOTACIÓN, NO OLVIDAR!!!:

    En las templates, se puede acceder a los datos de cualquier campo siempre y cuando tengan relacion entre ellos.

    En el siguiente caso, observamos que compra tiene dos relaciones ForeignKey(ManyToOne) con Cliente y Empleado. 
    
    También tiene una relacion ManyToMany con Producto a través de DetalleCompra. 
    
    Luego DetalleCompra tiene dos relaciones ForeignKey(ManyToOne) con Compra y Producto.

    Como podemos observar existe una relacion inversa entre Compra y DetalleCompra.

    class Compra(models.Model):
        fecha_compra = models.DateField(null=False, blank=False)
        cliente_compra = models.ForeignKey(Cliente, on_delete=models.CASCADE)
        producto_compra = models.ManyToManyField(Producto, through='DetalleCompra', related_name="producto_compra")
        empleado_compra = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    class DetalleCompra(models.Model):
        cantidad_prod_comprado = models.IntegerField(null=True, blank=True)
        precio_ud = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
        compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
        producto_detalle = models.ForeignKey(Producto, on_delete=models.CASCADE)


    Si quisieramos acceder desde compra a un dato que no esta en nuestro modelo, si es una ForeignKey, podemos acceder 
    facilmente recorriendo el nombre de la variable que recoge esta relacion con:
    
    "compra.empleado_compra"

    Esto nos situa en el campo que la relaciona, en este caso Empleado. Una vez estamos situados en ese campo, es tan 
    fácil como seleccionar que información queremos mostrar (en mi caso nombre del empleado) y la agregamos.

    "compra.empleado_compra.nombre_emp"

    Si quisieramos acceder desde compra a un dato de DetalleCompra, al ser esta una relación inversa, lo que se me 
    ocurrio fue recoger todos los datos Producto mediante producto_compra y dentro de producto hacer una relacion inversa para coger los datos de DetalleCompra usando 
    
    "for det in producto.detallecompra_set.all".
    
    De este modo puedo mostrar fácilmente los datos que necesite.


    <div>
        <h2> Fecha Compra: {{ compra.fecha_compra|date:"d-m-Y" }}</h2>
        <h2> Cliente: {{ compra.cliente_compra.nombre_cli|truncatewords:1 }} </h2>
        {% for producto in compra.producto_compra.all %}
            <h2>Producto comprado: {{ producto.nombre_prod|truncatewords:2 }} </h2>
            {%for det in producto.detallecompra_set.all %}
                <h2>Cantidad: {{ det.cantidad_prod_comprado }}
                <h2>Precio Unidad: {{ det.precio_ud }} </h2>
            {% endfor %}
        {% endfor %}
        <h2> Empleado: {{ compra.empleado_compra.nombre_emp|truncatewords:2 }} </h2>
    </div> 


