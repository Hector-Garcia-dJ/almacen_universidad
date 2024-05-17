from django import forms
from django.core.exceptions import ValidationError  # Validación correo 
from .models import Solicitud, Producto, Persona, Almacen

class RegistroPersonaForm(forms.Form):
    id_rol = forms.CharField(max_length=255)
    nombre = forms.CharField(max_length=255)
    apellido_paterno = forms.CharField(max_length=255)
    apellido_materno = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=15)
    correo = forms.EmailField()
    contrasena = forms.CharField(max_length=255, widget=forms.PasswordInput())

# Dominios de la UACM
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')    
        # Validar el dominio del correo electrónico
        if not correo.endswith('@uacm.edu.mx'):
            raise ValidationError('El correo electrónico debe pertenecer al dominio uacm.edu.mx')
        return correo

#########################   
class SolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Consulta a la base de datos para obtener los nombres de los productos
        productos = Producto.objects.values_list('nombre_producto', flat=True)
        # Llena el campo nombre_producto con los nombres obtenidos
        self.fields['nombre_producto'] = forms.ChoiceField(choices=[(producto, producto) for producto in productos])

        # Consulta a la base de datos para obtener los nombres de las personas
        personas = Persona.objects.all()
        # Llena el campo nombre_persona con los nombres obtenidos
        self.fields['nombre_persona'] = forms.ModelChoiceField(queryset=personas, empty_label=None)

        # Consulta a la base de datos para obtener los tipos de almacén
        tipos_almacen = Almacen.objects.values_list('tipo_almacen', flat=True).distinct()
        # Llena el campo tipo_almacen con los tipos obtenidos
        self.fields['tipo_almacen'] = forms.ChoiceField(choices=[(tipo, tipo) for tipo in tipos_almacen])

    class Meta:
        model = Solicitud
        fields = ['tipo_almacen', 'nombre_producto', 'nombre_persona', 'cantidad']
#######################


#clase para enviar correos 
from django import forms

class SolicitudAlmacenCentralForm(forms.Form):
    campo_1 = forms.CharField(label='Campo 1', max_length=100)
    campo_2 = forms.IntegerField(label='Campo 2')
    # Agrega más campos según tus necesidades
