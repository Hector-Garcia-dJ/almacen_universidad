import json
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Persona, Rol, Singleton, Producto
from almacen_app.models import Persona as AlmacenPersona
from .forms import RegistroPersonaForm, SolicitudAlmacenCentralForm
from django.core.mail import send_mail
from django.db import connection
from django.contrib import messages



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            pass
    return render(request, 'login.html')


def registrar_persona(request):
    if request.method == 'POST':
        form = RegistroPersonaForm(request.POST)
        if form.is_valid():
            prototipo = Persona.objects.first().clone()
            nueva_persona = prototipo.clone()

            nueva_persona.nombre = form.cleaned_data['nombre']
            nueva_persona.apellido_paterno = form.cleaned_data['apellido_paterno']
            nueva_persona.apellido_materno = form.cleaned_data['apellido_materno']
            nueva_persona.telefono = form.cleaned_data['telefono']
            nueva_persona.correo = form.cleaned_data['correo']
            nueva_persona.contrasena = make_password(form.cleaned_data['contrasena'])
            nueva_persona.id_rol = Rol.objects.get(nombre_rol=form.cleaned_data['id_rol'])

            nueva_persona.save()
            return redirect('welcome')

    else:
        form = RegistroPersonaForm()

    return render(request, 'registro_persona.html', {'form': form})


@login_required(login_url='login')
def welcome_view(request):
    if request.user.is_authenticated:
        return render(request, 'welcome.html')
    else:
        return redirect('login')


class LoginManager(Singleton):
    logged_in_users = set()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            cls._instance.logged_in_users = set()
        return cls._instance

    def login_user(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            self.logged_in_users.add(username)
            return True
        return False


def registrar_productos_view(request):
    print("Entrando a la vista registrar_productos")

    if request.method == 'POST':
        id_producto = request.POST.get('id')
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('RegistrarProducto', [id_producto, nombre, cantidad])
        except Exception as e:
            messages.error(request, f"Error al registrar el producto: {str(e)}")
        else:
            messages.success(request, "Producto registrado con éxito.")

    return render(request, 'registrar_productos.html')


def consultar_productos(request):
    print("Entrando a la vista consultar_productos")

    try:
        productos = Producto.objects.all()  # Obtener todos los productos
    except Exception as e:
        # Manejar el error si ocurre al consultar la base de datos
        return render(request, 'error.html', {'error_message': str(e)})

    return render(request, 'consultar_productos.html', {'productos': productos})


def generar_reportes_view(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        with connection.cursor() as cursor:
            cursor.callproc('GenerarReporteProductos', [fecha_inicio, fecha_fin])
            productos = cursor.fetchall()
            cursor.nextset()
            solicitudes = cursor.fetchall()

        # Convertir los resultados a formato JSON
        productos_json = [{'id_producto': producto[0], 'nombre_producto': producto[1],
                        'cantidad_total': producto[2], 'tipo_almacen': producto[3],
                        'direccion': producto[4], 'correo': producto[5], 'telefono': producto[6]} for producto in productos]

        solicitudes_json = [{'id_solicitud': solicitud[0], 'tipo_almacen': solicitud[1],
                            'nombre_persona': solicitud[2], 'nombre_producto': solicitud[3],
                            'cantidad': solicitud[4], 'fecha_solicitud': solicitud[5]} for solicitud in solicitudes]
        # Imprimir los resultados para verificar
        print("Productos obtenidos:")
        for producto in productos:
            print(producto)
        
        print("\nSolicitudes obtenidas:")
        for solicitud in solicitudes:
            print(solicitud)

        # Devolver los datos en formato JSON usando JsonResponse
        data = {'productos': productos_json, 'solicitudes': solicitudes_json}
        return JsonResponse(data)

    return render(request, 'seleccionar_fechas.html')



def solicitudes_view(request):
    result = None
    solicitud_data = None

    if request.method == 'POST':
        # Obtener datos del formulario
        tipo_almacen = request.POST.get('tipo_almacen')
        nombre_persona = request.POST.get('nombre_persona')
        nombre_producto = request.POST.get('nombre_producto')
        cantidad = request.POST.get('cantidad')

        # Imprimir los valores de los argumentos
        print("Tipo de Almacén:", tipo_almacen)
        print("Nombre de Persona:", nombre_persona)
        print("Nombre del Producto:", nombre_producto)
        print("Cantidad:", cantidad)

        # Llamar al procedimiento para insertar la solicitud
        with connection.cursor() as cursor:
            try:
                # Llamar al procedimiento 'Solicitud' para insertar la solicitud
                cursor.callproc(
                    'Solicitud', [None, cantidad, tipo_almacen, nombre_persona, nombre_producto])
                # Obtener el ID de la solicitud asignada
                solicitud_id = cursor.fetchone()[0]
                # Recuperar todos los datos de la solicitud recién insertada
                cursor.execute(
                    'SELECT * FROM almacen_app_solicitud WHERE id_solicitud = %s', [solicitud_id])
                solicitud_data = cursor.fetchone()

                # Llamar al procedimiento 'Datos' para obtener los datos para el formulario
                cursor.callproc('Datos')
                result = cursor.fetchall()
            except Exception as e:
                print(e)  # Manejar la excepción de manera adecuada en tu aplicación

    else:
        # Si la solicitud no es un POST, obtener los datos para el formulario
        with connection.cursor() as cursor:
            try:
                cursor.callproc('Datos')
                result = cursor.fetchall()
            except Exception as e:
                print(e)  # Manejar la excepción de manera adecuada en tu aplicación

    return render(request, 'solicitudes.html', {'result': result, 'solicitud_data': solicitud_data})


