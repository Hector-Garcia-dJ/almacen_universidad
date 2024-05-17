from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .commands import Command


class Rol(models.Model):
    DOCENTE = 'docente'
    MANTENIMIENTO = 'mantenimiento'

    ROL_CHOICES = [
        (DOCENTE, 'Docente'),
        (MANTENIMIENTO, 'Personal de Mantenimiento'),
    ]

    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=255, choices=ROL_CHOICES)

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=255)

    def clone(self):
        # Crea una nueva instancia de Persona clonando los atributos del objeto actual
        new_persona = Persona(
            id_rol=self.id_rol,
            nombre=self.nombre,
            apellido_paterno=self.apellido_paterno,
            apellido_materno=self.apellido_materno,
            telefono=self.telefono,
            correo=self.correo,
            contrasena=make_password(self.contrasena)  # Cifra la contraseña antes de guardarla
        )
        return new_persona
    
    # Obtenemos el nombre completo de la persona y sus apellidos
    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'


class Almacen(models.Model):
    id_almacen = models.AutoField(primary_key=True)
    tipo_almacen = models.CharField(max_length=255)
    direccion = models.TextField()
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

# Apartado del patron de diseño Factory Method
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=255)
    cantidad = models.IntegerField()

class ProductoFactory:
    def create_producto(self, id_producto, nombre, cantidad):
        return Producto.objects.create(id_producto=id_producto, nombre=nombre, cantidad=cantidad)

class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    tipo_almacen = models.CharField(max_length=255)
    nombre_persona = models.CharField(max_length=255)
    nombre_producto = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    fecha_solicitud = models.DateTimeField(default=datetime.now, blank=True)

    # Relación con otras clases
    id_almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def set_command(self, command):
        self.command = command

    def procesar_solicitud(self):
        if hasattr(self, 'command'):
            self.command.execute()
    # PATRON SINGLETON


class Singleton:
    _instance = None  # Variable de clase para almacenar la única instancia de la clase

    def __new__(cls):  # método "new_" que se llama al crear una nueva instancia en la clase
        if cls._instance is None:  # verificación de clase

            # si no hay instancia, crea una nueva utilizando "_new_"
            cls._instance = super(Singleton, cls).__new__(cls)

        return cls._instance  # devuelve la instancia existente o creada